from tabnanny import verbose
from unicodedata import name
from django.db import models

# Create your models here.
class User (models.Model):
    
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField()
    
    def __str__(self):
        return self.username
    
class Dictionary(models.Model):
    
    name = models.CharField()
    
    class Meta:
        verbose_name_plural = "Dictionaries"
    
    def __str__(self):
        return self.name

class Word (models.Model):
    
    dictionary = models.ForeignKey('Dictionary', on_delete=models.CASCADE)
    
    word = models.CharField()
    
    def __str__(self):
        return self.word

class Mode(models.Model):
    
    name = models.CharField()
    
    def __str__(self):
        return self.name

class Game(models.Model):
    
    dictionary = models.ForeignKey('Dictionary', on_delete=models.CASCADE)
    mode = models.ForeignKey('Mode', on_delete=models.CASCADE)
    
    nb_letters = models.PositiveSmallIntegerField()
    time_s = models.PositiveIntegerField()
    nb_words = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return "Nombre de lettres : " + self.nb_letters

class Games_per_users(models.Model):
    
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    
    position = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = (("user", "game"),)
        

class History_sole(models.Model):
    
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    
    nb_words = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = (("user", "game"),)