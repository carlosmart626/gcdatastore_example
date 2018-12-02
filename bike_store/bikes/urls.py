from django.urls import path

from . import views

urlpatterns = [
    path('', views.BikesListView.as_view(), name="bikes-list"),
    path('<int:id>/', views.BikeView.as_view(), name="bikes-detail"),
]