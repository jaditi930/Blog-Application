from django.db import models

from login.models import RegisterUser
CATEGORY_CHOICES=[("Mental Health","Mental Health"),("Heart Disease","Heart Disease"),("Covid19","Covid19"),("Immunization","Immunization")]
# Create your models here.
class blog(models.Model):
    author=models.ForeignKey(RegisterUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    image=models.ImageField()
    category=models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    summary=models.CharField(max_length=200)
    content=models.CharField(max_length=2000)
    is_draft=models.BooleanField(default=False)
    liked_by_users=models.TextField(default="",blank=True)
    no_of_likes=models.IntegerField(default=0)
