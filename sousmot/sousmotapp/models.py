from tabnanny import verbose
from unicodedata import name
from django.db import models

# Create your models here.
class User (models.Model):
    
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
class Dictionary(models.Model):
    
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Dictionaries"
    
    def __str__(self):
        return self.name

class Word (models.Model):
    
    dictionary = models.ForeignKey('Dictionary', on_delete=models.CASCADE)
    
    word = models.CharField(max_length=20)
    
    def __str__(self):
        return self.word

class Mode(models.Model):
    
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Game(models.Model):
    dictionary = models.ForeignKey('Dictionary', on_delete=models.CASCADE, null=True)
    mode = models.ForeignKey('Mode', on_delete=models.CASCADE, null=True)

    nb_letters = models.PositiveSmallIntegerField(null=True)
    time_s = models.PositiveIntegerField(null=True)
    nb_words = models.PositiveSmallIntegerField(null=True)
    in_game = models.BooleanField(default=False)
    uuid = models.TextField()

    def __str__(self):
        return "Game ID : " + str(self.uuid)

class GamesPerUser(models.Model):
    
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    
    position = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = (("user", "game"),)
        verbose_name_plural = "GamesPerUser"
        

class HistorySolo(models.Model):
    
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    
    nb_words = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = (("user", "game"),)
        verbose_name_plural = "HistorySolo"