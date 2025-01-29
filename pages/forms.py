from django import forms # type: ignore
from pages.models import Posts

class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ['content', 'post_img']

class updatePost(forms.ModelForm):
    
    class Meta:
        model = Posts
        fields= ['content', 'post_img']