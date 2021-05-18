class Pagination(object):
    pagination_query_param = 'page'

    def paginate(self, data: list) -> dict:
        return {
            'results': data,
        }
