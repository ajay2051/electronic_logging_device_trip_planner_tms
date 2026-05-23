from django.urls import path

from route.views import CreateRouteAPIView, RouteListAPIView

urlpatterns = [
    path("create/", CreateRouteAPIView.as_view(), name="create_route"),
    path("list/", RouteListAPIView.as_view(), name="list_route"),
]
