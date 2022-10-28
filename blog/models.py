from django.db import models

from login.models import RegisterUser
CATEGORY_CHOICES=[("1","Mental Health"),("2","Heart Disease"),("3","Covid19"),("4","Immunization")]
# Create your models here.
class blog(models.Model):
    author_id=models.ForeignKey(RegisterUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    image=models.ImageField()
    category=models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    summary=models.CharField(max_length=200)
    content=models.CharField(max_length=2000)
    is_draft=models.BooleanField(default=False)
