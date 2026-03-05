from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from .serializers import MyTokenObtainPairSerializer

# Login
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                key = 'refresh_token',
                value = refresh_token,
                httponly = True,
                secure = False,
                samesite = 'Lax',
                path = '/api/token/refresh/',
            )

            del response.data['refresh']
        return response

# Refresh token   
class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            new_refresh_token = response.data.get('refresh')

            response.set_cookie(
                key = 'refresh_token',
                value = new_refresh_token,
                httponly = True,
                secure = False,
                samesite = 'Lax',
                path = '/api/token/refresh/',
            )

            del response.data['refresh']
        return response

# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(({"detail": "Successfully logged out."}), status=200)
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        
        response.delete_cookie('refresh_token', path='/api/token/refresh/')
        return response
