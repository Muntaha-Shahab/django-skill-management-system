from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    years_of_experience = models.IntegerField()

    def __str__(self):
        return f"{self.skill_name} ({self.user.username})"
