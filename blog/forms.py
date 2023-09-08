from django import forms
from .models import blog
class PostForm(forms.ModelForm):
    class Meta:
        model=blog
        exclude=["author","liked_by_users","no_of_likes"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print(visible)
            visible.field.widget.attrs['class'] = 'form-control'
        visible.field.widget.attrs['class']='form-check-input'
        visible.field.widget.attrs['class']='ml-3'