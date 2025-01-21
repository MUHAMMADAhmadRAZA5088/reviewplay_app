from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from . import views,api_views,get_api_views,delete_view,google_view

urlpatterns = [
    path('reviewpayrole_api/get_statistics',get_api_views.get_business_state, name='get_statistics'),
    path('reviewpayrole_api/get_feedback/<int:slug>/', get_api_views.get_feedback, name='get_feedback'),
    path('reviewpayrole_api/get_feedback', get_api_views.get_feedback, name='get_feedback'),
    path('reviewpayrole_api/feedback', api_views.feedback, name='feedback'),
    path('reviewpayrole_api/get_employee_detail/<int:slug>/',get_api_views.get_employee_detail, name="employee_detail"),
    path('reviewpayrole_api/get_employee_detail',get_api_views.get_employee_detail, name="employee_detail"),
    path('reviewpayrole_api/get_user_detail', get_api_views.get_user_detail, name="get_user_detail"),
    path('reviewpayrole_api/get_business_detail', get_api_views.get_business_detail, name="get_business_detail"),
    path('reviewpayrole_api/user/user_detail', api_views.user_detail, name='user_detail'),
    path('reviewpayrole_api/business/products_detail', api_views.product, name='products_detals'),
    path('reviewpayrole_api/get_products',get_api_views.get_products, name="get_products"),
    path('reviewpayrole_api/get_products/<int:slug>/',get_api_views.get_products, name="get_products_with_id"),
    path('reviewpayrole_api/delete_product/<int:slug>/',delete_view.delete_product, name="delete_product"),
    path('reviewpayrole_api/business/employee_detail', api_views.employee_detail, name='employee_detail'),
    path('reviewpayrole_api/business/business_detail', api_views.create_or_update_business_detail, name='business_detail'),
    path('reviewpayrole_api/business/business_verification', api_views.business_verifications, name='business_verification'),   
    path('reviewpayrole_api/business/get_business_verification', get_api_views.get_business_verification, name='business_verification'),     
    path('reviewpayrole_api/signup/', api_views.api_signup, name='api_signup'),
    path('reviewpayrole_api/login/', api_views.api_login, name='api_login'),
    path('reviewpayrole_api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reviewpayrole_api/password-reset/', api_views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reviewpayrole_api/password-reset/<uidb64>/<token>/', api_views.ResetPasswordView.as_view(), name='password_reset_confirm'),
    # Google Login
    path('api/auth/social/google', google_view.GoogleLogin.as_view(), name='google_login'),
    # logout 
    path('logout/', api_views.LogoutView.as_view(), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
