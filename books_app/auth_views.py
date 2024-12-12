from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import SignupSerializer, CustomTokenObtainPairSerializer
from .helpers import generate_auth_token
from .responses import ApiResponse


class SignUpView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		try:
			serializer = SignupSerializer(data=request.data)

			# Save the new user
			if serializer.is_valid():
				user = serializer.save()

				# Generate JWT tokens
				tokens = generate_auth_token(user)
				res_obj = {
					'user': serializer.data,
					'tokens': tokens
				}
				res = ApiResponse.success_response("User successfully created", "00", res_obj)
				return Response(res, status=status.HTTP_201_CREATED)
		except Exception as e:
			res = ApiResponse.error_response(e, '00')
			return Response(res, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
	permission_classes = [AllowAny]
	serializer_class = CustomTokenObtainPairSerializer

	def post(self, request, *args, **kwargs):
		try:
			response = super().post(request, *args, **kwargs)

			# Modify the response data
			data = response.data
			# Change 'refresh' to 'refresh_token'
			data['refresh_token'] = data.pop('refresh')
			# Change 'access' to 'access_token'
			data['access_token'] = data.pop('access')
			res = ApiResponse.success_response( "User successfully logged in", "00", data)
			return Response(res, status=status.HTTP_200_OK)
		except Exception as e:
			res = ApiResponse.error_response(e, '03')
			return Response(res, status=status.HTTP_400_BAD_REQUEST)