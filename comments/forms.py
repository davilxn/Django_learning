from django import forms
from django.core.exceptions import ValidationError
from .models import Comments

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['title_comment', 'email_comment', 'comment']
        labels = {
            'title_comment': 'Título do comentário:',
            'email_comment': 'E-mail:',
            'comment': 'Comentário:'
        }
        widgets = {
            'title_comment': forms.TextInput(attrs={
                'placeholder': 'Digite o título:',
                'class': 'span-2'
            }),
            'email_comment': forms.EmailInput(attrs={
                'placeholder': 'Digite seu e-mail:',
                'class': 'span-2'
            }),
            'comment': forms.TextInput(attrs={
                'placeholder': 'Faça seu comentário: Ex. "Que receita legal!"',
                'class': 'span-2'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title_comment')
        email = cleaned_data.get('email_comment')
        comment = cleaned_data.get('comment')

        if len(title) > 0:
            if len(email) == 0:
                raise ValidationError({
                    'email': 'Preenchimento obrigatório.'
                })
            elif len(comment) == 0:
                raise ValidationError({
                    'comment': 'Preenchimento obrigatório.'
                })
            else: 
                pass

        elif len(email) > 0:
            if len(title) == 0:
                raise ValidationError({
                    'title': 'Preenchimento obrigatório.'
                })
            elif len(comment) == 0:
                raise ValidationError({
                    'comment': 'Preenchimento obrigatório.'
                })
            else: 
                pass
        
        if len(comment) > 0:
            if len(title) == 0:
                raise ValidationError({
                    'title': 'Preenchimento obrigatório.'
                })
            elif len(email) == 0:
                raise ValidationError({
                    'email': 'Preenchimento obrigatório.'
                })
            else: 
                pass
        ...
    ...