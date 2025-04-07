from django.urls import path
from . import views

urlpatterns = [
    path('', views.WordListView.as_view(), name='word-list'),
    path('create/', views.WordListCreateView.as_view(), name='word-list-create'),
    path('<int:pk>/', views.WordListDetailView.as_view(), name='word-list-detail'),
] 