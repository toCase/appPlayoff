from django.db import models
from django.contrib.auth.models import User

class Tournament(models.Model):
    idx = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    tdate = models.CharField(max_length=255)
    referre = models.CharField(max_length=40)
    secretary = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    idx = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Participants(models.Model):
    idx = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'idx']
    
class Competition(models.Model):
    class GenderList(models.IntegerChoices):
        MALE = 1, ("Чоловіки")
        FEMALE = 2, ("Жінки")
        MIX = 3, ("Змішана")
        
    idx = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GenderList, default=GenderList.MALE)
    age = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.category.name} -- {self.get_gender_display()} -- {self.age}'
    
    class Meta:
        ordering = ['gender', 'category']
    
class CompetitionParticipants(models.Model):
    idx = models.BigAutoField(primary_key=True)
    pos = models.IntegerField(default=1)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['pos', 'idx']
