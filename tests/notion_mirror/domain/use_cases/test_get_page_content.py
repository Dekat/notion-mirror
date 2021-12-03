from unittest.mock import MagicMock

from notion_mirror.domain import ports
from notion_mirror.domain.use_cases import GetPageContent


def test_page():
    use_case = GetPageContent(MagicMock(side_effect=ports.DocumentationSource))
    use_case.documentation_source.get_page_content = MagicMock(return_value="coucou")

    result = use_case.perform("ee2affb1e6ae4b17bba33a895459f09e")

    assert result == "coucou"
    use_case.documentation_source.get_page_content.assert_called_once_with(
        "ee2affb1e6ae4b17bba33a895459f09e"
    )
