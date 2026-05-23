from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tms_auth.models import AuthUser
from tms_auth.serializers.create_users import AuthUserSerializers
from utils.pagination import CustomPagination
from utils.user_permissions import DriverPermission


class ListUserAPIView(APIView):
    serializer_class = AuthUserSerializers
    permission_classes = [DriverPermission]
    # permission_classes = [AdminPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        return AuthUser.objects.all().order_by('-id')

    @swagger_auto_schema(
        operation_id="list_users",
        operation_description="Retrieve paginated list of all users",
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of records per page",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Users retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={

                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=100
                        ),

                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            nullable=True,
                            example="http://127.0.0.1:8000/api/users?page=2"
                        ),

                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            nullable=True,
                            example=None
                        ),

                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
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
                                        format=openapi.FORMAT_EMAIL,
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
                        ),
                    }
                )
            ),

            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Authentication credentials were not provided."
                        )
                    }
                )
            ),

            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Permission denied",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="You do not have permission to perform this action."
                        )
                    }
                )
            ),

            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal server error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="An error occurred while retrieving Users"
                        ),

                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Internal server error details"
                        )
                    }
                )
            ),
        },
        tags=["Auth"]
    )
    def get(self, request):
        try:
            paginator = self.pagination_class()
            queryset = self.get_queryset()
            page = paginator.paginate_queryset(queryset, request=request)
            if page is not None:
                serializer = self.serializer_class(page, many=True, context={'request': request})
                return paginator.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            return Response({"message": "Users List Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        except (ValueError, TypeError, AttributeError) as e:
            return Response({"message": "An error occurred while retrieving Users", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
