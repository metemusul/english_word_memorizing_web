from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import WordList, Word
from django.urls import reverse_lazy

# Create your views here.

class WordListView(ListView):
    model = WordList
    template_name = 'words/word_list.html'
    context_object_name = 'word_lists'

class WordListCreateView(CreateView):
    model = WordList
    template_name = 'words/word_list_create.html'
    fields = ['name', 'language_direction']
    success_url = reverse_lazy('word-list')

class WordListDetailView(DetailView):
    model = WordList
    template_name = 'words/word_list_detail.html'
    context_object_name = 'word_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = self.object.words.all()
        return context
