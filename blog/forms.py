from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=["post"]
        labels={
            "user_name":"Your_Name",
            "user_email":"Your_Email",
            "text":"Your Comment"
        }
