from django import forms
from django.forms import ModelForm
from django.shortcuts import HttpResponse


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Note,Table





class CreateRegestrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
            ]
        widgets = {
            "username": forms.TextInput(attrs={
                                        "class":"form-control",
                                        "style":"width:250px",
                                        "placeholder":"example@gmail.com",
                                        "type":"email",
                                    }),


            "errors":forms.TextInput(attrs={
                                        "style":"background-color:#ffff00"
                                    })
        }
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={
                                                        "class":"form-control",
                                                        "style":"width: 250px;margin-top:1em",
                                                        "placeholder":"Ваш пароль"
                                                    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                                                        "class":"form-control",
                                                        "style":"width: 250px;margin-top:1em",
                                                        "placeholder":"Підтвердження паролю"
                                                    }))



class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "note"
            ]
        labels = {
            "note":"Запис:"
        }
        widgets = {
            "note": forms.TextInput(attrs={
                    "class":"form-control",
                    "placeholder":"Введіть бажаний запис"
                    })
        }



class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = [
            "loan",
            "description",
            "amount"
            ]
        widgets = {
            "loan":forms.TextInput(attrs={
                    "class":"form-control",
                    "placeholder":"Напишіть за що ви винні гроші"
                    }),
            "description":forms.TextInput(attrs={
                    "class":"form-control",
                    "placeholder":"Опишіть заборгованість"
                    }),
            "amount":forms.TextInput(attrs={
                    "class":"form-control",
                    "placeholder":"Вкажіть сумму заборгованості"
                    })
        }   


class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "note"
            ]
        labels = {
            "note":"Запис:"
        }
        widgets = {
            "note":forms.TextInput(attrs={
                    "class":"form-control"
                    })
        }
        


class TableLoanUpdateForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = [
            "loan"
            ]
        
        labels = {
            "loan":"За що"
            }
        
        widgets = {
            "loan":forms.TextInput(attrs={
                    "class":"form-control"
                })
            }

class TableDescriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = [
            "description"
            ]

        labels = {
            "description":"Опис"
            }

        widgets = {
            "description":forms.TextInput(attrs={
                    "class":"form-control"
                })
            }

class TableAmountUpdateForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = [
            "amount"
            ]

        labels = {
            "amount":"Скільки"
            }

        widgets = {
            "amount":forms.TextInput(attrs={
                    "class":"form-control"
                })
            }