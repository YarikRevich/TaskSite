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
            "note",
            "description"
            ]
        labels = {
            "note":"Запис:",
            "description":"Опис:"
        }
        error_messages = {
            "note":{"required":"Поле з записом не заповнене"},
            "description":{"required":"Поле з описом не заповнене"}

        }

        widgets = {
            "note": forms.TextInput(attrs={
                    "class":"form-control",
                    "placeholder":"Введіть бажаний запис"
                    }),
            "description":forms.Textarea(attrs={
                    "class":"form-control",
                    "style":"width:100%;height:150px;resize:none",
                    "placeholder":"Введіть бажаний опис"
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
        error_messages = {
            "amount":{
                "invalid":"Ви маєте ввести число",
                "required":"Поле має бути заповнене"
            }
        }


        labels = {
            "loan":"За що",
            "description":"Опис",
            "amount":"Скільки"
            }
            
        widgets = {
            "loan":forms.TextInput(attrs={
                    "class":"form-control",
                    "style":"margin-top:.8em",
                    "placeholder":"Напишіть за що ви винні гроші"
                    }),
            "description":forms.TextInput(attrs={
                    "class":"form-control",
                    "style":"margin-top:.8em",
                    "placeholder":"Опишіть заборгованість"
                    }),
            "amount":forms.TextInput(attrs={
                    "class":"form-control",
                    "style":"margin-top:.8em",
                    "placeholder":"Вкажіть сумму заборгованості"
                    })
        }   


class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "note"
            ]

        error_messages = {
            "note":{"required":"Поле запису не заповнене"}
        }

        labels = {
            "note":"Запис:"
        }
        widgets = {
            "note":forms.TextInput(attrs={
                    "class":"form-control"
                    })
        }
        
class EditDescriptionForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "description"
        ]

        error_messages = {
            "description":{"required":"Поле опису не заповнене"}
        }

        labels = {
            "description":"Опис:"
        }
        widgets = {
            "description":forms.Textarea(attrs={
                    "class":"form-control",
                    "style":"resize:none;width:100%;height:150px"
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
        error_messages = {
            "amount":{
                "invalid":"Ви маєте ввести число",
                "required":"Поле має бути заповнене"
            }
        }
        labels = {
            "amount":"Скільки"
            }

        widgets = {
            "amount":forms.TextInput(attrs={
                    "class":"form-control"
                })
            }