import json
import threading
import time
import base64
import os
from decimal import Decimal
from uuid import uuid4

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
from .models import CategoryUsers, Businessdetail, Employee, Product
from .models import UserDetail, Feedback, Barcode, ProductImage
from .models import BusinessVerifications,CommingsoonLogin, Welcome_new_user
from .models import BusinessLogo, BusinessVideo, BusinessImage, OrderTracking
from .models import ReviewCashback,ReferralCashback, UserCashBack,Notifications
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
                'category': business_data.get("category"),
                'sub_category': business_data.get("subCategory"),
                'abn_number': business_data.get("abnNumber"),
                'business_name': business_data.get("businessName"),
                'business_address': business_data.get("businessAddress"),
            }
        )

        # Get multiple images
        business_logos = request.FILES.getlist("businessLogo")
        
        for business_logo in business_logos:
            file_extension = os.path.splitext(business_logo.name)[1]  
            new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  
            business_logo.name = new_file_name  

            # Correctly link to `Businessdetail` instance
            BusinessLogo.objects.create(business=business_detail, image=business_logo)
        
        ReviewCashback.objects.update_or_create(business=business_detail)
        ReferralCashback.objects.update_or_create(business=business_detail)
        
        message = 'Business data added successfully.' if created else 'Business data updated successfully.'
        try:
            notification = Notifications.objects.get(user_id=user)
            notification.business_detail = 'success'
            notification.business_detail_date = date.today()
            notification.save()
        except:
            return JsonResponse({'message': 'notification error'}, status=400)

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
            
            image = request.FILES.get('image')
            file_extension = os.path.splitext(image.name)[1]  # Get file extension (e.g., .jpg, .png)
            new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  # Username + UUID + extension
            image.name = new_file_name  # Assign the new name
            # Check if required data is present

            user_detail, created = UserDetail.objects.update_or_create(
                                    business = user,
                                    defaults = {
                                     'first_name' : request.POST.get('first_name'),
                                     'last_name' : request.POST.get('last_name'),
                                     'email' : request.POST.get('email'),
                                     'gender' : request.POST.get('gender'),
                                     'phone_number' : request.POST.get('phone_number'),
                                     'post_code' : request.POST.get('post_code'),
                                     'date_of_birth' : datetime.strptime(request.POST.get('date_of_birth'), '%d-%m-%Y').date(),                                     
                                     'profile_image' : image
                                    })
        
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
                'openning_hours': business_data.get("openning_hours"),
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

        # Get multiple videos from request
        videos = request.FILES.getlist('video')
        images = request.FILES.getlist('image')

        if not videos:
            return JsonResponse({'error': 'No videos uploaded.'}, status=400)

        if not images:
            return JsonResponse({'error': 'No images uploaded.'}, status=400)

        for video in videos:
            # Generate unique filename
            file_extension = os.path.splitext(video.name)[1]  
            new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  
            video.name = new_file_name  

            # Save to database
            business_video = BusinessVideo.objects.create(business=business_detail, video=video)
          
        for image in images:
            # Generate unique filename
            file_extension = os.path.splitext(video.name)[1]  
            new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  
            video.name = new_file_name  

            # Save to database
            business_images = BusinessImage.objects.create(business=business_detail, image=image)
        try:
            notification = Notifications.objects.get(user_id=user)
            notification.product_image = 'success'
            notification.product_image_date = date.today()
            notification.save()
        except:
            return Response({'message': 'Notification Error'}, status=400)
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