from django import forms
from .models import Answer, Question
from mptt.forms import TreeNodeChoiceField


class NewAnswerForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Answer.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Answer
        fields = ('parent', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        Answer.objects.rebuild()
        return super(NewAnswerForm, self).save(*args, **kwargs)




class PostSearchForm(forms.Form):
    q = forms.CharField()
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model=Question
        fields=['title','content']
        