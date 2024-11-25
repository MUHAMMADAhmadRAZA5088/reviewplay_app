import json
import base64
import os
import uuid

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import CategoryUsers, Employee, Product, UploadedImages
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
        if role == 'business':
            business_detail = user_data['businessDetails']
            business_name = business_detail["businessName"]
            business_address = business_detail["businessAddress"]
            abn_number = business_detail["abnNumber"]
            category = business_detail["category"]
            sub_category = business_detail["subCategory"]
            businessLogo = image_decode(business_detail["businessLogo"])
        elif role == 'custom':
            # If role is "custom", ensure these fields are cleared
            category = ''
            sub_category = ''
            abn_number = ''
            business_name = ''
            business_address = ''
            businessLogo = ''
        else:
            return JsonResponse({'error': 'Invalid role User'}, status=400)


        # Save the user instance

        try:
            user = CategoryUsers.objects.create_user(username=email, name=name, email=email, password=password, role=role, category=category, sub_category=sub_category, abn_number=abn_number, business_name=business_name, business_address=business_address, businessLogo=businessLogo)
            if role == 'business':
                user.save()
                if  user_data['employees'] :
                    employ(user, user_data['employees'])
               
                if  user_data['products'] :
                    Product_Data(user,  user_data['products'])

                if user_data['uploadedImages']['businessImages']:
                    businessImages(user,user_data['uploadedImages']['businessImages'])

                return JsonResponse({'message': 'Business User add Successfully'}, status=201)
            elif role == 'custom':
                user.save()
                return JsonResponse({'message': 'Custom User add Successfully'}, status=201)
            else :
                return JsonResponse({'error': 'Invalid role User'}, status=400)
        except:
            return JsonResponse({'error': 'User is already register'}, status=400)
    else:
        return JsonResponse({'error': 'Enter all fields again.'}, status=400)
#----------------------------------------------------------------------------------------------------

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

