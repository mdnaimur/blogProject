from django import forms
from django.forms import fields, models
from pagedown.widgets import PagedownWidget
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(attrs={"show_preview":False}))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [ 'title','content' ,'image','draft','publish']