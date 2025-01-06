import json
import threading
import time
import base64
import os
import uuid

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
from .models import CategoryUsers, Businessdetail, Employee, Product, UserDetail


User = get_user_model()  # Get the custom user model

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_detail(request):
    user = request.user
    try:
        user_detail = UserDetail.objects.get(business=user)
    except:
        return JsonResponse({'error':'data is not find'}, status=404)
    try:
        data = {
                'id': user_detail.id,
                'first_name': user_detail.first_name,
                'email' : user_detail.business.email,
                'last_name': user_detail.last_name,  # Assuming you want to send the ID of the related business
                'gender': user_detail.gender,
                'date_of_birth': user_detail.date_of_birth,
                'profile_image': 'http://192.168.100.14:8000'+user_detail.profile_image.url if user_detail.profile_image else None,  # Check if profile_image exists
                'email' : user_detail.business.email,
            }
        
        # Return the data as JSON
        return JsonResponse(data, status=200)
        
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_detail(request):
    user = request.user
    try :
        business_detail = Businessdetail.objects.get(business=user)
    except:
        return JsonResponse({'error':'data is not find'}, status=404)

    try:
        data = {
                'id': business_detail.id,
                'business_name': business_detail.business_name,
                'email' : business_detail.business.email,
                'business_address' : business_detail.business_address,
                'abn_number': business_detail.abn_number,  # Assuming you want to send the ID of the related business
                'category': business_detail.category,
                'sub_category': business_detail.sub_category,
                'businessLogo': 'http://192.168.100.14:8000'+business_detail.businessLogo.url if business_detail.businessLogo else None,  # Check if profile_image exists
                'email' : business_detail.business.email,
            }

        # Return the data as JSON
        return JsonResponse(data, safe=False, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_detail(request):
    # import pdb;pdb.set_trace()
    user = request.user
    data = []
    try :
        employee_detail = Employee.objects.filter(business=user)
        for employee in employee_detail:
            data.append({
                'id': employee.id,
                'employee_name': employee.employee_name,
                'identification_number' : employee.identification_number,
                'designation' : employee.designation,
                'email' : employee.employee_email_address,
                'working_since' : employee.working_since,
                'employee_profiles' : 'http://127.0.0.1:8000/' + employee.employee_profiles.url,  # Check if profile_image exists
                'user_email' : employee.business.email

            })
            # Return the data as JSON
        return JsonResponse(data, safe=False, status=200)
    except:
        return JsonResponse({'error':'data is not find'}, status=404)

