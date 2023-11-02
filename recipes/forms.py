from enum import Enum
from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, NumberInput
from recipes.models import Recipe, Category

class CategoryEnum(Enum):
    BREAKFAST = 'Breakfast'
    FIRST_COURSE = 'First Course'
    MAIN = 'Main'
    DESSERT = 'Desert'

CATEGORY_CHOICE = (
    (CategoryEnum.BREAKFAST.value, 'Breakfast'),
    (CategoryEnum.FIRST_COURSE.value, 'First Course'),
    (CategoryEnum.MAIN.value, 'Main'),
    (CategoryEnum.DESSERT.value, 'Desert'),
)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'steps', 'cooking_time', 'image']
        widgets = {
            'name': TextInput(attrs={'style': 'width: 100%'}),
            'description': Textarea(attrs={'style': 'width: 100%'}),
            'steps': Textarea(attrs={'style': 'width: 100%'}),
            'cooking_time': NumberInput(attrs={'style': 'width: 100%'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CookingForm(forms.Form):
    category = forms.CharField(label='Category',required=False,widget=forms.Select(attrs={'required': 'True'}, choices=CATEGORY_CHOICE))
    name = forms.CharField(label='Label', max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Label for the meal','required': 'True'}))
    cooking_time = forms.IntegerField(label='Time', required=False,widget=forms.NumberInput(attrs={'class': 'form-control','required': 'True'}))
    description = forms.CharField(label='Description', max_length=1000,required=False,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Long description','required': 'True'}))
    steps = forms.CharField(label='Steps', required=False, max_length=1000,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Steps for preparation','required': 'True'}))
    image = forms.ImageField(label='Photo', required=False, widget=forms.FileInput(attrs={'required': 'True'}))

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=65)
    password = forms.CharField(label='Password', max_length=65, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': 'Username'
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords are not the same.')
        return cd['password2']
