import json
import threading
import time
import base64
import os
import qrcode
import uuid

from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect

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
from .models import CategoryUsers, Businessdetail,BusinessVerifications, Employee, favorate_business
from .models import Product, UserDetail, Feedback, ProductImage, Barcode, BusinessState, Follow
from .models import BusinessImage,BusinessLogo,BusinessVideo,UserCashBack, QRScan,Notifications
from .models import Product_business_invoice, NotificationMassage, UserSession, refferial_code
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
                'email' : user_detail.email,
                'last_name': user_detail.last_name,  # Assuming you want to send the ID of the related business
                'gender': user_detail.gender,
                'date_of_birth': user_detail.date_of_birth,
                'profile_image': 'https://superadmin.reviewpay.com.au' + user_detail.profile_image.url if user_detail.profile_image else None,  # Check if profile_image exists
                'profile_image_color' : user_detail.profile_image_color,
                'phone_number': user_detail.phone_number,
                'post_code' : user_detail.post_code,
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
            try:
                business_verification = BusinessVerifications.objects.get(business= business_detail.business) 
                
                verification = {
                    'id': business_verification.id,
                    'business_web': business_verification.business_web,
                    'ACN' : business_verification.ACN,
                    'fullname_director_1' : business_verification.fullname_director_1,
                    'fullname_director_2' : business_verification.fullname_director_2,
                    'admin_phone_number' : business_verification.admin_phone_number,
                    'business_phone_number' : business_verification.business_phone_number,
                    'facebook_link' : business_verification.facebook_link,
                    'instagram_link' : business_verification.instra_link,
                    'admin_email' : business_verification.admin_email,
                    'client_email' : business_verification.client_email,
                    'openning_hours' : business_verification.openning_hours,
                }
                
            except:
                verification = {}

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
                        'business_verification': verification,
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
                'government_issue_document' : 'https://superadmin.reviewpay.com.au'+ business_verification.government_issue_document.url if business_verification.government_issue_document else None,
                'business_name_evidence' : 'https://superadmin.reviewpay.com.au'+ business_verification.business_name_evidence.url if business_verification.business_name_evidence else None,
                'company_extract_issue' : 'https://superadmin.reviewpay.com.au'+ business_verification.company_extract_issue.url if business_verification.company_extract_issue else None,  # Check if profile_image exists,
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
def generate_qr_api(request, Business_id):
    
    try:
        business_detail_instance = Businessdetail.objects.get(id=Business_id)
    except:
        return JsonResponse({'error':'business not found'}, status=404)
    
    data = f"https://superadmin.reviewpay.com.aureviewpayrole_api/qr_scan/?user_id={request.user.id}&Business_id={Business_id}&url={business_detail_instance.business_url}&status=pending"
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
    business_id = request.GET.get("Business_id")
    status = request.GET.get("status")
    url = request.GET.get("url")
    scan_url = request.build_absolute_uri()

    # Store scan in database
    if user_id and business_id:
        scan_entry = QRScan.objects.create(
            user_id=user_id,
            business_id=business_id,
            scan_url=url,
            status=status
        )
        return redirect(f"{url}?uccid={scan_entry.id}&user_id{user_id}&business_id={business_id}")
        # return JsonResponse({
        #     "message": "Scan recorded",
        #     "status": "pending",
        #     "scan_id": scan_entry.id,  
        #     "business_id" : business_id,
        #     "user_id" : user_id,
        #     "website_url" : f"{url}?uccid={scan_entry.id}&user_id{user_id}&business_id={business_id}"
        # }, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def business_message_alert(request):
    user = request.user
    try:
        try:
            business_detail = Businessdetail.objects.get(business=user)
            if business_detail:
                business_detal = "Add Business detail successfully"
            else:
                business_detal = "Add Business detail failed"
            images = business_detail.business_image.all()
            if images:
                product_img = "Add product images successfully"
            else :
                product_img = "Add product images failed"
        except:
            business_detal = "Add Business detail failed"
            product_img = "Add product images failed"
        
        try:
            business_verification = BusinessVerifications.objects.get(business= business_detail.business) 
            if business_verification:
                business_verify = "Business verification successfully"
            else:
                business_verify = "Business verification failed"
        except:
            business_verify = "Business verification failed"
        
        return JsonResponse({"Business Detail": business_detal, "product image" : product_img, "business verification" : business_verify }, safe=False, status=200)
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification(request):
    user = request.user
    try:
        notification = Notifications.objects.get(user_id=user)
        current_date = date.today()
        
        if notification.business_detail_date:
            total_day = (current_date - notification.business_detail_date).days
            if total_day >= 3 and notification.business_detail == 'delay' :
                notification.business_detail = 'pending'
                notification.business_detail_date = date.today()
                notification.save()
        
        if notification.product_image_date:
            total_day = (current_date - notification.product_image_date).days
            if total_day >= 3 and notification.product_image == 'delay' :
                notification.product_image = 'pending'
                notification.product_image_date = date.today()
                notification.save()

        if notification.business_verify_date:
            total_day = (current_date - notification.business_verify_date).days
            if total_day >= 3 and notification.business_verify == 'delay' :
                notification.business_verify = 'pending'
                notification.business_verify_date = date.today()
                notification.save()
                
        return JsonResponse({'id': notification.id,
                             'business_detail':notification.business_detail,
                             'business_detail_date':notification.business_detail_date,
                             'product_image':notification.product_image,
                             'product_image_date':notification.product_image_date,
                             'business_verify':notification.business_verify,
                             'business_verify_date':notification.business_verify_date
                             }, safe=False, status=200)
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_detail_one(request, Business_id):

    try :
        business_detail = Businessdetail.objects.get(id = Business_id)
        videos = business_detail.business_video.all()
        logos = business_detail.business_logo.all() 
        images = business_detail.business_image.all()
        try:
            business_verification = BusinessVerifications.objects.get(business= business_detail.business) 
        except:
            business_verification = None
        verification = {}
        if business_verification:
            verification = {
                    'id': business_verification.id,
                    'business_web': business_verification.business_web,
                    'ACN' : business_verification.ACN,
                    'fullname_director_1' : business_verification.fullname_director_1,
                    'fullname_director_2' : business_verification.fullname_director_2,
                    'admin_phone_number' : business_verification.admin_phone_number,
                    'business_phone_number' : business_verification.business_phone_number,
                    'facebook_link' : business_verification.facebook_link,
                    'instagram_link' : business_verification.instra_link,
                    'admin_email' : business_verification.admin_email,
                    'client_email' : business_verification.client_email,
                    'openning_hours' : business_verification.openning_hours,
                }
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
                "verification": verification
                }

        # Return the data as JSON
        return JsonResponse(data, safe=False, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['GET'])
def generate_qr_business(request, Business_id):
    
    try:
        business_detail_instance = Businessdetail.objects.get(id=Business_id)
        business_user = BusinessVerifications.objects.get(business=business_detail_instance.business)
    except:
        return JsonResponse({'error':'business not found'}, status=404)
    
    data = f"https://superadmin.reviewpay.com.aureviewpayrole_api/qr_scan/?Business_id={Business_id}&url={business_user.business_web}&status=pending"
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
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def qr_scan_api_business(request):
    user_id = request.user.id
    business_id = request.GET.get("Business_id")
    status = request.GET.get("status")
    url = request.GET.get("url")
    scan_url = request.build_absolute_uri()

    # Store scan in database
    if user_id and business_id:
        scan_entry = QRScan.objects.create(
            user_id=user_id,
            business_id=business_id,
            scan_url=url,
            status=status
        )
        # return redirect(f"{url}?uccid={scan_entry.id}&user_id{user_id}&business_id={business_id}")
        return JsonResponse({
            "message": "Scan recorded",
            "status": "pending",
            "scan_id": scan_entry.id,  
            "business_id" : business_id,
            "user_id" : user_id,
            "website_url" : f"{url}?uccid={scan_entry.id}&user_id{user_id}&business_id={business_id}"
        }, status=200)
    
    return JsonResponse({"massage": "please login the reviewpay",url : "https://reviewpay.com.au/signin"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_favorite_businesses(request):
    user = request.user
    user = UserDetail.objects.get(business=user)
    favorites = favorate_business.objects.filter(user=user)
    all_data = []
    try:
        for favorite in favorites:
            try:
                business_detail = Businessdetail.objects.get(id= favorite.business_id)
                business_verification = BusinessVerifications.objects.get(business= business_detail.business) 
                
                verification = {
                    'id': business_verification.id,
                    'business_web': business_verification.business_web,
                    'ACN' : business_verification.ACN,
                    'fullname_director_1' : business_verification.fullname_director_1,
                    'fullname_director_2' : business_verification.fullname_director_2,
                    'admin_phone_number' : business_verification.admin_phone_number,
                    'business_phone_number' : business_verification.business_phone_number,
                    'facebook_link' : business_verification.facebook_link,
                    'instagram_link' : business_verification.instra_link,
                    'admin_email' : business_verification.admin_email,
                    'client_email' : business_verification.client_email,
                    'openning_hours' : business_verification.openning_hours,
                }
                
            except:
                verification = {}

            try :
                videos = business_detail.business_video.all()
                logos = business_detail.business_logo.all() 
                images = business_detail.business_image.all()

            except:
                return JsonResponse({'error':'data is not find'}, status=404)

            try:
                data = {
                        'favirote' : favorite.id,
                        'id': business_detail.id,
                        'business_name': business_detail.business_name,
                        'marchant api' : business_detail.marchant_api_key,
                        'email' : business_detail.business.email,
                        'business_address' : business_detail.business_address,
                        'abn_number': business_detail.abn_number,  # Assuming you want to send the ID of the related business
                        'category': business_detail.category,
                        'sub_category': business_detail.sub_category,
                        'business_verification': verification,
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
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def history_product_business_invoice(request):
    try:
        user = request.user
        if user.role == 'business':

            try:
                business = BusinessVerifications.objects.get(business= user)
                products = Product_business_invoice.objects.filter(business= business)
                all_data = []
                for product in products:
                    all_data.append( {
                        'id' : product.id,
                        'user_id' : product.user.id,
                        'business_id' : product.business.id,
                        'product_service' : product.product_service,
                        'invoice_amount' : product.invoice_amount,
                        'reviewcashback' : product.reviewcashback,
                        'refferial_code' : product.refferial_code,
                        'client_name' : product.client_name,
                        'client_phone' : product.client_phone,
                        'client_email' : product.client_email
                    })
                    
            
                return JsonResponse(all_data, safe=False, status=200)
            except:
                return JsonResponse({'error':'data is not find'}, status=404)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_followers(request):
    user = request.user
    followers = Follow.objects.filter(following=user)
    data = []
    for f in followers:
        data.append({
            'id': f.follower.id,
            'username': f.follower.username,
        })

    return JsonResponse({'followers': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_following(request):
    user = request.user
    following = Follow.objects.filter(follower=user)
    data = []
    for f in following:
        data.append({
            'id': f.following.id,
            'username': f.following.username,
        })

    return JsonResponse({'following': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_user(request):
    try:
        current_user = request.user
        category_user = CategoryUsers.objects.all()
        data = []
        for user in category_user:
            img = ''
            
            if user.id != current_user.id:
                if user.role == 'user':
                    try:
                        user_detail = UserDetail.objects.get(business=user) 
                        try:
                            img = user_detail.profile_image.url
                        except:
                            img = ''
                    except:
                        img = ''
                if user.role == 'business' :
                    try:
                        business_detail = Businessdetail.objects.get(business=user) 
                        image = business_detail.business_image.get()  
                        img = image.image.url
                    except:
                        img = ''

                data.append({
                    'id': user.id,
                    'username': user.name,
                    'image' : img ,
                    'role' : user.role
                })

        return JsonResponse({'user': data})
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_notification_all(request,slug = None):
    user = request.user

    try:
        if slug:
            notifications = NotificationMassage.objects.filter(user = user)
            for notification in notifications:
                if notification.id == int(slug):
                    return JsonResponse({ "id": notification.id, "notification" : notification.notification, "created_date" : notification.created_at, "updated_date": notification.updated_at }, safe=False, status=200)

        else: 
            notifications = NotificationMassage.objects.filter(user = user)
            all_notification = []
            for notification in notifications:
                all_notification.append(
                    {
                        "id": notification.id,
                        "notification" : notification.notification,
                        "created_date" : notification.created_at,
                        "updated_date": notification.updated_at

                    }
                    )
            return JsonResponse(all_notification, safe=False, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_time(request):
    
    user = request.user
    try:
        data = []
        times = UserSession.objects.filter(user=user)
        for time in times:
            data.append({
                "id": time.id,
                "user_id": time.user_id,
                "duration": str(time.duration),
                "created_at": time.timestamp,

            })
        
        return JsonResponse(data, safe=False, status=200)
    except:
        return JsonResponse({'error': 'Error'}, status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Anyone can scan the QR
def get_total_refferial(request):
    user = request.user
    code = user.referral_code

    refferials = refferial_code.objects.filter(refferial_code = code)
    data = []
    for refferial in refferials:
        data.append( {
            "email" : refferial.user_email,
            "refferial_code" : refferial.refferial_code,
        })
    return JsonResponse(data, safe=False, status=200)

