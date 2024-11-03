from typing import Dict

class HeaderParser:
    @staticmethod
    def parse(headers: Dict[str, str]) -> Dict[str, str]:
        return {k.lower(): v for k, v in headers.items()}