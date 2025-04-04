# core/filters.py
from rest_framework.filters import SearchFilter


class SmartSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        terms = super().get_search_terms(request)
        return [term.strip() for term in terms if term.strip()]

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        return super().filter_queryset(request, queryset, view)
