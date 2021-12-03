import os.path
import re
import shutil
import zipfile
from io import BytesIO
from time import sleep
from typing import Optional
from urllib.parse import quote

import requests

from instance import settings
from notion_mirror import logger
from notion_mirror.domain import entities, ports


class Notion(ports.DocumentationSource):

    API_BASE_URL = "https://www.notion.so/api/v3/"

    NOTION_URLS_REGEX = re.compile(
        r"https://www\.notion\.so/(?:[a-z0-9-_]+-)?([a-f0-9]{32})", flags=re.IGNORECASE
    )

    def __init__(self) -> None:
        self.requests_session = requests.session()
        self.requests_session.cookies.set("token_v2", settings.NOTION_API_TOKEN)

    def get_page_content(self, page_id: str) -> str:  # pragma: no cover
        export_request_response = self._ask_to_export_page(page_id)
        exported_file_url = export_request_response["results"][0]["status"]["exportURL"]

        html_folder_original_name = self._download_export_file(
            page_id, exported_file_url
        )

        html_file_content = Notion._rewrite_html_file(
            page_id, html_folder_original_name
        )

        return html_file_content

    def _ask_to_export_page(self, page_id: str) -> dict:  # pragma: no cover
        # We first enqueue the export request
        enqueue_task_response: dict = self.requests_session.post(
            os.path.join(self.API_BASE_URL, "enqueueTask"),
            json={
                "task": {
                    "eventName": "exportBlock",
                    "request": {
                        "block": {
                            "id": Notion._get_alternative_page_id(page_id),
                            "spaceId": settings.NOTION_SPACE_ID,
                        },
                        "exportOptions": {
                            "exportType": "html",
                            "timeZone": "Europe/Paris",
                            "locale": "fr",
                        },
                        "recursive": False,
                    },
                },
            },
        ).json()

        task_id = enqueue_task_response["taskId"]

        while True:
            get_tasks_response: dict = self.requests_session.post(
                os.path.join(self.API_BASE_URL, "getTasks"), json={"taskIds": [task_id]}
            ).json()
            logger.info(get_tasks_response)

            if "error" in get_tasks_response["results"][0]:
                raise entities.exceptions.CannotGetPageContentError(
                    get_tasks_response["results"][0]["error"]
                )

            if (
                get_tasks_response["results"][0].get("status", {}).get("type", {})
                == "complete"
            ):
                return get_tasks_response
            else:
                sleep(1)

    def _download_export_file(
        self, page_id: str, export_file_url: str
    ) -> Optional[str]:  # pragma: no cover
        tmp_files_folder = os.path.join(settings.CACHE_FOLDER, "tmp", page_id)

        exported_file_response = self.requests_session.get(export_file_url)
        zipfile.ZipFile(BytesIO(exported_file_response.content)).extractall(
            tmp_files_folder
        )

        html_folder_original_name = None
        for file_name in os.listdir(tmp_files_folder):
            if file_name.endswith(".html"):
                shutil.move(
                    os.path.join(tmp_files_folder, file_name),
                    os.path.join(settings.CACHE_FOLDER, page_id + ".html"),
                )
            else:
                html_folder_original_name = file_name

                destination_folder = os.path.join(settings.CACHE_ASSETS_FOLDER, page_id)
                if os.path.exists(destination_folder):
                    shutil.rmtree(destination_folder)
                shutil.move(
                    os.path.join(tmp_files_folder, file_name),
                    destination_folder,
                )
        shutil.rmtree(tmp_files_folder)

        return html_folder_original_name

    @staticmethod
    def _rewrite_html_file(
        page_id: str, html_folder_original_name: Optional[str]
    ) -> str:  # pragma: no cover
        with open(
            os.path.join(settings.CACHE_FOLDER, page_id + ".html"), "r"
        ) as html_file:
            html_file_content = html_file.read()

        if html_folder_original_name is not None:
            html_file_content = Notion._rewrite_assets_urls(
                page_id, html_file_content, html_folder_original_name
            )

        html_file_content = Notion._rewrite_pages_urls(html_file_content)

        with open(
            os.path.join(settings.CACHE_FOLDER, page_id + ".html"), "w"
        ) as html_file:
            html_file.write(html_file_content)

        return html_file_content

    @staticmethod
    def _rewrite_assets_urls(
        page_id: str, html_file_content: str, html_folder_original_name: str
    ) -> str:
        return html_file_content.replace(
            f'"{quote(html_folder_original_name)}/', f'"/assets/{page_id}/'
        )

    @classmethod
    def _rewrite_pages_urls(cls, html_file_content: str) -> str:
        return cls.NOTION_URLS_REGEX.sub(r"/page/\1", html_file_content)

    @staticmethod
    def _get_alternative_page_id(page_id: str) -> str:
        """
        page_id is and hexadecimal ID but we want it to be seperated by some "-".
        """
        return "-".join(
            [
                page_id[0:8],
                page_id[8:12],
                page_id[12:16],
                page_id[16:20],
                page_id[20:],
            ]
        )
