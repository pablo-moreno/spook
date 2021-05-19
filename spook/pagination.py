class BasePagination(object):
    def __init__(self, data: dict):
        self.data = data

    def get_next(self) -> str:
        raise NotImplementedError

    def get_previous(self) -> str:
        raise NotImplementedError

    def get_count(self) -> int:
        raise NotImplementedError

    def get_results(self) -> str:
        raise NotImplementedError

    def get_paginated_response(self) -> dict:
        return {
            'next': self.get_next(),
            'previous': self.get_previous(),
            'count': self.get_count(),
            'results': self.get_results(),
        }
