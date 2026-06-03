from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    score = models.IntegerField(default=0)
    skills = models.TextField()
    role = models.CharField(max_length=100, blank=True)

class InterviewResult(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=100, blank=True)

    question = models.TextField()

    answer = models.TextField()

    score = models.FloatField()

    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):

    role = models.CharField(max_length=100)

    difficulty = models.CharField(max_length=50)

    question = models.TextField()

    answer = models.TextField()

    def __str__(self):
        return f"{self.role} - {self.question[:50]}"

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name