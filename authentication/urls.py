from django.urls import path, include


from authentication.views.csv_views import upload_csv_create_users
from authentication.views.token_views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import user_views


token_paths = [
    path("", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("default/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("register/", user_views.register, name="user-registration"),
    path("delete/<str:pk>/", user_views.delete, name="user-delete"),
    path("update/<str:pk>/", user_views.update, name="user-update"),
    path('upload-csv/', upload_csv_create_users,
         name='upload_csv_create_users'),
    path("register/admin/", user_views.register_admin, name="admin-registration"),
    path("register/employee/", user_views.register_employee,
         name="employee-registration"),
    path("token/", include(token_paths)),
]
