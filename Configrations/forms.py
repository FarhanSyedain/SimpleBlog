from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django.forms import ModelForm
from .models import User,Staff

class CreateUser(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

class UpdateUser(SetPasswordForm):
    
    class Meta:
        model = User
        fields = ['password']
        

class Update_Staff(ModelForm):
    
    class Meta:
        model = Staff
        fields = ['about_me','phone_number','email','profile_pic']