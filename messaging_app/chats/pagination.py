from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to set a default page size for messages.
    This class is used by Django REST Framework to paginate querysets.
    When applied, a 'page' object will have attributes like 'paginator.count'.
    """

    page_size = 10
    page_size_query_param='page_size'
    max_page_size=100
    