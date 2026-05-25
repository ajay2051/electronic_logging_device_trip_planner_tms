from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from driverlog.models import Driverlog
from driverlog.serializers import DriverLogSerializer
from utils.pagination import CustomPagination
from utils.user_permissions import DriverPermission, AdminPermission


class CreateDriverLogsAPIView(APIView):
    permission_classes = [DriverPermission]
    serializer_class = DriverLogSerializer

    @swagger_auto_schema(
        operation_id="create_driver_logs",
        operation_description="Create multiple driver logs",

        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=[
                    "log_date",
                    "driver_number",
                    "vehicle_number"
                ],
                properties={

                    "log_date": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        example="2026-05-24"
                    ),

                    "driver_number": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="DRV-1001"
                    ),

                    "driver_signature": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="John Doe"
                    ),

                    "co_driver_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Jane Doe"
                    ),

                    "driver_initials": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="JD"
                    ),

                    "vehicle_number": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="BA-2-CHA-1234"
                    ),

                    "trailer_number": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="TRL-202"
                    ),

                    "total_miles_today": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        example=450
                    ),

                    "total_mileage_today": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        example=12500
                    ),

                    "operating_center_name_address": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Kathmandu Operating Center, Nepal"
                    ),

                    "total_off_duty_time": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="08:00"
                    ),

                    "total_sleeper_time": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="02:00"
                    ),

                    "total_driving_time": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="09:00"
                    ),

                    "total_on_duty_time": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="11:00"
                    ),

                    "shipper": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="ABC Logistics"
                    ),

                    "commodity": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Electronics"
                    ),

                    "load_no": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="LOAD-001"
                    ),

                    "route": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Kathmandu - Pokhara"
                    ),
                }
            )
        ),

        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Driver logs created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={

                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Driver Log Created Success"
                        ),

                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={

                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        example=1
                                    ),

                                    "log_date": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATE,
                                        example="2026-05-24"
                                    ),

                                    "driver_number": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="DRV-1001"
                                    ),

                                    "vehicle_number": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="BA-2-CHA-1234"
                                    ),

                                    "route": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="Kathmandu - Pokhara"
                                    ),

                                    "created_at": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        example="2026-05-24T10:30:00Z"
                                    ),

                                    "updated_at": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        example="2026-05-24T10:30:00Z"
                                    ),
                                }
                            )
                        )
                    }
                )
            ),

            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "driver_number": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            example=["This field is required."]
                        )
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
        },

        tags=["Driver Logs"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request}, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Driver Log Created Success", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDriverLogsAPIView(APIView):
    # permission_classes = [DriverPermission]
    permission_classes = [AdminPermission]
    serializer_class = DriverLogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Driverlog.objects.select_related('route').order_by('-id')

    @swagger_auto_schema(
        operation_id="list_driver_logs",
        operation_description="Retrieve paginated list of driver logs",

        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                description='Page number',
                type=openapi.TYPE_INTEGER
            ),

            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                description='Number of records per page',
                type=openapi.TYPE_INTEGER
            ),
        ],

        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Driver logs retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={

                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=50
                        ),

                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            nullable=True,
                            example="http://127.0.0.1:8000/api/driver-logs/?page=2"
                        ),

                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
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

                                    "log_date": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATE,
                                        example="2026-05-24"
                                    ),

                                    "driver_number": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="DRV-1001"
                                    ),

                                    "driver_signature": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="John Doe"
                                    ),

                                    "vehicle_number": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="BA-2-CHA-1234"
                                    ),

                                    "route": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="Kathmandu - Pokhara"
                                    ),

                                    "created_at": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        example="2026-05-24T10:30:00Z"
                                    ),

                                    "updated_at": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        example="2026-05-24T10:30:00Z"
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
                            example="An error occurred while retrieving driver logs"
                        ),

                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Internal server error details"
                        ),
                    }
                )
            ),
        },

        tags=["Driver Logs"]
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
            return Response({"message": "Driver Log List Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        except (ValueError, TypeError, AttributeError) as e:
            return Response({"message": "An error occurred while retrieving driver logs", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
