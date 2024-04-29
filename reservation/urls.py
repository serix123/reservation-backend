from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservation.viewsets import (
    DepartmentViewSet,
    EquipmentViewSet,
    FacilityViewSet,
    EventViewSet,
)
from reservation.views import department_views, employee_views


department_paths = [
    path("create/", department_views.insert, name="dept-create"),
    path("delete/<str:pk>", department_views.delete, name="dept-delete"),
    path("get/<str:pk>", department_views.get, name="dept-get"),
    path("update/<str:pk>", department_views.update, name="dept-update"),
    path(
        "update-dept/<str:pk>", department_views.update_department, name="dept-update-2"
    ),
    path("get/", department_views.get_all, name="dept-get-all"),
    path(
        "update/head/<int:pk>",
        department_views.update_dept_head,
        name="update-department-head",
    ),
]

employee_paths = [
    path(
        "update-employees-department/",
        employee_views.update_employees_department,
        name="update-employees-department",
    ),
    path("get/", employee_views.get_all, name="emp-get-all"),
    path("get/<str:pk>", employee_views.get, name="emp-get"),
    path("update-emp/<str:pk>", employee_views.update_employees, name="emp-update"),
]

router = DefaultRouter()
router.register(r"department", DepartmentViewSet, basename="vs-department")
router.register(r"equipment", EquipmentViewSet, basename="vs-equipment")
router.register(r"facility", FacilityViewSet, basename="vs-facility")
router.register(r"event", EventViewSet, basename="vs-event")

urlpatterns = [
    path("departments/", include(department_paths)),
    path("employee/", include(employee_paths)),
    path("", include(router.urls)),
]
