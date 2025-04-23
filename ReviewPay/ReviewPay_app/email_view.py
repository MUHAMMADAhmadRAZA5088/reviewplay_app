import json
import threading
import time
import base64
import os
import uuid
import time
import sib_api_v3_sdk



from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.views import APIView
from django.utils.timezone import now
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime
from .models import CategoryUsers, Businessdetail,BusinessVerifications, Employee,favorate_business
from .models import Product, UserDetail, Feedback,  Product, ProductImage, Barcode


@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email(request):
    import pdb;pdb.set_trace()
    configuration = sib_api_v3_sdk.Configuration()
    # configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    subject = "My Subject"
    html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
    sender = {"name":"Robert","email":"hello@reviewpay.com.au"}
    to = [{"email":"ahmadelectricaltraders@gmail.com","name":"ahmad"}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)
    import pdb;pdb.set_trace()
