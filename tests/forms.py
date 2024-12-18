from django import forms
from .models import Question, Answer


class TestForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=200, required=True)

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ModelChoiceField(
                queryset=Answer.objects.filter(question=question),
                widget=forms.RadioSelect,
                label=question.text,
                required=True
            )
