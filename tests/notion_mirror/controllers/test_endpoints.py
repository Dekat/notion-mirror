from unittest.mock import MagicMock

from notion_mirror import registry


def test_ping(client):
    ping_response = client.get("/ping")

    assert "app" in ping_response.json
    assert ping_response.json["app"] == "ok"
    assert ping_response.status_code == 200


def test_page(client):
    registry.get_page_content.perform = MagicMock(return_value="coucou")

    page_response = client.get("/page/ee2affb1e6ae4b17bba33a895459f09e")

    assert page_response.status_code == 200
    registry.get_page_content.perform.assert_called_once_with(
        "ee2affb1e6ae4b17bba33a895459f09e"
    )
    assert page_response.data == b"coucou"
