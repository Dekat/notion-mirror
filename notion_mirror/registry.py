from notion_mirror import adapters
from notion_mirror.domain import use_cases


get_page_content = use_cases.GetPageContent(adapters.Notion())
