from django.shortcuts import render,redirect, HttpResponse,Http404
from .models import Regestration,Note,Table
from django.template import loader
from django.views.generic import View
from .forms import Forma,TableForm,RegForm
from django.db import IntegrityError
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.db.models import Sum
from functools import wraps


#Specially made dictionary and list for the next actions

user_dict = {}
acc_email = {}
remote_addr = {}
remote_email = {}
global check_list
notath = False
ckeck_list = []


########################################################








def ath(request):
    
    if request.method == 'GET':
        if request.GET:
            b = request.GET.get("password")
            a = request.GET.get("email")
            if len(Regestration.objects.all()) > 0:
                for i in Regestration.objects.all():
                    if i.email == a:
                        if i.password == b:
                            ckeck_list.clear()
                            ckeck_list.append(a)
                            user_dict[a] = 1
                            remote_addr["email"] = request.META["REMOTE_ADDR"]
                            remote_email[remote_addr["email"]] = a
                            #acc_email[request.META["REMOTE_ADDR"]] = a
                            return redirect("/homepage/")
                            
                
                return render(request, "secondapp/firstpage.html",context={"succes":1,"notath":notath})
            else:
                
                return render(request, "secondapp/firstpage.html",context={"succes":1,"notath":notath})
        
        return render(request, "secondapp/firstpage.html",context={"succes":0})
    if request.method == "POST":
        if request.POST:
            emailPost = request.POST.get("email")
            if len(Regestration.objects.all()) > 0:
                for i in Regestration.objects.all():
                    if i.email == emailPost:  
                        ckeck_list.clear()
                        ckeck_list.append(emailPost)
                        user_dict[emailPost] = 1
                        return redirect("/homepage/")
        
                
                return render(request, "secondapp/firstpage.html",context={"succes":1,"notath":notath})
            else:
                
                return render(request, "secondapp/firstpage.html",context={"succes":1,"notath":notath})
        
        return render(request, "secondapp/firstpage.html",context={"succes":0})
            



class Home(View):
    
    def autorized(func):
        def wrapper(self,request,*args, **kwargs):
            try:
                a = ckeck_list[0]
                if len(a) > 0:
                    if user_dict[a] >= 1:   
                        return func(self,request)
                    return render(request, "secondapp/firstpage.html",context={"succes":1,"notath":notath})
                else:
                    return render(request, "secondapp/firstpage.html",context={"notath":1})
            except IndexError:
                return render(request, "secondapp/firstpage.html",context={"notath":1})
        return wrapper

    _autorized = staticmethod(autorized)




    @autorized
    def get(self,request,*args, **kwargs):

        
        notes = Note.objects.filter(note_email=remote_email[remote_addr["email"]])
        table = Table.objects.filter(email=remote_email[remote_addr["email"]])
        result = table.aggregate(su = Sum("amount"))
        sum_table = result["su"]
        if sum_table == None:
            sum_table = 0
        return render(request,"secondapp/homepage.html",context={"notes":notes,"email":remote_email[remote_addr["email"]],"form":table,"sum":sum_table})
            
    def post(self,request,*args, **kwargs):
        ckeck_list.clear()
        return redirect("/")





"""
Clases for the note part 


"""




class Edit(Home):
    notepk = 0 


    @Home._autorized
    def get(self,request,*args, **kwargs):
        setattr(Edit,"pk",request.GET.get("note"))
        try:
            setattr(Edit,"notepk",Note.objects.get(pk=self.pk))
        except ObjectDoesNotExist:
            return Http404()                
        note = self.notepk.note
        return render(request,"secondapp/edit.html",context={"note":note,"email":remote_email[remote_addr["email"]]})
        
    def post(self,request,*args, **kwargs):
        self.notepk.delete()
        return redirect("/homepage/")




    


class EditEntrypage(Edit):

    @Home._autorized
    def get(self,request,*args, **kwargs):
        note = self.notepk.note
        return render(request,"secondapp/editentry.html",context={"note":note,"email":remote_email[remote_addr["email"]]})


    def post(self,request,*args, **kwargs):
        notetochange = request.POST.get("changednote")
        update = Note.objects.filter(pk=self.pk).update(note=notetochange)
        return redirect("/homepage/")







"""


Classes for the sheet part



"""






class Sheet(EditEntrypage):

    @Home._autorized
    def get(self,request,*args, **kwargs):
        form = TableForm()
        return render(request,"secondapp/table.html",context={"form":form,"email":remote_email[remote_addr["email"]]})

    def post(self,request,*args, **kwargs):
        bound = TableForm(request.POST)
        if bound.is_valid():
            bound.save()
            return redirect("Home")
        return Http404()






class TableEdit(View):

    @Home._autorized
    def get(self,request,*args, **kwargs):
            for i in request.GET:
                if i == "loan":
                    table_pk = request.GET["loan"]
                    setattr(TableEdit,"pk",table_pk)
                    setattr(TableEdit,"loan",True)
                    table = Table.objects.get(pk=table_pk)
                    table_loan = table.loan
                    return render(request,"secondapp/tableedit.html",context={"table":table_loan,"stat":"loan","email":remote_email[remote_addr["email"]]})
                elif i == "description":
                    table_pk = request.GET["description"]
                    setattr(TableEdit,"pk",table_pk)
                    table = Table.objects.get(pk=table_pk)
                    table_loan = table.description
                    return render(request,"secondapp/tableedit.html",context={"table":table_loan,"stat":"description","email":remote_email[remote_addr["email"]]})
                elif i == "amount":
                    table_pk = request.GET["amount"]
                    setattr(TableEdit,"pk",table_pk)
                    table = Table.objects.get(pk=table_pk)
                    table_loan = table.amount
                    return render(request,"secondapp/tableedit.html",context={"table":table_loan,"stat":"amount","email":remote_email[remote_addr["email"]]})

    def post(self,request,*args, **kwargs):
        error = True
        if request.POST.get("loan") != None:
            Table.objects.filter(pk=self.pk).update(loan=request.POST["loan"])
            error = False
            return redirect("Home")
        elif request.POST.get("description") != None:
            Table.objects.filter(pk=self.pk).update(description=request.POST["description"])
            error = False
            return redirect("Home")
        elif request.POST.get("amount") != None:
            try:
                Table.objects.filter(pk=self.pk).update(amount=request.POST["amount"])
                error = False
                return redirect("Home")
            except ValueError:
                if request.POST.get("amount") == "-":
                    Table.objects.filter(pk=self.pk).update(amount=0)
                    error = False
                    return redirect("Home")
                error = True
                return render(request,"secondapp/tableedit.html",context={"error":error,"table":"","stat":"amount"})

class DeleteTable(View):

    @Home._autorized
    def get(self,request,*args, **kwargs):
        return redirect("Home")

    @Home._autorized
    def post(self,request,*args, **kwargs):
        if request.POST.get("loan") != None:
            print(request.POST)
            Table.objects.filter(loan=request.POST.get("loan")).delete()
            return redirect("Home")
        elif request.POST.get("description") != None:
            print(request.POST)
            Table.objects.filter(description=request.POST.get("description")).delete()
            return redirect("Home")
        elif request.POST.get("amount") != None:
            Table.objects.filter(amount=request.POST.get("amount")).delete()
            return redirect("Home")


class CreateNote(View):

    @Home._autorized
    def get(self,request,*args, **kwargs):
        form = Forma()
        return render(request,"secondapp/create.html",context={"form":form})

    def post(self,request):
        bound = Forma(request.POST)
        if bound.is_valid():   
            bound.save()
            return redirect("Home")
        return HttpResponse("IT is bad")




"""
A part for the regestration

"""

class Reg(View):

   
    def get(self,request,*args, **kwargs):


        form = RegForm()
        return render(request,"secondapp/regpage.html",context={"form":form})



    def post(self,request,*args, **kwargs):
        bound = RegForm(request.POST)
        if bound.is_valid():
            bound.save()
            return render(request,"secondapp/firstpage.html",context={"regestrated":True})
        return render(request,"secondapp/regpage.html",context={"form":bound})