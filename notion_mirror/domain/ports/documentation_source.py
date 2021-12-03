from abc import ABC, abstractmethod


class DocumentationSource(ABC):
    @abstractmethod
    def get_page_content(self, page_id: str) -> str:
        pass
