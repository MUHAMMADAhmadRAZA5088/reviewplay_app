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
    pass
