from django import forms
from .models import blog
class PostForm(forms.ModelForm):
    class Meta:
        model=blog
        exclude=["author","liked_by_users","no_of_likes"]