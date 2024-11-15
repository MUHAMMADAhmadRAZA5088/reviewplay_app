
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

User = get_user_model()  # Get the custom user model


@csrf_exempt  # Exempt CSRF for Postman testing; remove this in production
def api_signup(request):
    if request.method == 'POST':
        data = request.POST
        
        name = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        role = data.get('role')
        
        if bool(name) == False or bool(email)== False or bool(password) == False :
            return JsonResponse({'error': 'username,email and password is required'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Check if the role is "business"
        if role == 'business':
            category = data.get('category')
            sub_category = data.get('sub_category')
            abn_number = data.get('abn_number')
            business_name = data.get('business_name')
            business_address = data.get('business_address')
        elif role == 'custom':
            # If role is "custom", ensure these fields are cleared
            category = ''
            sub_category = ''
            abn_number = ''
            business_name = ''
            business_address = ''
        else:
            return JsonResponse({'error': 'Invalid role User'}, status=400)
        profile_picture = None
        if request.FILES.get('profile_picture'):
            profile_picture = request.FILES.get('profile_picture')

        # Save the user instance

        try:
            user = User.objects.create_user(username=email,name=name ,email=email, password=password,role=role,category=category,sub_category=sub_category,abn_number=abn_number,business_name=business_name,business_address=business_address,profile_picture=profile_picture)
            if role == 'business':
                user.save()
                return JsonResponse({'message': 'Business User add Successfully'}, status=201)
            elif role == 'custom':
                user.save()
                return JsonResponse({'message': 'Custom User add Successfully'}, status=201)
        
        except:
            return JsonResponse({'error': 'User is already register'}, status=400)
    else:
        return JsonResponse({'error': 'Enter all fields again.'}, status=400)
#------------------------------------

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
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=200)
           
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

