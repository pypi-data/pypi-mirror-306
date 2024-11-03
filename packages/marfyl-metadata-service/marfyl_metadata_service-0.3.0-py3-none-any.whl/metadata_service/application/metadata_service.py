from .config import Config
from ..domain.services import MetaDataService
from ..infrastructure.header_parser import HeaderParser

class MetadataApplicationService:
    def __init__(self):
        self.meta_data_service = MetaDataService()

    def process_headers(self, headers: dict) -> None:
        parsed_headers = HeaderParser.parse(headers)
        self.meta_data_service.set_meta_data(parsed_headers)