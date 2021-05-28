class BasePagination(object):
    def __init__(self, data: dict, context: dict = None):
        self.data = data
        self.context = context

    def get_next(self) -> str:
        raise NotImplementedError

    def get_previous(self) -> str:
        raise NotImplementedError

    def get_count(self) -> int:
        raise NotImplementedError

    def get_results(self) -> list:
        raise NotImplementedError

    def get_paginated_response(self) -> dict:
        return {
            "next": self.get_next(),
            "previous": self.get_previous(),
            "count": self.get_count(),
            "results": self.get_results(),
        }


class DefaultPagination(BasePagination):
    def get_next(self) -> str:
        return self.data.get("next", "")

    def get_previous(self) -> str:
        return self.data.get("previous", "")

    def get_count(self) -> int:
        return self.data.get("count", 0)

    def get_results(self) -> list:
        return self.data.get("results", [])
