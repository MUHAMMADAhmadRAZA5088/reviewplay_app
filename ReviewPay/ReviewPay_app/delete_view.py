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
from .models import CategoryUsers, Businessdetail,BusinessVerifications, Employee,favorate_business
from .models import Product, UserDetail, Feedback,  Product, ProductImage, Barcode

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_product(request, slug=None):
    try:
        user = request.user  # Get the authenticated user
        # Check if slug is provided
        if slug:
            # Fetch specific product using slug or ID
            product = Product.objects.filter(business=user, id=slug).first()  # Replace `id` with slug if necessary
        else:
            return JsonResponse({'error': 'Product ID or slug is required.'}, status=400)

        # Check if product exists
        if not product:
            return JsonResponse({'error': 'Product not found.'}, status=404)

        # Delete the product
        product.delete()

        return JsonResponse({'message': 'Product deleted successfully.'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_favorite_business(request, slug=None):
    try:
        user = request.user
        user = UserDetail.objects.get(business=user)
        favorites = favorate_business.objects.filter(user=user)
        if slug:
            for favorite in favorites:
                if favorite.id == slug:
                    favorite.delete()
                    return JsonResponse({'message': 'favorite business deleted successfully.'}, status=200)
  # Replace `id` with slug if necessary
        else:
            return JsonResponse({'error': 'Product ID or slug is required.'}, status=400)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  