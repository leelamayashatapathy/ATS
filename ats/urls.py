from django.urls import path
from .views import (
    AtsApiView,
    SearchAPIView
)

urlpatterns = [
    path('candidates/', AtsApiView.as_view(), name='candidates'),
    path('candidates/search/', SearchAPIView.as_view(), name='search-candidates'),
]
