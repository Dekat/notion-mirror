import pytest

from notion_mirror.adapters import Notion


@pytest.mark.parametrize(
    "html_page_content_input, html_folder_original_name, html_page_content_output",
    [
        (
            """
            <img style="width:232px"
            src="%5BK%5D%20Coucou%20test%20325850f921cf4da3a65ae1f033cb2f0e/screenshot%203.png"
            />
            """,
            "[K] Coucou test 325850f921cf4da3a65ae1f033cb2f0e",
            """
            <img style="width:232px"
            src="/assets/03d9b47453884ea6b50fee5a99e97df7/screenshot%203.png"
            />
            """,
        ),
        (
            """
            <img src="bla/screenshot.jpg" >
            """,
            "bla",
            """
            <img src="/assets/03d9b47453884ea6b50fee5a99e97df7/screenshot.jpg" >
            """,
        ),
    ],
)
def test_rewrite_assets_urls(
    html_page_content_input: str,
    html_folder_original_name: str,
    html_page_content_output: str,
):
    assert (
        Notion._rewrite_assets_urls(
            "03d9b47453884ea6b50fee5a99e97df7",
            html_page_content_input,
            html_folder_original_name,
        )
        == html_page_content_output
    )


@pytest.mark.parametrize(
    "html_page_content_input, html_page_content_output",
    [
        (
            """
            <a href="https://www.notion.so/coucou-01d9b47453884ea6b50fee5a99e97df7">
            """,
            """
            <a href="/page/01d9b47453884ea6b50fee5a99e97df7">
            """,
        ),
        (
            """
            <a href="https://www.notion.so/test_coucou-02d9b47453884ea6b50fee5a99e97df7">
            """,
            """
            <a href="/page/02d9b47453884ea6b50fee5a99e97df7">
            """,
        ),
        (
            """
            <a
                href="https://www.notion.so/03d9b47453884ea6b50fee5a99e97df7"
                style="border: 1px;"
            >
            """,
            """
            <a
                href="/page/03d9b47453884ea6b50fee5a99e97df7"
                style="border: 1px;"
            >
            """,
        ),
    ],
)
def test_rewrite_pages_urls(
    html_page_content_input: str, html_page_content_output: str
):
    assert (
        Notion._rewrite_pages_urls(html_page_content_input) == html_page_content_output
    )


@pytest.mark.parametrize(
    "from_page_id, to_page_id",
    [
        ("ee2affb1e6ae4b17bba33a895459f09e", "ee2affb1-e6ae-4b17-bba3-3a895459f09e"),
        ("3b240f624d024db8bc7ec23ab42ce5ea", "3b240f62-4d02-4db8-bc7e-c23ab42ce5ea"),
    ],
)
def test_get_alternative_page_id(from_page_id: str, to_page_id: str):
    assert Notion._get_alternative_page_id(from_page_id) == to_page_id
