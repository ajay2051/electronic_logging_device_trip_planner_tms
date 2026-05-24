from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from driverlog.models import Driverlog
from driverlog.serializers import DriverLogSerializer
from utils.pagination import CustomPagination
from utils.user_permissions import DriverPermission


class CreateDriverLogsAPIView(APIView):
    permission_classes = [DriverPermission]
    serializer_class = DriverLogSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request}, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Driver Log Created Success", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDriverLogsAPIView(APIView):
    permission_classes = [DriverPermission]
    # permission_classes = [AdminPermission]
    serializer_class = DriverLogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Driverlog.objects.all().order_by('-id')

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
