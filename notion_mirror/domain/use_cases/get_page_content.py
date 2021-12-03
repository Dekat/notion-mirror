from notion_mirror.domain import ports


class GetPageContent:
    def __init__(self, documentation_source: ports.DocumentationSource):
        self.documentation_source = documentation_source

    def perform(self, page_id: str) -> str:
        return self.documentation_source.get_page_content(page_id)
