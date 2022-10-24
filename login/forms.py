from django import forms
from login.models import RegisterUser
from django.forms import TextInput, Textarea
class RegisterUserForm(forms.ModelForm):
    confirm_pass=forms.CharField(max_length=200, required=True,widget=TextInput(attrs={'type': 'password'}))
    class Meta:
        model=RegisterUser
        fields=['first_name','last_name','username','password','confirm_pass','email','role','address','state','pincode','city','profile_picture']
        widgets={
            'password': TextInput(attrs={'type': 'password'}),
            'address':Textarea(attrs={'rows':5,'cols':25})
        }
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
