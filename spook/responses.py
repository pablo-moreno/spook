class ProxyResponse(object):
    def __init__(self, queryset, status):
        self.queryset = queryset
        self.status = status
