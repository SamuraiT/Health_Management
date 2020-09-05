from django import forms
from .models import HealthApp
import bootstrap_datepicker_plus as datetimepicker

EXERCISE = (('N/A', 'Exercise'),('Yes', 'Yes'), ('No', 'No'))


class PostForm(forms.ModelForm):
    class Meta:
        model = HealthApp
        fields=('postdate','weight','steps','exercise','notes')


class InputForm(forms.Form):
    postdate = forms.DateField(label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-2',
                'style': 'width:15%',
                'placeholder': 'Date',
                'id': 'calendar',
            }
        )
    )

    weight = forms.IntegerField(label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-2',
                'style': 'width:15%',
                'placeholder': 'Weight',
            }
        )
    )

    steps = forms.IntegerField(label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-2',
                'style': 'width:15%',
                'placeholder': 'Steps ',
            }
        )
    )

    exercise = forms.ChoiceField(label="",
        choices= EXERCISE,
        widget=forms.Select(
            attrs={
                'class': 'form-control mr-2',
                'style': 'width:15%',
                'placeholder': 'Exercise',
            }
        )
    )

    notes = forms.CharField(label="",
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-2',
                'style': 'width:25%',
                'placeholder': 'Notes',
            }
        )
    )
