from django.db import models

# Create your models here.

class WordList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    language_direction = models.CharField(max_length=20, choices=[
        ('en_tr', 'English - Turkish'),
        ('tr_en', 'Turkish - English')
    ], default='en_tr')

    def __str__(self):
        return self.name

class Word(models.Model):
    word_list = models.ForeignKey(WordList, on_delete=models.CASCADE, related_name='words')
    source_word = models.CharField(max_length=100)
    target_word = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_word} - {self.target_word}"
