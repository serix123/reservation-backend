from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservation.viewsets import (
    ApprovalViewSet,
    DepartmentViewSet,
    EquipmentViewSet,
    FacilityViewSet,
    EventViewSet,
)
from reservation.views import (
    department_views,
    employee_views,
    approve_by_immediate_head,
    revoke_by_immediate_head,
    reject_by_immediate_head,
    approve_by_person_in_charge,
    revoke_by_person_in_charge,
    reject_by_person_in_charge,
    approve_by_admin,
    revoke_by_admin,
    reject_by_admin,
    get_all,
)


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

approver_paths = [
    path('approve_by_immediate_head/<int:pk>/',
         approve_by_immediate_head, name='approve_by_immediate_head'),
    path('approve_by_person_in_charge/<int:pk>/',
         approve_by_person_in_charge, name='approve_by_person_in_charge'),
    path('approve_by_admin/<int:pk>/',
         approve_by_admin, name='approve_by_admin'),
    path('revoke_by_person_in_charge/<int:pk>/',
         revoke_by_person_in_charge, name='revoke_by_person_in_charge'),
    path('revoke_by_immediate_head/<int:pk>/',
         revoke_by_immediate_head, name='revoke_by_immediate_head'),
    path('revoke_by_admin/<int:pk>/',
         revoke_by_admin, name='revoke_by_admin'),
    path('reject_by_immediate_head/<int:pk>/',
         reject_by_immediate_head, name='reject_by_immediate_head'),
    path('reject_by_person_in_charge/<int:pk>/',
         reject_by_person_in_charge, name='reject_by_person_in_charge'),
    path('reject_by_admin/<int:pk>/',
         reject_by_admin, name='reject_by_admin'),
    path('', get_all, name='get-all-approval'),
]

router = DefaultRouter()
router.register(r"approval", ApprovalViewSet, basename="vs-approval")
router.register(r"department", DepartmentViewSet, basename="vs-department")
router.register(r"equipment", EquipmentViewSet, basename="vs-equipment")
router.register(r"facility", FacilityViewSet, basename="vs-facility")
router.register(r"event", EventViewSet, basename="vs-event")

urlpatterns = [
    path("departments/", include(department_paths)),
    path("employee/", include(employee_paths)),
    path("approval/actions/", include(approver_paths)),
    path("", include(router.urls)),
]
