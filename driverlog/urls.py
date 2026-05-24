from django.urls import path

from driverlog.views import CreateDriverLogsAPIView, ListDriverLogsAPIView

urlpatterns = [
    path("create/", CreateDriverLogsAPIView.as_view(), name="create_logs"),
    path("list/", ListDriverLogsAPIView.as_view(), name="list_logs"),
]
