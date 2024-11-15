from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from . import views,api_views

urlpatterns = [
    # path('', views.signup, name='signup'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='login_out'),
    # path('home/', views.home, name='home'),

    path('reviewpayrole_api/signup/', api_views.api_signup, name='api_signup'),
    path('reviewpayrole_api/login/', api_views.api_login, name='api_login'),
    path('reviewpayrole_api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
