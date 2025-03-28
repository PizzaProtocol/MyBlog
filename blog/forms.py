from  django import forms
from blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']


class SearchForm(forms.Form):
    query = forms.CharField(label= '')