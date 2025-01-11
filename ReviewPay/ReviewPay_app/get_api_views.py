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
from .models import CategoryUsers, Businessdetail,BusinessVerifications, Employee, Product, UserDetail, Feedback,  Product, ProductImage, Barcode


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
def get_employee_detail(request, slug=None):
    user = request.user
    data = []
    try:
        # Check if slug is provided
        if slug:
            # Fetch specific employee using slug
            employee_detail = Employee.objects.filter(business=user, id=slug)  # Replace `id` with your slug field if it's different
        else:
            # Fetch all employees for the user
            employee_detail = Employee.objects.filter(business=user)

        if not employee_detail.exists():
            return JsonResponse({'error': 'No employee found with the given ID or slug'}, status=404)

        # Prepare data
        for employee in employee_detail:
            data.append({
                'id': employee.id,
                'employee_name': employee.employee_name,
                'identification_number': employee.identification_number,
                'designation': employee.designation,
                'email': employee.employee_email_address,
                'working_since': employee.working_since,
                'employee_profiles': f'https://superadmin.reviewpay.com.au{employee.employee_profiles.url}' if employee.employee_profiles else None,
                'user_email': employee.business.email
            })

        # Return data as JSON
        return JsonResponse(data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feedback(request, slug=None):
    user = request.user
    data = []
    try:
        # Check if slug is provided
        if slug:
            # Fetch specific employee using slug
            feedback = Feedback.objects.filter(business=user, id=slug)  # Replace `id` with your slug field if it's different
        else:
            # Fetch all employees for the user
            feedback = Feedback.objects.filter(business=user)

        if not feedback.exists():
            return JsonResponse({'error': 'No employee found with the given ID or slug'}, status=404)
        
         # Prepare data
        for item in feedback:
            data.append({
                'id': item.id,
                'issue_category': item.issue_category,
                'issue_description': item.issue_description,
                'urgency_level': item.urgency_level,
                'user_email': item.business.email
            })

        # Return data as JSON
        return JsonResponse(data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request, slug=None):
    # Saare products fetch karein
    try:
        user = request.user
        # Check if slug is provided
        if slug:
            # Fetch specific employee using slug
            products = Product.objects.filter(business=user, id=slug)  # Replace `id` with your slug field if it's different
        else:
            # Fetch all employees for the user
            products = Product.objects.filter(business=user)

        if not products.exists():
            return JsonResponse({'error': 'No employee found with the given ID or slug'}, status=404)
      
        
        # Response data prepare karna
        response_data = []
        for product in products:
            
            # Product images aur barcodes ko alag filter karna
            product_images = ProductImage.objects.filter(product=product)
            barcode_images = Barcode.objects.filter(product=product)
            # Image URLs prepare karna
            product_image_urls = ["https://superadmin.reviewpay.com.au"+image.image.url for image in product_images]
            barcode_image_urls = ["https://superadmin.reviewpay.com.au"+image.barcode_value.url for image in barcode_images]

            # Product data ko JSON mein add karna
            response_data.append({
                "id": product.id,
                "name": product.product_name,
                "price": str(product.product_price),
                "description": product.product_description,
                "product_images": product_image_urls,
                "barcodes": barcode_image_urls,
            })
           
        return JsonResponse({"products": response_data}, safe=False)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_verification(request):
    user = request.user
    try :
        business_verification = BusinessVerifications.objects.get(business=user)
    except:
        return JsonResponse({'error':'data is not find'}, status=404)

    try:
        data = {
                'id': business_verification.id,
                'ACN': business_verification.ACN,
                'business_web' : business_verification.business_web,
                'fullname_director_1' : business_verification.fullname_director_1,
                'fullname_director_2': business_verification.fullname_director_2,  # Assuming you want to send the ID of the related business
                'admin_phone_number': business_verification.admin_phone_number,
                'business_phone_number': business_verification.business_phone_number,
                'facebook_link': business_verification.facebook_link,
                'instagram_link' : business_verification.instra_link,
                'admin_email' : business_verification.admin_email,
                'client_email' : business_verification.client_email,
                'openning_hours' : business_verification.openning_hours,
                'government_issue_document' : 'http://192.168.100.14:8000'+business_verification.government_issue_document.url if business_verification.government_issue_document else None,
                'business_name_evidence' : 'http://192.168.100.14:8000'+business_verification.business_name_evidence.url if business_verification.business_name_evidence else None,
                'company_extract_issue' : 'http://192.168.100.14:8000'+business_verification.company_extract_issue.url if business_verification.company_extract_issue else None,  # Check if profile_image exists,
            }

        # Return the data as JSON
        return JsonResponse(data, safe=False, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)