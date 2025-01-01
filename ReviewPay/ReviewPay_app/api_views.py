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
from .models import CategoryUsers, Businessdetail, Employee, Product
# from .models import CategoryUsers, Employee, Product, UploadedImages

User = get_user_model()  # Get the custom user model


def image_decode(image):
    format, imgstr = image.split(';base64,')  # 'data:image/png;base64,...'
    ext = format.split('/')[-1]  # File ka extension (png/jpg)
    image = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
    return image

def employ(user, data_employee):
    for employee_data in data_employee:
        
        business = user
        employee_name = employee_data['employeeName']
        identification_number = employee_data['identificationNumber']
        designation = employee_data['designation']
        employee_email_address = employee_data['employeeEmailAddress']
        if employee_data['profilePic'] != '':
            employee_profiles = image_decode(employee_data['profilePic'])
        else:
            employee_profiles = ''
        Employee.objects.create(
                business=business,
                employee_name=employee_name,
                identification_number=identification_number,
                designation=designation,
                employee_email_address=employee_email_address,
                employee_profiles=employee_profiles
            )

def Product_Data(user, data_product):
    for product_data in data_product:
        if product_data['productImage'] != '':
            product_image = image_decode(product_data['productImage'])
        else:
            product_image = ''
        Product.objects.create(business = user,product_name = product_data['productName'],product_description = product_data['productDescription'],product_price = product_data['productPrice'],product_images = product_image)

def businessImages(user, businessImages):
    for businessimages in businessImages:
        if businessimages != '':
            business_images = image_decode(businessimages)
        else:
            business_images = ''
        UploadedImages.objects.create(business = user,business_images = business_images)

# Restful signup api
@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_signup(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)
        data = user_data['createAccount']
        name = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirmPassword']
        role = data.get('role')
        
        if bool(name) == False or bool(email)== False or bool(password) == False :
            return JsonResponse({'error': 'username,email and password is required'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        # Check if the role is "business"
 
        # Check if the role is "user"
        if role == 'user' or role == 'business':
            try:
                user = CategoryUsers.objects.create_user(
                                    username=email, name=name, email=email,
                                    password=password, role=role
                                                        )
                user.save
                return JsonResponse({'message': 'User add Successfully'}, status=201)
            except:
                return JsonResponse({'error': 'Email already exists'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid role User'}, status=400)
      
    else:
        return JsonResponse({'error': 'Enter all fields again.'}, status=400)

# Restful api login api
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
                'message': 'Login successfull!',
                'role' : user.role,
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Password Reset Request View
class PasswordResetRequestView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        email = body.get('email')
       
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            token = default_token_generator.make_token(user)
            reset_url = f'http://localhost:3000/reset-password/{uid}/{token}/'  # React frontend URL
           
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
        business_data = json.loads(request.body)

        # Check if required data is present
        if not business_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)

        # Check if Businessdetail exists for the user; update or create accordingly
        business_detail, created = Businessdetail.objects.update_or_create(
            business=user,  # Check by the `business` field (OneToOne relation)
            defaults={
                'businessLogo': business_data.get("businessLogo"),
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
        employee_data = json.loads(request.body)
        # Check if required data is present
        if not employee_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)
        
        employee = Employee(business=user,
                            employee_name = employee_data['employee_name'],
                            identification_number = employee_data['identification_number'],
                            designation = employee_data['designation'],
                            employee_email_address = employee_data['employee_email_address'],
                            employee_profiles = employee_data['employee_profiles']
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
    user = request.user
    try:
        # Parse the incoming JSON data
        product_data = json.loads(request.body)
        # Check if required data is present
        if not product_data:
            return JsonResponse({'error': 'Invalid data.'}, status=400)
        
        product = Product(  
                            business=user,
                            product_name = product_data['product_name'],
                            product_description = product_data['product_description'],
                            product_price = product_data['product_price'],
                            product_images = product_data['product_images']
                            )

        product.save()
        return JsonResponse({'message': 'Product data added successfully.'}, status=200)
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        