from django import forms
from .models import Question, Response

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'Try to keep the title short and catchy'
            })
        }


class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']


class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widget = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'What are your thoughts?'
            })
        }