from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from . import views,api_views,get_api_views,delete_view,google_view

urlpatterns = [


    # Paypal setting
    path('paypal/token/', views.get_paypal_token, name='get_paypal_token'),
    path('paypal/create-payment/', views.create_payment, name='create_payment'),
    path('paypal/capture-payment/', views.capture_payment, name='capture_payment'),

    # marchant api
    path('reviewpayrole_api/order_validation', api_views.api_validation, name='order_validation'),
    path('reviewpayrole_api/ordertracking',api_views.api_ordertracking, name='order_tracking'),

    # cashback api
    path('reviewpayrole_api/get_cashback/',get_api_views.get_cashback, name='get_cashback'),
    path('reviewpayrole_api/cashback/', api_views.cashback, name='cashback'),

    # cashback api
    path('reviewpayrole_api/create_review_cashback/', api_views.create_review_cashback, name='create_review_cashback'),
    path('reviewpayrole_api/create_referral_cashback/', api_views.create_referral_cashback, name='create_referral_cashback'),

    # commimg soon api
    path('reviewpayrole_api/business_video_images', api_views.upload_business_video_and_image,name='business_video_images'),
    path('reviewpayrole_api/commingsoon',api_views.commingsoon, name='comming_soon_user'),
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
    # FaceBook Login
    path('api/auth/social/facebook', google_view.FacebookLogin.as_view(), name='facebook_login'),
    # logout 

    path('logout/', api_views.LogoutView.as_view(), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
