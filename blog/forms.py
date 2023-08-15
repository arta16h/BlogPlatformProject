from django import forms
from .models import Post
from users.models import Author


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']


class CommentUpdateForm(forms.Form):
    content = forms.CharField(max_length=255, widget=forms.Textarea)


class CreateCommentForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    content = forms.CharField(max_length=255, widget=forms.Textarea)