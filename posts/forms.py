from django import forms
from .models import Post
from .models import Archivos
from django.contrib.auth.models import User
from django.forms import ModelForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "nombrealbum",
            "titulo",
            "imagen",
            "cancion",
            "Letra",
        ]  
        
class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivos
        fields = [
            "artista",
            "album",
        ]
        
class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }