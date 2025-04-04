import json
import threading
import time
import base64
import os
import qrcode
import uuid

from django.http import HttpResponse
import secrets
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
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
from .models import CategoryUsers, Businessdetail,BusinessVerifications, Employee
from .models import Product, UserDetail, Feedback, ProductImage, Barcode, BusinessState
from .models import BusinessImage,BusinessLogo,BusinessVideo,UserCashBack
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
                'profile_image': 'http://192.168.100.14:8000' + user_detail.profile_image.url if user_detail.profile_image else None,  # Check if profile_image exists
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
        videos = business_detail.business_video.all()
        logos = business_detail.business_logo.all() 
        images = business_detail.business_image.all()

    except:
        return JsonResponse({'error':'data is not find'}, status=404)

    try:
        data = {
                'id': business_detail.id,
                'business_name': business_detail.business_name,
                'marchant api' : business_detail.marchant_api_key,
                'email' : business_detail.business.email,
                'business_address' : business_detail.business_address,
                'abn_number': business_detail.abn_number,  # Assuming you want to send the ID of the related business
                'category': business_detail.category,
                'sub_category': business_detail.sub_category,
                'Logos' : ['https://superadmin.reviewpay.com.au' + logo.image.url for logo in logos],
                'video' : ['https://superadmin.reviewpay.com.au' + video.video.url for video in videos],
                'images': ['https://superadmin.reviewpay.com.au' + image.image.url for image in images],
                "review_cashbacks": list(business_detail.ReviewCashback.all().values(
                                        "id", "review_amount_cashback_percent", "review_amount_cashback_fixed",
                                        "review_cashback_return_refund_period", "review_cashback_expiry"
                )),
                # Referral Cashback
                "referral_cashbacks": list(business_detail.ReferralCashback.all().values(
                                        "id", "referral_cashback_enabled", "referral_amount_cashback_percent",
                                        "referral_amount_cashback_fixed", "referral_cashback_return_refund_period",
                                        "referral_cashback_expiry"
                )),
                }

        # Return the data as JSON
        return JsonResponse(data, safe=False, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_detail_all(request):
    
    user = request.user
    business_details = Businessdetail.objects.all()
    all_data = []
    try:
        for business_detail in business_details:
            try :
                videos = business_detail.business_video.all()
                logos = business_detail.business_logo.all() 
                images = business_detail.business_image.all()

            except:
                return JsonResponse({'error':'data is not find'}, status=404)

            try:
                data = {
                        'id': business_detail.id,
                        'business_name': business_detail.business_name,
                        'marchant api' : business_detail.marchant_api_key,
                        'email' : business_detail.business.email,
                        'business_address' : business_detail.business_address,
                        'abn_number': business_detail.abn_number,  # Assuming you want to send the ID of the related business
                        'category': business_detail.category,
                        'sub_category': business_detail.sub_category,
                        'Logos' : ['https://superadmin.reviewpay.com.au' + logo.image.url for logo in logos],
                        'video' : ['https://superadmin.reviewpay.com.au' + video.video.url for video in videos],
                        'images': ['https://superadmin.reviewpay.com.au' + image.image.url for image in images],
                        "review_cashbacks": list(business_detail.ReviewCashback.all().values(
                                                "id", "review_amount_cashback_percent", "review_amount_cashback_fixed",
                                                "review_cashback_return_refund_period", "review_cashback_expiry"
                        )),
                        # Referral Cashback
                        "referral_cashbacks": list(business_detail.ReferralCashback.all().values(
                                                "id", "referral_cashback_enabled", "referral_amount_cashback_percent",
                                                "referral_amount_cashback_fixed", "referral_cashback_return_refund_period",
                                                "referral_cashback_expiry"
                        )),
                        }
                all_data.append(data)
            except:
                return JsonResponse({'error':'data is not find'}, status=404)
                # Return the data as JSON

        return JsonResponse(all_data, safe=False, status=200)

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
                'government_issue_document' : 'http://192.168.100.14:8000'+ business_verification.government_issue_document.url if business_verification.government_issue_document else None,
                'business_name_evidence' : 'http://192.168.100.14:8000'+ business_verification.business_name_evidence.url if business_verification.business_name_evidence else None,
                'company_extract_issue' : 'http://192.168.100.14:8000'+ business_verification.company_extract_issue.url if business_verification.company_extract_issue else None,  # Check if profile_image exists,
            }

        # Return the data as JSON
        return JsonResponse(data, safe=False, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_business_state(request):
    business_state = BusinessState.objects.get()
    return JsonResponse({'name': business_state.product_name,
                         'quality' : business_state.quality,
                         'performance' : business_state.performance,
                         'easy_to_use' : business_state.easy_to_use,
                         'durability' : business_state.durability,
                        }, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cashback(request):
    user = request.user
    try:
        try:
            user_detail = UserDetail.objects.get(business=user)
        except:
            return JsonResponse({'error':'user_detail not fullfill'}, status=404)
        if user_detail:
            invoice = 0
            cashback_price = 0
            user_cashback = user_detail.usercashback.all()
            data = []
            for cashback in user_cashback:
            
                data.append({
                    'id': cashback.id,
                    'user_id': cashback.user.id,
                    'business_id' : cashback.business_id,
                    'invoice price' : cashback.invoice_price,
                    'amount' : cashback.amount,
                    'created date' : cashback.created_date,

                })
                
                invoice += cashback.invoice_price
                cashback_price += cashback.amount
            whole_data = {'invoice': invoice, 'cashback': cashback_price, 'total invoice': data}
            return JsonResponse(whole_data, safe=False, status=200)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_qr_api(request, Business_id):
    # Data to be encoded in the QR code
    # import pdb;pdb.set_trace()
    data = f"http://127.0.0.1:8000/reviewpayrole_api/qr_scan/?user_id={request.user.id}&Business_id={Business_id}&status=pending"

    # Create the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create image from QR code
    img = qr.make_image(fill="black", back_color="white")

    # Save image to a BytesIO object to send in the response
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the image as HTTP response
    return HttpResponse(buffer, content_type="image/png")

@api_view(['GET'])
@permission_classes([AllowAny])  # Anyone can scan the QR
def qr_scan_api(request):
    user_id = request.GET.get("user_id")
    business_id = request.GET.get("business_id")
    scan_url = request.build_absolute_uri()
    
    # Store scan in database
    if user_id and business_id:
        QRScan.objects.create(
            user_id=user_id,
            business_id=business_id,
            scan_url=scan_url,
            status="pending"
        )
        return JsonResponse({"message": "Scan recorded", "status": "pending"}, status=status.HTTP_201_CREATED)
    
    return JsonResponse({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)