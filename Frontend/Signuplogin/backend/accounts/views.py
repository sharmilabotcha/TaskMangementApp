from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import SignupSerializer, LoginSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)  # Fixed data initialization
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "User created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)  # Authenticate user

        if user:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
            }, status=status.HTTP_200_OK)
        
        # Invalid credentials response
        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_403_FORBIDDEN
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


token_generator = PasswordResetTokenGenerator()

@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        # Logic to handle forgot password
        return JsonResponse({'message': 'Password reset email sent.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
    logger.info('Forgot password request received.')
    try:
        email = request.data.get('email')
        logger.info(f'Received email: {email}')
        if not email:
            logger.warning('Email is required but not provided.')
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            logger.info('User found: %s', user.username)
        except User.DoesNotExist:
            logger.warning('User not found for email: %s', email)
            return Response({"message": "If the email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        token = token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{user.id}/{token}/"
        logger.info('Generated reset URL: %s', reset_url)

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info('Reset email sent to: %s', email)

        return Response({"message": "If the email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error('An error occurred: %s', str(e))
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def reset_password(request, user_id, token):
    new_password = request.data.get('password')
    if not new_password:
        return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User = get_user_model()
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)

    if not token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

    # Reset the password
    user.set_password(new_password)
    user.save()
    return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

