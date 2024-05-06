from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
    path("register/admin/", user_views.register_admin, name="admin-registration"),
    path("register/employee/", user_views.register_employee,
         name="employee-registration"),
    path("token/", include(token_paths)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
