import json, requests, re
import threading
import time
import base64
import os
import uuid
from decimal import Decimal
from datetime import timedelta
from uuid import uuid4
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from datetime import date
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
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from google.cloud import vision
import os
from .models import CategoryUsers, Businessdetail, Employee, Product, Product_business_invoice
from .models import UserDetail, Feedback, Barcode, ProductImage, favorate_business, Follow, industry_question
from .models import BusinessVerifications,CommingsoonLogin, Welcome_new_user, ProductClientReview
from .models import BusinessLogo, BusinessVideo, BusinessImage, OrderTracking,NotificationMassage
from .models import ReviewCashback,ReferralCashback, UserCashBack,Notifications, UserSession, refferial_code
User = get_user_model()  # Get the custom user model


def image_decode(image):
    format, imgstr = image.split(';base64,')  # 'data:image/png;base64,...'
    ext = format.split('/')[-1]  # File ka extension (png/jpg)
    image = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
    return image

def businessImages(user, businessImages):
    for businessimages in businessImages:
        if businessimages != '':
            business_images = image_decode(businessimages)
        else:
            business_images = ''
        businessImages.objects.create(business = user,business_images = business_images)

# Restful signup api
@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_signup(request):
    if request.method == 'POST':
        # Fetch data from the form
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        role = request.POST.get('role')
        referral_code = request.POST.get('referral_code')

        if not re.search(r'[A-Z]', password):
            return JsonResponse({ "error": "Password must contain at least one uppercase letter." }, status=400)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return JsonResponse({ "error":"Password must contain at least one special character."}, status=400)
        # Validation for required fields
        if not name or not email or not password:
            return JsonResponse({'error': 'Username, email, and password are required'}, status=400)

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Role validation
        if role == 'user' or role == 'business':
            try:
                # Create user
                user = CategoryUsers.objects.create_user(
                    username=email, 
                    name=name, 
                    email=email,
                    password=password, 
                    role=role
                )
                user.save()
                if role == 'business':
                    Notifications.objects.create(user_id=user)
             
                if referral_code:
                 
                    referral = refferial_code.objects.create(
                        user_email = email,
                        refferial_code = referral_code
                                                            )
                    referral.save()
                return JsonResponse({'message': 'User added successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': 'Email already exists'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid role. Must be "user" or "business"'}, status=400)
      
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('email')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in (creates a session)
            try:
                data = Welcome_new_user.objects.get(email=username) 
                massage = 'None'
            except:
               Welcome_new_user.objects.create(
                   user = user,
                   email = username
               )
               massage = 'Nice to meet you, Dear! Your ReviewPay journey starts now – explore, connect, and get the best!'
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return JsonResponse({
                'message': 'Login successful!',
                'role': user.role,
                'access_token': access_token,
                'refresh_token': str(refresh),
                'notification' : massage
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Password Reset Request View
class PasswordResetRequestView(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
    
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                token = default_token_generator.make_token(user)
                reset_url =f'https://reviewpay.com.au/SavePassword/{uid}/{token}/' 
            
                # Send Email
                subject = 'Password Reset Request'
                message = f'Click the link below to reset your password:\n{reset_url}'
                send_mail(subject, message, 'ahmadelectricaltraders@gmail.com', [email])
                return JsonResponse({'message': 'Password reset link has been sent to your email.'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist.'}, status=400)

# Reset Password View
class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
          
            if default_token_generator.check_token(user, token):
                new_password = request.data.get('password')
                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password has been reset successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid or expired token.'},status=400)
        except (User.DoesNotExist, ValueError):
            return JsonResponse({'error': 'Invalid request.'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_business_detail(request):
    user = request.user
    try:
        business_data = request.POST

        if not business_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)

        # Ensure `Businessdetail` instance is assigned
        business_detail, created = Businessdetail.objects.update_or_create(
            business=user,  # Check by `business` field (OneToOne relation)
            defaults={
                'description' : business_data.get('description'),
                'category': business_data.get("category"),
                'sub_category': business_data.get("subCategory"),
                'abn_number': business_data.get("abnNumber"),
                'business_name': business_data.get("businessName"),
                'business_address': business_data.get("businessAddress"),
            }
        )
        # Get multiple images
        try:
            business_logo = request.FILES.get("businessLogo")
        except:
            return JsonResponse({'error': 'Business logo is not define.'}, status=400)
        try:
            video_images = request.FILES.get("video_images")
        except:
            return JsonResponse({'error': 'Video is not define.'}, status=400)
        
        
        business_logo, created = BusinessLogo.objects.update_or_create(business=business_detail, defaults= {'image' : business_logo})

        # Correctly link to `Businessdetail` instance
        business_video, created = BusinessVideo.objects.update_or_create(business = business_detail,defaults = {'video' :video_images})

        ReviewCashback.objects.update_or_create(business=business_detail)
        ReferralCashback.objects.update_or_create(business=business_detail)
        
        message = 'Business data added successfully.' if created else 'Business data updated successfully.'
        
        try:
            notification = Notifications.objects.get(user_id=user)
            notification.business_detail = 'success'
            notification.business_detail_date = date.today()
            notification.save()
        except:
            pass
            # return JsonResponse({'message': 'notification error'}, status=400)

        return JsonResponse({'message': message}, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employee_detail(request):
    user = request.user
    try:
        # Parse the incoming JSON data
        employee_data = request.POST
        employee_profiles = request.FILES.get("employee_profiles")
        file_extension = os.path.splitext(employee_profiles.name)[1]  # Get file extension (e.g., .jpg, .png)
        new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  # Username + UUID + extension
        employee_profiles.name = new_file_name  # Assign the new name
        # Check if required data is present
        if not employee_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)
        
        employee = Employee(
            business=user,
            employee_name = employee_data.get('employee_name'),
            identification_number = employee_data.get('identification_number'),
            working_since = employee_data.get('working_since'),
            designation = employee_data['designation'],
            employee_email_address = employee_data.get('employee_email_address'),
            employee_profiles = employee_profiles
                            )

        employee.save()
        return JsonResponse({'message': 'Employee data added successfully.'}, status=200)
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product(request):
    try:
        # Extract form data
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description', '')
        # Validate required fields
        if not product_name or not product_price:
            return JsonResponse({'error': 'Name and Price are required'}, status=400)

        # Create the Product
        product = Product.objects.create(
            business=request.user,
            product_name=product_name,
            product_price=product_price,
            product_description=product_description
        )

        # Handle barcodes (if provided)
        barcodes = request.POST.getlist('barcode_images', [])
        for barcode in barcodes:
            Barcode.objects.create(product=product, barcode_value=image_decode(barcode))

        # Handle product images (if provided)
        product_images = request.FILES.getlist('product_images')
        for image in product_images:
            ProductImage.objects.create(product=product, image=image)

        return JsonResponse({'message': 'Product created successfully', 'product_id': product.id}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    if 'user' == request.user.role:

        try:
            try:
                color = request.POST.get('bg_color')
            except:
                color = ''
            image = request.FILES.get('image')
            file_extension = os.path.splitext(image.name)[1]  # Get file extension (e.g., .jpg, .png)
            new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  # Username + UUID + extension
            image.name = new_file_name  # Assign the new name

            # Step 1: Call PhotoRoom API to remove/change background
            photoroom_url = "https://sdk.photoroom.com/v1/segment"
            headers = {
                'Accept': 'image/png, application/json',
                'x-api-key': 'sandbox_f7771a44dacbb0f51885ae7c40fa6c17b02d6e0c'
            }
            payload = {
            }
            files = [
                ('image_file', (image.name, image.read(), 'application/octet-stream'))
            ]
            response_1 = requests.post(photoroom_url, headers=headers, data=payload, files=files)
            # try:
            #     color = request.POST.get('bg_color')
            # except:
            #     color = ''
            # if color != '':
            #     payload['bg_color'] = color
            # response = requests.post(photoroom_url, headers=headers, data=payload, files=files)
    
            if 'image/png' not in response_1.headers.get('Content-Type', ''):
                return JsonResponse({'error': 'PhotoRoom API failed.', 'details': response_1.text}, status=500)
            
            # if 'image/png' not in response.headers.get('Content-Type', ''):
            #     return JsonResponse({'error': 'PhotoRoom API failed.', 'details': response.text}, status=500)  
                   
            # Step 2: Save the returned image (as profile_image)
            output_image = ContentFile(response_1.content, name=new_file_name)
            # output_image_1 = ContentFile(response.content, name=new_file_name)

            # Step 3: Update or create user detail
            user_detail, created = UserDetail.objects.update_or_create(
                business=user,
                defaults={
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'email': request.POST.get('email'),
                    'gender': request.POST.get('gender'),
                    'phone_number': request.POST.get('phone_number'),
                    'post_code': request.POST.get('post_code'),
                    'date_of_birth': datetime.strptime(request.POST.get('date_of_birth'), '%d-%m-%Y').date(),
                    'profile_image': output_image,
                    'profile_image_color': color
                }
            )

            if created:
                message = 'User Detail data added successfully.'
            else:
                message = 'User Detail data updated successfully.'

            return JsonResponse({'message': message}, status=200)
        
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
      return JsonResponse({'error': 'The role is not of a user.'}, status=400)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feedback(request):
    user = request.user
    try:
        data = json.loads(request.body)
        feedback = Feedback.objects.create(business = user,
                                           issue_category = data['issue_category'],
                                           issue_description = data['feedback_description'],
                                           urgency_level = data['urgency_level']
                                           )
        return JsonResponse({'message': 'feedback add successfully.'}, status=200)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def business_verifications(request):
    user = request.user
    try:
        # Get JSON data and files
        business_data = request.data  # Use request.data to handle both form data and files
        files = request.FILES
        # Check if required data is present
        if not business_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)

        # Extract file fields if present
        government_issue_document = files.get('government_issue_document')  # Handle uploaded file
        business_name_evidence = files.get('business_name_evidence')
        company_extract_issue = files.get('company_extract_issue')

        # Check if Businessdetail exists for the user; update or create accordingly
        business_detail, created = BusinessVerifications.objects.update_or_create(
            business=user,  # Check by the `business` field (OneToOne relation)

            defaults={
                'ACN': business_data.get("acn"),
                'business_web': business_data.get("business_web"),
                'fullname_director_1': business_data.get("fullname_director_1"),
                'fullname_director_2': business_data.get("fullname_director_2"),
                'admin_phone_number': business_data.get("admin_phone_number"),
                'business_phone_number': business_data.get("business_phone_number"),
                'facebook_link': business_data.get("facebook_link"),
                'instra_link': business_data.get("instragram_link"),
                'admin_email': business_data.get("admin_email"),
                'client_email': business_data.get("client_email"),
                'monday_from': business_data.get("monday_from"),
                'monday_to': business_data.get("monday_to"),
                'tuesday_from': business_data.get("tuesday_from"),
                'tuesday_to': business_data.get("tuesday_to"),
                'wednesday_from': business_data.get("wednesday_from"),
                'wednesday_to': business_data.get("wednesday_to"),
                'thursday_from': business_data.get("thursday_from"),
                'thursday_to': business_data.get("thursday_to"),
                'friday_from': business_data.get("friday_from"),
                'friday_to': business_data.get("friday_to"),
                'saturday_from': business_data.get("saturday_from"),
                'saturday_to': business_data.get("saturday_to"),
                'sunday_from': business_data.get("sunday_from"),
                'sunday_to': business_data.get("sunday_to"),
                'government_issue_document': government_issue_document,
                'business_name_evidence': business_name_evidence,
                'company_extract_issue': company_extract_issue,
            }
        )

        if created:
            message = 'Business verifications data added successfully.'
        else:
            message = 'Business verifications data updated successfully.'

        try:
            notification = Notifications.objects.get(user_id=user)
            notification.business_verify = 'success'
            notification.business_verify_date = date.today()
            notification.save()
        except:
            return JsonResponse({'message': 'notification error'}, status=400)
        
        return JsonResponse({'message': message}, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def commingsoon(request):
    if request.method == 'POST':
        # Fetch data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Validation for required fields
        if not name or not email or not phone_number:
            return JsonResponse({'error': 'Username, email, and password are required'}, status=400)

        # Role validation
        if email:
            try:
                # Create user
                user = CommingsoonLogin.objects.create(name = name, email = email,phone_number = phone_number)
                user.save()
                return JsonResponse({'message': 'User added successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': 'Email already exists'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid role. Must be "user" or "business"'}, status=400)
      
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_business_video_and_image(request):
    user = request.user

    try:
        # Ensure business detail exists for the user
        business_detail = Businessdetail.objects.filter(business=user).first()
        if not business_detail:
            return JsonResponse({'error': 'Business detail not found for this user.'}, status=404)

        
        
        videos_and_image = request.FILES.getlist('video_and_image')
        business_logo = request.FILES.get('business_logo')

        if business_logo:
            file_extension = os.path.splitext(business_logo.name)[1]  
            new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  
            business_logo.name = new_file_name
            obj, created = BusinessLogo.objects.update_or_create(
                business = business_detail,
                defaults={'business_logo': business_logo}
                )
            print("updated logo")


        if not videos_and_image:
            return JsonResponse({'error': 'No videos or images uploaded.'}, status=400)

        for video in videos_and_image:
            # Generate unique filename
            
            if video.content_type == 'video/mp4':
                file_extension = os.path.splitext(video.name)[1]  
                new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  
                video.name = new_file_name
                # Save to database
                business_video = BusinessVideo.objects.create(business=business_detail, video=video)
                # Save to database
            if video.content_type in ['image/png', 'image/jpeg', 'image/svg+xml']:
                file_extension = os.path.splitext(video.name)[1]  
                new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  
                video.name = new_file_name  
                # Save to database
                business_image = BusinessImage.objects.create(business=business_detail, image=video)
                

        
        return Response({'message': 'Videos and images uploaded successfully.'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review_cashback(request):
    user = request.user

    try:
        # Get the business instance
        business = Businessdetail.objects.get(business=user)
        
        # Get data from the request
        review_amount_cashback_percent = request.data.get("review_amount_cashback_percent")
        review_amount_cashback_fixed = request.data.get("review_amount_cashback_fixed")
        review_cashback_return_refund_period = request.data.get("review_cashback_return_refund_period")
        review_cashback_expiry = request.data.get("review_cashback_expiry")

        # Create or update the ReviewCashback record
        review_cashback, created = ReviewCashback.objects.update_or_create(
            business=business,  # linking to the business
            defaults={
                'review_amount_cashback_percent': review_amount_cashback_percent,
                'review_amount_cashback_fixed': review_amount_cashback_fixed,
                'review_cashback_return_refund_period': review_cashback_return_refund_period,
                'review_cashback_expiry': review_cashback_expiry
            }
        )

        if created:
            message = 'Review Cashback Settings created successfully.'
        else:
            message = 'Review Cashback Settings updated successfully.'

        return JsonResponse({'message': message}, status=200)

    except Businessdetail.DoesNotExist:
        return JsonResponse({'error': 'Business not found.'}, status=404)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_referral_cashback(request):
    user = request.user

    try:
        # Get the business instance
        business = Businessdetail.objects.get(business=user)

        # Get data from the request
        referral_cashback_enabled = request.data.get("referral_cashback_enabled")
        referral_amount_cashback_percent = request.data.get("referral_amount_cashback_percent")
        referral_amount_cashback_fixed = request.data.get("referral_amount_cashback_fixed")
        referral_cashback_return_refund_period = request.data.get("referral_cashback_return_refund_period")
        referral_cashback_expiry = request.data.get("referral_cashback_expiry")

        # Create or update the ReferralCashback record
        referral_cashback, created = ReferralCashback.objects.update_or_create(
            business=business,  # linking to the business
            defaults={
                'referral_cashback_enabled': referral_cashback_enabled,
                'referral_amount_cashback_percent': referral_amount_cashback_percent,
                'referral_amount_cashback_fixed': referral_amount_cashback_fixed,
                'referral_cashback_return_refund_period': referral_cashback_return_refund_period,
                'referral_cashback_expiry': referral_cashback_expiry
            }
        )

        if created:
            message = 'Referral Cashback Settings created successfully.'
        else:
            message = 'Referral Cashback Settings updated successfully.'

        return JsonResponse({'message': message}, status=200)

    except Businessdetail.DoesNotExist:
        return JsonResponse({'error': 'Business not found.'}, status=404)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cashback(request):
    try:
        user = request.user
    
        data = json.loads(request.body)
        try:
            user_detail = UserDetail.objects.get(business=user)
        except:
            return JsonResponse({'error': 'User Detail not found.'}, status=404)
        business_detail = Businessdetail.objects.get(id=data.get('business_id'))
        cashback = business_detail.ReviewCashback.first()
        if cashback:
            cashback = cashback.review_amount_cashback_percent

        invoice_price = data.get('price')
        amount = (invoice_price/100) * cashback
        UserCashBack.objects.create(
            user=user_detail,
            business_id=business_detail.id,
            invoice_price=float(invoice_price),
            amount=float(amount)
        )
        return JsonResponse({'message': "invoce cashback created"}, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_ordertracking(request):
    if request.method == 'POST':
        try:
            marchant_api = request.headers.get("X-API-KEY")
            data = json.loads(request.body)
            try:
                business_detail = Businessdetail.objects.get(marchant_api_key = marchant_api)
            except:
                return JsonResponse({'error': 'marchant api key not found.'}, status=404)
            order = OrderTracking.objects.create(
                    marchant_api = marchant_api,
                    adv_sub = data.get("adv_sub"),
                    adv_sub2 = data.get("adv_sub2"),
                    adv_sub3 = data.get("adv_sub3"),
                    adv_sub4 = data.get("adv_sub4"),
                    adv_sub5 = data.get("adv_sub5"),
                    transaction_id = data.get("transaction_id"),
                    amount = data.get("amount"),
                    user_id = business_detail.id,
                    status = "Pending"
                )

            return JsonResponse({"message": "Order received successfully", "order_id": order.id}, status=200)

        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else :
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_validation(request):
    if request.method == 'POST':
        marchant_api = request.headers.get("X-API-KEY")
        data = json.loads(request.body)
        
        try:
            business_detail = Businessdetail.objects.get(marchant_api_key = marchant_api)
        except:
            return JsonResponse({'error': 'marchant api key not found.'}, status=404)
        orders = OrderTracking.objects.filter(transaction_id = 'AR6666')  
        pending_amount = 0

        for order in orders:
            pending_amount = pending_amount + orders[0].amount
     
        if Decimal(data["amount"]) == pending_amount:
          
            for order in orders:
                order.status = data["status"]
                order.save()
            return JsonResponse({'massage': 'The order has been updated to approved status.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        
        
@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dissmise_notification(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        notification = Notifications.objects.get(user_id=user)
        
        try:
            success_business = Businessdetail.objects.get(business=user)
            
            notification.business_detail = 'success'
            notification.business_detail_date = date.today()
            notification.save()
         
            image = success_business.business_image.all()
            if image:
                notification.product_image = 'success'
                notification.product_image_date = date.today()
                notification.save()
            else:
                image = ''
        except:
            success_business = ''
            image = ''

        try :
            verify = BusinessVerifications.objects.get(business= user)
            if verify:
                notification.business_verify = 'success'
                notification.business_verify_date = date.today()
                notification.save()
        except:
            verify = ''

        
        try:
            data["detail_business"]
        except:
            data["detail_business"] = None

        try:
            data["product_image"]
        except:
            data["product_image"] = None
        
        try:
            data["business_verify"]
        except:
            data["business_verify"] = None

        if data["detail_business"] == 'd' and success_business == '':
            notification.business_detail = 'delay'
            notification.business_detail_date = date.today()
            notification.save()

        if data["product_image"] == 'd' and image == '':
            notification.product_image = 'delay'
            notification.product_image_date = date.today()
            notification.save()
        
        if data["business_verify"] == 'd' and verify == '':
            
            notification.business_verify = 'delay'
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

def send_email_review(email,name):
    try:
        with open('/home/ubuntu/email_send/email_key.json', 'r') as file:
            data = json.load(file)
    except:
        with open('C:\\bravo\email_key.json', 'r') as file:
            data = json.load(file)   
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = data["key"]
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "feed back"
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    html_content = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Signature</title>
  <style>
    @font-face {{
      font-family: 'GeneralSansBold';
      src: url('path-to-font/GeneralSansBold.woff2') format('woff2');
    }}
    @font-face {{
      font-family: 'GeneralSansMedium';
      src: url('path-to-font/GeneralSansMedium.woff2') format('woff2');
    }}
    @font-face {{
      font-family: 'GeneralSansRegular';
      src: url('path-to-font/GeneralSansRegular.woff2') format('woff2');
    }}
    @font-face {{
      font-family: 'VerminViva';
      src: url('path-to-font/VerminViva.woff2') format('woff2');
    }}

    body {{
      margin: 0;
      padding: 0;
      font-family: 'GeneralSansRegular', sans-serif;
    }}

    .container {{
      width: 100%;
      max-width: 800px;
      margin: 0 auto;
    }}

    .banner-section {{
      height: 288px;
      width: 100%;
    }}

    .banner-image {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    .content-section {{
      width: 100%;
      background-color: #B7BDCA;
      padding: 32px;
      box-sizing: border-box;
    }}

    .heading {{
      font-family: 'GeneralSansBold', sans-serif;
      font-size: 30px;
      color: black;
      text-align: center;
      margin-bottom: 28px;
    }}

    .horizontal-line {{
      width: 100%;
      height: 2px;
      background-color: black;
      margin-bottom: 40px;
    }}

    .refer-text {{
      font-family: 'GeneralSansMedium', sans-serif;
      font-size: 30px;
      text-align: center;
      color: #0D182E;
      margin-bottom: 40px;
    }}

    .cashback-text {{
      text-align: center;
      font-family: 'GeneralSansMedium', sans-serif;
      color: #0D182E;
      margin-bottom: 40px;
      margin-top: 20px;
    }}

    .footer {{
      text-align: center;
    }}

    .logo-container {{
      display: flex;
      justify-content: center;
      margin-bottom: 16px;
    }}

    .company-logo {{
      height: 80px;
      width: auto;
    }}

    .company-name {{
      font-family: 'VerminViva', sans-serif;
      font-size: 24px;
      color: #0D182E;
      margin-bottom: 8px;
    }}

    .disclaimer {{
      font-family: 'GeneralSansRegular', sans-serif;
      color: black;
      text-align: center;
      margin-bottom: 16px;
    }}

    .social-icons {{
      display: flex;
      justify-content: center;
      gap: 16px;
      margin-bottom: 16px;
    }}

    .social-icon {{
      width: 20px;
      height: 20px;
    }}

    .address {{
      font-size: 14px;
      font-family: 'GeneralSansRegular', sans-serif;
      color: black;
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Banner Section -->
    <div class="banner-section">
      <img src="https://reviewpay.com.au/static/media/emailbanner.52ea48d6eff86503dfbb.jpeg" alt="Email Signature Header" class="banner-image">
    </div>

    <!-- Main Content Section -->
    <div class="content-section">
      <!-- Heading -->
      <h1 class="heading">Thank you Rita for your review!</h1>

      <!-- Horizontal Line -->
      <div class="horizontal-line"></div>

      <!-- Refer Now and Earn Text -->
      <h2 class="refer-text">Refer now and Earn</h2>

      <!-- Refer a Friend Text -->
      <p class="cashback-text">Refer a friend and earn 9% cash back</p>

      <div class="horizontal-line"></div>

      <!-- Footer -->
      <div class="footer">
        <!-- Company Logo -->
        <div class="logo-container">
          <img src="https://superadmin.reviewpay.com.au/static/img/logo_reviewpay_role.png" alt="Company Logo" class="company-logo">
        </div>

        <!-- Company Name -->
        <h2 class="company-name">Review Pay</h2>

        <p class="disclaimer">
          You are receiving this email because you opted in via our website.
        </p>

        <!-- Social Media Icons -->
        <div class="social-icons">
          <a href="#"><img src="https://superadmin.reviewpay.com.au/static/img/ii1.png"></a>
          <a href="#"><img src="https://superadmin.reviewpay.com.au/static/img/blushdesign).jpg"></a>
          <a href="#"><img src="https://superadmin.reviewpay.com.au/static/img/twitterlogo.png"></a>
          <a href="#"><img src="https://superadmin.reviewpay.com.au/static/img/insta.png"></a>
          <a href="#"><img src="https://superadmin.reviewpay.com.au/static/img/linkdin.jpg" alt="LinkedIn" class="social-icon"></a>
        </div>

        <!-- Company Address -->
        <p class="address">
          123 Review Street, Tech City, Innovation District 12345
        </p>
      </div>
    </div>
  </div>
</body>
</html>"""
    sender = {"name":"ahsan","email":"hello@reviewpay.com.au"}
    to = [{"email": email,"name": name}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return "sucess"
    except:
        return "false"



def send_email(email ,name ,phone ,client_id ,product_id,business_id):
    try:
        with open('/home/ubuntu/email_send/email_key.json', 'r') as file:
            data = json.load(file)
    except:
        with open('C:\\bravo\email_key.json', 'r') as file:
            data = json.load(file)   
            
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = data["key"]
    website_url = f"https://reviewpay.com.au/UserDashboard/BusinessPostReview?review_id={product_id}&business_id={business_id}"
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "Reviewpay product invoice"
    html_content = f"<html><body><h1>Thank you for your purchase!</h1><p>Dear Customer,</p>{website_url}<p></p> </body></html>"
    sender = {"name":"ahmad","email":"hello@reviewpay.com.au"}
    to = [{"email": email,"name": name}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return "sucess"
    except:
        return "false"


@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_businesses(request):
    try:
        user = request.user
        if user.role == 'user' :
            user = UserDetail.objects.get(business=user)
            business_id = request.POST.get('business_id')
            business = Businessdetail.objects.get(id=business_id)
        
            favorate_business.objects.create(
                user = user, business = business
            )
            return JsonResponse({'massage' : 'Business added to favorites successfully.'}, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Only users can favorite businesses.'}, status=403)
    
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_business_invoice(request):

    try:
        user = request.user
        
        if user.role == 'business' :
            data = request.POST
            user_simple = CategoryUsers.objects.get(email= data.get('client_email'))
            
            business = BusinessVerifications.objects.get(business= user)
            notification_business = CategoryUsers.objects.get(email=business.business) 
            if data.get('product_service') != '' and data.get('client_email') != '':
               
                product_service = data.get('product_service')
                invoice_amount = data.get('invoice_amount')
                invoice_number = data.get('invoice_number')
                reviewcashback = data.get('reviewcashback')
                refferial_code = data.get('refferial_code')
                client_name = data.get('client_name')
                client_phone = data.get('client_phone')
                client_email = data.get('client_email')
                product = Product_business_invoice.objects.create(
                    user = user_simple,
                    business = business,
                    product_service = product_service,
                    invoice_amount = invoice_amount,
                    invoice_number = invoice_number,
                    reviewcashback = reviewcashback,
                    refferial_code = refferial_code,
                    client_name = client_name,
                    client_phone = client_phone,
                    client_email = client_email
                )
                
                email_status = send_email(client_email,client_name,client_phone,user_simple.id,product.id,business.id)
                try:
                    notification =  NotificationMassage.objects.create(
                        user = user_simple,
                        notification = f"Got a minute? {notification_business.name} would love to hear your thoughts. Please complete their review form."
                    )
                except:
                    return JsonResponse({"massage":"Notification Error"}, status = 403)
                
                if email_status == "sucess":
                    return JsonResponse({"massage":f"create sucessfully invoice and send email {client_email}.","notification" : notification.notification}, status = 200)
                else:
                    return JsonResponse({"massage":"create sucessfully invoice and not send email."}, status = 403)
        else:
            return JsonResponse({'error': 'Only users can favorite businesses.'}, status=403)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_client_review(request):
    try:
        user = request.user
        data = request.POST
        user_simple = CategoryUsers.objects.get(id = user.id)
        product = Product_business_invoice.objects.get(id= data["review_id"]) 
        business = BusinessVerifications.objects.get(id= data["business_id"])
        notification_business = CategoryUsers.objects.get(email=business.business) 
        project_review_client = ProductClientReview.objects.create(
        product_id = product,
        user = user_simple,
        business = business,
        benefit_quality = int(data['benefit_quality']),
        benefit_performance = int(data['benefit_performance']),
        benefit_rate = int(data['benefit_rate']),
        benefit_training = int(data['benefit_training']),
        culture_expertise = int(data['culture_expertise']),
        culture_extra_care = int(data['culture_extra_care']),
        culture_responsiveness = int(data['culture_responsiveness']),
        culture_professionalism = int(data['culture_professionalism']),
        operator_business_support = int(data['operator_business_support']),
        operator_delivery = int(data['operator_delivery']),
        operator_offering = int(data['operator_offering']),
        hear_about_us = data['hear_about_us'],
        experience = data['experience']
        )
        if project_review_client:
            product.status = "approve" 
            product.save
            email_status = send_email_review(user.username,user.name)
            try:
                notification =  NotificationMassage.objects.create(
                    user = notification_business,
                    notification = f"Great news! {user.name} has submitted their review for your business."
                )
            except:
                return JsonResponse({"massage":"Notification Error"}, status = 403)

            if email_status == "sucess":
                return JsonResponse({"massage":f"create sucessfully invoice and send email {user.name}.","notification_id": notification.id,"notification":notification.notification,"created_date" : notification.created_at, "updated_date": notification.updated_at}, status = 200)
            else:
                return JsonResponse({"massage":"create sucessfully invoice and not send email."}, status = 403)
            
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    user = request.user
    try:
        data = request.POST
        user_id_to_follow = data['user_id']
        
        try:
            user_to_follow = User.objects.get(id=user_id_to_follow)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        follow_relation = Follow.objects.filter(follower=user, following=user_to_follow)

        if follow_relation.exists():
            follow_relation.delete()
            return JsonResponse({'message': f'Unfollowed {user_to_follow.username}'})
        else:
            
            follow_user = Follow.objects.filter(follower = user_to_follow, following = user)

            if follow_user :
                massage = f"{user_to_follow.name} has followed you back"
            else :
                massage = f"{user_to_follow.name} has starting following you"

            notification =  NotificationMassage.objects.create(
                user = user_to_follow,
                notification = massage
            )
            Follow.objects.create(follower=user, following=user_to_follow)

            return JsonResponse({'message': f'Now following {user_to_follow.username}',"follow massage" : massage})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_massagenotification(request):
    user = request.user
    data = request.POST
    try:
        notification =  NotificationMassage.objects.create(
                user = user,
                notification = data["notification"]
        )
        return JsonResponse({"massage":f"create sucessfully.","notification_id" : notification.id}, status = 200)
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_user_time(request):
    user = request.user
    try:
        duration_str = request.data.get('duration')

        if duration_str is None:
            return Response({'error': 'Duration is required. Format: HH:MM:SS'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            hours, minutes, seconds = map(int, duration_str.split(':'))
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            return Response({"error": "Invalid duration format. Use HH:MM:SS"}, status=status.HTTP_400_BAD_REQUEST)

        entry, created = UserSession.objects.update_or_create(user=request.user, defaults={'duration': duration if duration else timedelta(0)}  )
        return Response({'message': 'Session time saved successfully.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def referral_referrel_request(request):
    user = request.user
    data = request.POST
    business_id = data.get('business_id')
    try:
        if user.role == 'user':
            code = user.referral_code
            url = f"https://reviewpay.com.au/UserDashboard/BusinessCategories?code={code}&business_id={business_id}"
            return JsonResponse({'refferal_url': url}, status=200)
        else:
            return JsonResponse({'error': 'You are not a user'}, status=400)
        
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sharereferral_code(request):
    user = request.user
    data = request.POST
    email =  data.get('email') 
    try:
        if user.role == 'user':
            code = user.referral_code
            share_user = CategoryUsers.objects.get(email = email)

            massage = f"Hi {share_user.name}, {user.name} has sent you a referral code for the business. \n\n referral code : {code}"
            if share_user:
                notification =  NotificationMassage.objects.create(
                user = share_user,
                notification = massage
                )
                return JsonResponse({'message': 'Referral code shared successfully.'}, status=200)
           
    except:
        return JsonResponse({'error': 'You are not a user'}, status=400)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def visionapi(request):
    try:
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image uploaded'}, status=400)

        # Service key path
        key_path = '/home/ubuntu/reviewplay_app/ReviewPay/service_keys/vision-key.json'
        if not os.path.exists(key_path):  # if running on Windows
            key_path = 'C:\\ReviewPlayRole\\ReviewPay\\service_keys\\vision-key.json'

        # Pass the file path directly (not loaded json)
        client = vision.ImageAnnotatorClient.from_service_account_file(key_path)

        # Process the image
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]

        return Response({'labels': labels})

    except Exception as e:
        return Response({'error': str(e)}, status=500)