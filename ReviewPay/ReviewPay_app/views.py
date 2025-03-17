import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

# PayPal Token Generate Karna
@api_view(['GET'])
def get_paypal_token(request):
    """ PayPal ke liye Access Token Generate karna """
    url = f"{settings.PAYPAL_API_URL}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, headers=headers, data=data, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET))

    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({"error": "Failed to get token"}, status=400)


#Payment Create Karna
@api_view(['POST'])
def create_payment(request):
    """ Payment Create Karna PayPal ke through """
    token = request.data.get("token")  # Postman se token bhejna hoga
    amount = request.data.get("amount", "10.00")  # Default amount 10 USD

    url = f"{settings.PAYPAL_API_URL}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": amount
                }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return Response(response.json())
    else:
        return Response({"error": "Failed to create payment"}, status=400)


# Payment Capture Karna (Customer se paisay lena)
@api_view(['POST'])
def capture_payment(request):
    """ PayPal se Paisay Confirm aur Capture karna """
    token = request.data.get("token") 
    order_id = request.data.get("order_id") 

    url = f"{settings.PAYPAL_API_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, headers=headers)

    if response.status_code == 201:
        return Response(response.json())
    else:
        return Response({"error": "Failed to capture payment"}, status=400)


# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate, login,logout
# from django.contrib.auth.decorators import login_required
# User = get_user_model()  # Get the custom user model

# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('name')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 == password2:
#             try:
#                 user = User.objects.create_user(username=username, email=email, password=password1)  # Set to False for admin approval
#                 user.save()
#                 return redirect('login')  
#             except Exception as e:
#                 messages.error(request, f'Error creating account: {str(e)}')
#         else:
#             messages.error(request, 'Passwords do not match.')
    
#     return render(request, 'signup.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['name']
#         password = request.POST['password']
        
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  # Built-in Django login function
#             return redirect('home')  # Redirect to home or another page
          
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'login.html')

# def logout_view(request):
#     request.session.flush()
#     logout(request)  # This will clear the session
#     return redirect('login')  # Redirect to login page after logout


# @login_required
# def home(request):
#     return render(request, 'home.html')

