from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm, Form
from django.core.validators import FileExtensionValidator

from django import forms
from django.forms.widgets import TextInput, PasswordInput, Select, NumberInput

from . import models

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(
            attrs={'class':'form-control'}
            )
        )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={'class':'form-control'}
        )
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TournamentForm(ModelForm):
    class Meta:
        model = models.Tournament
        fields = '__all__'
        exclude = ['user']
        labels = {
            'name':'Name',
            'place':'Place',
            'tdate':'Date',
            'referre':'Referre',
            'secretary':'Secretary'
        }
        widgets = {
            'name':TextInput(attrs={
                'class':'form-control',
                'id':'tournament-name',
                'title':'Tournaments name',
                'placeholder':'',
            }),
            'place':TextInput(attrs={
                'class':'form-control',
                'id':'tournament-place',
                'title':'Tournaments place',
                'placeholder':'',
            }),
            'tdate':TextInput(attrs={
                'class':'form-control',
                'id':'tournament-date',
                'title':'Tournaments date',
                'placeholder':'',
            }),
            'referre':TextInput(attrs={
                'class':'form-control',
                'id':'tournament-referre',
                'title':'Referre',
                'placeholder':'',
            }),
            'secretary':TextInput(attrs={
                'class':'form-control',
                'id':'tournament-secretary',
                'title':'Secretary',
                'placeholder':'',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required': 'Please insert Name of tournament'}

class CategoryForm(ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'
        exclude = ['user']
        labels = {
            'name':'Name'
        }
        widgets = {
            'name':TextInput(attrs={
                'class':'form-control',
                'id':'category-name',
                'title':'Category name',                
                'placeholder':'',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required':'Please enter the Name '}

class ParticipantsForm(Form):
    csv_file = forms.FileField(
        label='Выберите CSV файл',
        help_text='Файл должен быть в формате .csv',
        widget=forms.FileInput(attrs={
            'class':'form-control',
            'id':'select-file',
            'accept': '.csv'})
    )

class CompetitionsForm(ModelForm):
    class Meta:
        model = models.Competition
        fields = '__all__'
        exclude = ['tournament', 'user']
        labels = {
            'category':'Category',
            'gender':'Gender',
            'age':'Age'
        }
        widgets = {
            'category':Select(attrs={
                'id':'competition-category',
                'class':'form-control form-control-sm',
            }),
            'gender': Select(attrs={
                'id':'competition-gender',
                'class':'form-control form-control-sm',
            }),
            'age':TextInput(attrs={
                'class':'form-control',
                'id':'competition-age',
                'title':'Age',
                'placeholder':'',
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(CompetitionsForm, self).__init__(*args, **kwargs)
        data = kwargs.pop('initial')
        if 'user' in data:
            user_id = data.pop('user')
            print('INIT OK: ', user_id)
            qCategory = models.Category.objects.filter(Q(user=user_id))
        else:
            qCategory = models.Category.objects.all()
        self.fields['category'].queryset = qCategory
        self.fields['category'].initial = [0]
        
class CPForm(ModelForm):
    class Meta:
        model = models.CompetitionParticipants
        fields = '__all__'
        exclude = ['competition', 'user']
        labels = {
            'pos':'Position',
            'participant':'Participant',
        }
        widgets = {
            'pos':NumberInput(attrs={
                'id':'cp-pos',
                'class':'form-control form-control-sm', 
            }),
            'participant':Select(attrs={
                'id':'cp-participant',
                'class':'form-control form-control-sm',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(CPForm, self).__init__(*args, **kwargs)
        data = kwargs.pop('initial')
        if 'trn' in data:
            trn_id = data.pop('trn')
            print("TRN_ID: ", trn_id)
            qParticipant = models.Participants.objects.filter(Q(tournament_id=trn_id))
        else:
            qParticipant = models.Participants.objects.all()
        self.fields['participant'].queryset = qParticipant
        self.fields['participant'].initial = [0]