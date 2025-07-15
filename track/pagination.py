from rest_framework.pagination import PageNumberPagination

# Для публичных треков
class TrackListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 20

class AnswerListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10

class AnswerCommentPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10