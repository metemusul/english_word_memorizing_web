from django.urls import path
from .views import WordListView, WordListCreateView, WordListDetailView, AddWordView, DeleteWordView
from . import views

app_name = 'words'

urlpatterns = [
    path('', WordListView.as_view(), name='word-list'),
    path('create/', WordListCreateView.as_view(), name='word-list-create'),
    path('<int:pk>/', WordListDetailView.as_view(), name='word-list-detail'),
    path('<int:pk>/add-word/', AddWordView.as_view(), name='add-word'),
    path('word/<int:pk>/delete/', DeleteWordView.as_view(), name='delete-word'),
    path('text-to-speech/', views.TextToSpeechView.as_view(), name='text_to_speech'),
] 