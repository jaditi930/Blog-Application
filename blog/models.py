from django.db import models

from login.models import RegisterUser
CATEGORY_CHOICES=[("Entertainment","Entertainment"),("Technology","Technology"),("Food","Food"),("Travel","Travel"),("Health","Health")]
# Create your models here.
class blog(models.Model):
    author=models.ForeignKey(RegisterUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    image=models.ImageField(blank=True)
    category=models.CharField(max_length=100,choices=CATEGORY_CHOICES,default="Technology")
    summary=models.CharField(max_length=200000)
    content=models.CharField(max_length=200000)
    is_draft=models.BooleanField(default=False)
    liked_by_users=models.TextField(default="",blank=True)
    no_of_likes=models.IntegerField(default=0)
    

    def __str__(self):
        return self.title+ " " +str(self.id)

