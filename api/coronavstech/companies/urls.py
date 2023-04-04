from rest_framework import routers
from .views import CompanyViewSet, send_email
from django.urls import include, path


router = routers.DefaultRouter()
router.register("companies", viewset=CompanyViewSet, basename="companies")

urlpatterns = [
    path("", include(router.urls)),
    path('send-email/', send_email, name='send_email'),
]
