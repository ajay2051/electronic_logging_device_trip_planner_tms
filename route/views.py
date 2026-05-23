from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from route.models import Route
from route.serializers import RouteSerializer
from utils.pagination import CustomPagination
from utils.user_permissions import DriverPermission


class CreateRouteAPIView(APIView):
    permission_classes = [DriverPermission]
    serializer_class = RouteSerializer

    @swagger_auto_schema(
        operation_id="create_route",
        operation_description="Create a new route with current, pickup, and dropoff locations",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "current_location",
                "pickup_location",
                "dropoff_location"
            ],
            properties={

                "current_location": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Current location in GeoJSON format",
                    example={
                        "type": "Point",
                        "coordinates": [85.3240, 27.7172]
                    }
                ),

                "pickup_location": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Pickup location in GeoJSON format",
                    example={
                        "type": "Point",
                        "coordinates": [85.3270, 27.7150]
                    }
                ),

                "dropoff_location": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Dropoff location in GeoJSON format",
                    example={
                        "type": "Point",
                        "coordinates": [85.3300, 27.7100]
                    }
                ),
            }
        ),

        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Route created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={

                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=1
                        ),

                        "created_by": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="John Doe"
                        ),

                        "current_location": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={
                                "type": "Point",
                                "coordinates": [85.3240, 27.7172]
                            }
                        ),

                        "pickup_location": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={
                                "type": "Point",
                                "coordinates": [85.3270, 27.7150]
                            }
                        ),

                        "dropoff_location": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={
                                "type": "Point",
                                "coordinates": [85.3300, 27.7100]
                            }
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
                    }
                )
            ),

            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Validation Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "current_location": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            example=["Invalid GeoJSON format."]
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

            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal server error",
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

        tags=["Route"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteListAPIView(APIView):
    permission_classes = [DriverPermission]
    # permission_classes = [AdminPermission]
    serializer_class = RouteSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Route.objects.all().order_by('-id')

    @swagger_auto_schema(
        operation_id="list_routes",
        operation_description="Retrieve paginated list of routes",

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
                description="Routes retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={

                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=25
                        ),

                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            nullable=True,
                            example="http://127.0.0.1:8000/api/routes?page=2"
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

                                    "created_by": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="John Doe"
                                    ),

                                    "current_location": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        example={
                                            "type": "Point",
                                            "coordinates": [85.3240, 27.7172]
                                        }
                                    ),

                                    "pickup_location": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        example={
                                            "type": "Point",
                                            "coordinates": [85.3270, 27.7150]
                                        }
                                    ),

                                    "dropoff_location": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        example={
                                            "type": "Point",
                                            "coordinates": [85.3300, 27.7100]
                                        }
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

            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal server error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="An error occurred while retrieving route"
                        ),

                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Internal server error details"
                        )
                    }
                )
            ),
        },

        tags=["Route"]
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
            return Response({"message": "Route List Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        except (ValueError, TypeError, AttributeError) as e:
            return Response({"message": "An error occurred while retrieving route", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
