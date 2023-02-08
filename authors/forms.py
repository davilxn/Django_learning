from django import forms
from django.contrib.auth.models import User
from recipes.models import Recipe
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        required = True,
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Digite novamente sua senha'
        }),
        error_messages={
            'required': 'Este campo deve ser preenchido'
        },
        label="Repita sua senha:"
    )
    class Meta:
        model = User           
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

        labels = {
            'username': 'Nome de usuário:',
            'first_name': 'Nome:',
            'last_name': 'Sobrenome:',
            'email': 'E-mail:',
            'password': 'Senha:'
        }

        help_texts = {
            'username': '150 caracteres ou menos. Letras, números e @/.+-_',
            'email': 'Este email deve ser um email válido.',
            'password': 'Por segurança, crie uma senha formada por letras e números'
        }

        error_messages = {
            'username': {
                'required': 'Este campo deve ser preenchido.'
            },
            'password': {
                'required':'Este campo deve ser preenchido.'    
            },
            'first_name': {
                'invalid': 'Não é permitido'
            }
        }

        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu sobrenome'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Digite seu email'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome de usuário'
            }),
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if 'John Doe' in data or 'Jane Doe' in data:
            raise ValidationError('Não são permitidos desconhecidos.', code='invalid')
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('Este e-mail já foi cadastrado.')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('Um usuário com este nome já existe.')

        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
            'password':'As senhas estão diferentes',
            'password2': 'As senhas estão diferentes'
            })


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite sua senha'
        }),
        error_messages={
            'required': 'Este campo deve ser preenchido.'
        },
        label='Nome de usuário'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        }),
        error_messages={
            'required': 'Este campo deve ser preenchido.'
        },
        label='Senha'
    )

class AuthorRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 'preparation_time_unit', 'servings_time', 'servings_time_unit', 'preparation_steps', 'cover']
        widgets = { 
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'                   
                }
          ),
            'preparation_steps': forms.Textarea(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_time_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }
        labels = {
            'title': 'Título:',
            'preparation_steps': 'Passo-a-passo:',
            'servings_time': 'Serve:',
            'servings_time_unit': 'Unidades:',
            'preparation_time': 'Tempo de preparo:',
            'preparation_time_unit': 'Unidade de tempo:',
            'description': 'Descrição:',
            'cover': 'Imagem:',
        }     