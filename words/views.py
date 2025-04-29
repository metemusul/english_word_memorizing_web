from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import WordList, Word
from django.urls import reverse_lazy
from gtts import gTTS
import os
from django.conf import settings
import tempfile

# Create your views here.

class WordListView(ListView):
    model = WordList
    template_name = 'words/word_list.html'
    context_object_name = 'word_lists'

class WordListCreateView(CreateView):
    model = WordList
    template_name = 'words/word_list_create.html'
    fields = ['name', 'language_direction']
    success_url = reverse_lazy('words:word-list')

class WordListDetailView(DetailView):
    model = WordList
    template_name = 'words/word_list_detail.html'
    context_object_name = 'word_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = self.object.words.all()
        return context

class AddWordView(View):
    def post(self, request, pk):
        word_list = get_object_or_404(WordList, pk=pk)
        source_word = request.POST.get('source_word')
        target_word = request.POST.get('target_word')

        if source_word and target_word:
            word = Word.objects.create(
                word_list=word_list,
                source_word=source_word,
                target_word=target_word
            )
            return JsonResponse({
                'success': True,
                'word': {
                    'source_word': word.source_word,
                    'target_word': word.target_word,
                    'id': word.id
                }
            })
        return JsonResponse({'success': False, 'error': 'Kelime eklenemedi'})

class DeleteWordView(View):
    def post(self, request, pk):
        word = get_object_or_404(Word, pk=pk)
        word.delete()
        return JsonResponse({'success': True})

class TextToSpeechView(View):
    def get(self, request):
        text = request.GET.get('text', '')
        lang = request.GET.get('lang', 'en')
        
        print(f"Text to speech request - Text: {text}, Language: {lang}")
        
        if not text:
            return JsonResponse({'error': 'Text parameter is required'}, status=400)
            
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file_path = temp_file.name
                print(f"Created temporary file: {temp_file_path}")
                
                # Generate speech
                try:
                    tts = gTTS(text=text, lang=lang)
                    tts.save(temp_file_path)
                    print("Speech generated successfully")
                except Exception as e:
                    print(f"Error in gTTS: {str(e)}")
                    return JsonResponse({'error': f'Speech generation failed: {str(e)}'}, status=500)
                
                # Read the file and return it as response
                try:
                    with open(temp_file_path, 'rb') as f:
                        audio_data = f.read()
                        print(f"Audio file size: {len(audio_data)} bytes")
                        
                        if len(audio_data) == 0:
                            return JsonResponse({'error': 'Generated audio file is empty'}, status=500)
                        
                        response = HttpResponse(audio_data, content_type='audio/mpeg')
                        response['Content-Length'] = len(audio_data)
                        response['Content-Disposition'] = 'inline; filename="speech.mp3"'
                        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                        response['Pragma'] = 'no-cache'
                        response['Expires'] = '0'
                        response['Accept-Ranges'] = 'bytes'
                        
                        print("Response headers:", response.headers)
                        return response
                except Exception as e:
                    print(f"Error reading audio file: {str(e)}")
                    return JsonResponse({'error': f'Error reading audio file: {str(e)}'}, status=500)
                finally:
                    # Clean up the temporary file
                    try:
                        os.unlink(temp_file_path)
                        print("Temporary file deleted")
                    except Exception as e:
                        print(f"Error deleting temporary file: {str(e)}")
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
