from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CategoryUsers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from . import utils


def get_jwt_token(user):
                # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    # token = AccessToken.for_user(user)
    data = {
        'refresh': str(refresh),
        'access_token': access_token
    }
    return data

class GoogleLogin(APIView):

    def post(self, request):
        try:
            if 'code' in request.data.keys():
                code = request.data['code']
                id_token = utils.get_id_token_with_code_method_1(code)
                user_email = id_token['email']
                
                try:
                    user = CategoryUsers.objects.get(email=user_email)
                except CategoryUsers.DoesNotExist:
                    return Response({'error': 'Signup are required'})
                token = get_jwt_token(user)
            
                return Response({'access_token': token['access_token'],'refresh': token['refresh'] ,'username': user_email})

            return Response(status=status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            return Response({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)