from django import forms
from .models import Answer
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
        fields = ('name', 'parent', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        Answer.objects.rebuild()
        return super(NewAnswerForm, self).save(*args, **kwargs)




