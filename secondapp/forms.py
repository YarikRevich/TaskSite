from django import forms
from django.forms import ModelForm
from .models import Regestration,Note,Table
from django.core.exceptions import ValidationError



class Forma(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["note"]
        widgets = {
            "note": forms.TextInput(attrs={"class":"form-control","placeholder":"Введіть бажаний запис"})
        }


    def clean_note(self):
        data = self.cleaned_data["note"]
        return data
    
    
    
    

    def save(self):
        from .views import remote_email,remote_addr
        new = Note.objects.create(
            note = self.cleaned_data["note"],
            note_email = remote_email[remote_addr["email"]]
        )
        return new
    


class TableForm(forms.Form):
    loan = forms.CharField(max_length=50,label="За що")
    description = forms.CharField(max_length=200,required=False,label="Опис")
    amount = forms.IntegerField(label="Сума")

    loan.widget.attrs.update({"class":"form-control","placeholder":"Напишіть за що ви винні гроші"})
    description.widget.attrs.update({"class":"form-control","placeholder":"Опишіть заборгованість"})
    amount.widget.attrs.update({"class":"form-control","placeholder":"Вкажіть сумму заборгованості"})
    

    def clean_loan(self):
        data = self.cleaned_data["loan"]
        
        return data
    

    def clean_description(self):
        data = self.cleaned_data["description"]
        if data == "":
            changed_data = self.cleaned_data["description"]
            changed_data = "-"
            return changed_data
        
        return data
    

    def clean_amount(self):
        data = self.cleaned_data["amount"]
        return data
    
    def save(self):
        from .views import remote_addr,remote_email
        
        new = Table.objects.create(
            loan = self.cleaned_data["loan"],
            description = self.cleaned_data["description"],
            amount = self.cleaned_data["amount"],
            email = remote_email[remote_addr["email"]]
        )
        return new



class RegForm(forms.ModelForm):
    class Meta:
        model = Regestration
        fields = ["email","password"]
        labels = {"email":"","password":""}
        widgets = {
            "email": forms.TextInput(attrs={"class":"form-control","style":"width: 250px","placeholder":"example@gmail.com"}),
            "password": forms.TextInput(attrs={"class":"form-control","style":"width: 250px;margin-top:1em","placeholder":"123456"}),
            "errors":forms.TextInput(attrs={"style":"background-color:#ffff00"})
        }
        


    def clean_email(self):
        data = self.cleaned_data["email"]
        if Regestration.objects.filter(email=data).exists():
            raise forms.ValidationError("Аккаунт з такою адресою вже зареєстрований")
            
        return data
        

        
        
    

     
    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return data
    

    def save(self):
        new = Regestration.objects.create(
            email = self.cleaned_data["email"],
            password = self.cleaned_data["password"]


        )


        return new