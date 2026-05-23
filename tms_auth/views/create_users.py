from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from tms_auth.celery_tasks import send_mail_func
from tms_auth.models import AuthUser
from tms_auth.serializers.create_users import AuthUserSerializers


class CreateUserView(generics.CreateAPIView):
    """
        API view to create a new user.

        This view handles the creation of a new user by accepting user data,
        validating it, and saving it to the database. It allows any user
        (authenticated or not) to access this endpoint.

        Attributes:
            queryset: Queryset of all AuthUser objects.
            serializer_class: Serializer class for validating and serializing user data.
            permission_classes: Permissions allowing any user to access this view.
    """
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializers
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_id='create_user',
        operation_description='Create a new user account',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "first_name",
                "last_name",
                "email",
                "password"
            ],
            properties={
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="First name",
                    maxLength=20,
                    example="John"
                ),

                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Last name",
                    maxLength=20,
                    example="Doe"
                ),

                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="User email address",
                    example="john@example.com"
                ),

                "user_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number",
                    example="+9779852314785"
                ),

                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description="Password",
                    example="MyPassword123!"
                ),

                "country": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Country name",
                    example="Nepal"
                ),

                "role": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User role",
                    example="student"
                ),

                "passport": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Passport number",
                    example="PA123456"
                ),

                "is_staff": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is staff user",
                    example=False
                ),

                "is_superuser": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is superuser",
                    example=False
                ),

                "extras": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Additional metadata",
                    example={
                        "preferences": {
                            "notifications": True
                        }
                    }
                ),
            }
        ),

        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={

                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Please Check Email For Verification..."
                        ),

                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={

                                "id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    example=1
                                ),

                                "first_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="John"
                                ),

                                "last_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Doe"
                                ),

                                "email": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="john@example.com"
                                ),

                                "user_number": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="+9779852314785"
                                ),

                                "country": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Nepal"
                                ),

                                "role": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="student"
                                ),

                                "passport": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="PA123456"
                                ),

                                "is_staff": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    example=False
                                ),

                                "is_superuser": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    example=False
                                ),

                                "created_at": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_DATETIME,
                                    example="2026-05-23T10:30:00Z"
                                ),

                                "updated_at": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_DATETIME,
                                    example="2026-05-23T10:30:00Z"
                                ),

                                "extras": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    example={
                                        "preferences": {
                                            "notifications": True
                                        }
                                    }
                                ),
                            }
                        )
                    }
                )
            ),

            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "email": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            example=["This field is required."]
                        ),

                        "password": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            example=["Password is too short."]
                        ),
                    }
                )
            ),

            status.HTTP_409_CONFLICT: openapi.Response(
                description="Conflict Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User with this email already exists."
                        )
                    }
                )
            ),

            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="An unexpected error occurred."
                        )
                    }
                )
            ),
        },

        tags=["Auth"]
    )
    def create(self, request, *args, **kwargs):
        """
            Create a new user with the provided data.

            Args:
                request: The HTTP request containing user data in JSON format.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Response: A response object containing a success message and the
                          serialized user data with HTTP 200 status.

            Raises:
                serializers.ValidationError: If the provided data is invalid.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        email = request.data.get("email")
        user = AuthUser.objects.filter(email=email).first()
        try:
            if user:
                token = default_token_generator.make_token(user)
                verification_link = request.build_absolute_uri(reverse("verify_users", args=[user.id, token]))
                context = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'verification_link': verification_link,
                    'site_name': 'ELD_TMS',
                    'protocol': 'https' if request.is_secure() else 'http',
                    'domain': request.get_host(),
                }
                html_message = render_to_string('emails/user_verification.html', context)
                plain_message = strip_tags(html_message)
                send_mail_func.delay(
                    subject="Activate your ELD Account",
                    html_message=html_message,
                    plain_message=plain_message,
                    from_email="ajay.softechpark@gmail.com",
                    recipient_list=[email]
                )

            return Response({"message": "Please Check Email For Verification...", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Some error occurred while creating user", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
