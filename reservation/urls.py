from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservation.viewsets import DepartmentViewSet

from .views import department_views

department_paths = [
    path("create/", department_views.INSERT, name="dept-create"),
    path("delete/<str:pk>", department_views.DELETE, name="dept-delete"),
    path("get/<str:pk>", department_views.GET, name="dept-get"),
    path("update/<str:pk>", department_views.GET, name="dept-update"),
    path("get/", department_views.GET_ALL, name="dept-get-all"),
]

router = DefaultRouter()
router.register(r"department", DepartmentViewSet, basename="vs-department")

urlpatterns = [
    path("departments/", include(department_paths)),
    path("", include(router.urls)),
]
