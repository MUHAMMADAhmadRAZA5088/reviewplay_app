import json
import threading
import time
import base64
import os
from uuid import uuid4

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
from .models import BusinessVerifications,CommingsoonLogin

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
        UploadedImages.objects.create(business = user,business_images = business_images)

# Restful signup api
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CategoryUsers

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

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return JsonResponse({
                'message': 'Login successful!',
                'role': user.role,
                'access_token': access_token,
                'refresh_token': str(refresh)
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
        # Parse the incoming JSON data
        business_data = request.POST
        # Check if required data is present
        if not business_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)

        business_logo = request.FILES.get("businessLogo")
        file_extension = os.path.splitext(business_logo.name)[1]  # Get file extension (e.g., .jpg, .png)
        new_file_name = f"{user.id}_{uuid4().hex}{file_extension}"  # Username + UUID + extension
        business_logo.name = new_file_name  # Assign the new name

        business_detail, created = Businessdetail.objects.update_or_create(
            business=user,  # Check by the `business` field (OneToOne relation)
            defaults={
                'businessLogo': business_logo,
                'category': business_data.get("category"),
                'sub_category': business_data.get("subCategory"),
                'abn_number': business_data.get("abnNumber"),
                'business_name': business_data.get("businessName"),
                'business_address': business_data.get("businessAddress"),
            }
        )

        if created:
            message = 'Business data added successfully.'
        else:
            message = 'Business data updated successfully.'

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
                                     'gender' : request.POST.get('gender'),
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
