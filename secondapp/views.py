from django.shortcuts import render,redirect, HttpResponse,Http404
from django.template import loader
from django.utils.decorators import method_decorator


from django.db import IntegrityError
from django.db.models import Sum

from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView,UpdateView,CreateView,ModelFormMixin


from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .forms import CreateRegestrationForm,CreateNoteForm,CreateTableForm,EditNoteForm,TableLoanUpdateForm,TableDescriptionUpdateForm,TableAmountUpdateForm
from .models import Note,Table
from .backends import EmailAndPasswordBackend



client = MongoClient(
        "localhost",
        27017
    )
db = client["taskbot"]
collection = db["tasksite"]






"""
Regestration and Authorization and Logout


"""



class RegestrationClass(View):

    def get(self,request,*args, **kwargs):
        form = CreateRegestrationForm()
        args = {
            "form":form
        }
        return render(request,"secondapp/regpage.html",args)

    def post(self,request,*args, **kwargs):
        form = CreateRegestrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Authorization")
        args = {
            "form":form
        }
        return render(request,"secondapp/regpage.html",args)
    


class AuthorizationClass(View):

    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/homepage/")
        return render(request,"secondapp/firstpage.html")

    def post(self,request,*args, **kwargs):
        user = authenticate(username=request.POST["email"],password=request.POST["password"])
        if user is not None:
            login(request,user)
            if collection.find_one({"_id":request.user.username}) == None:
                collection.insert_one({"_id":request.user.username,"password":request.POST["password"]})
            return redirect("Home")
        return redirect("Authorization")

class LogoutClass(View):
    def post(self,request,*args, **kwargs):
        logout(request)
        return redirect("Authorization")
            



"""
A showing of HomePage


"""

class HomePage(LoginRequiredMixin,TemplateView):
    template_name = "secondapp/homepage.html"
    login_url = "/"    

    def get(self,request,*args, **kwargs):

        list_of_tables = [[tables.loan,tables.description,tables.amount] for tables in Table.objects.filter(author=self.request.user.username)]
        collection.update(

            {"_id":self.request.user.username},
            {"$set":{"full_loan":list_of_tables}}

        )

        collection.update(

            {"_id":self.request.user.username},
            {"$set":{"loan":Table.objects.filter(author=self.request.user.username).aggregate(su = Sum("amount"))["su"]}}
            
        )
        
        
        args = {
            "email":request.user.username,
            "notes":Note.objects.filter(author=request.user.username),
            "form":Table.objects.filter(author=request.user.username),
            "sum":Table.objects.filter(author=self.request.user.username).aggregate(su = Sum("amount"))["su"]
        }

        return self.render_to_response(args)
       

"""

A showing of your profile

"""

class Profile(TemplateView):
    template_name = "secondapp/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for info in collection.find({"_id":self.request.user.username}):
            try:
                context["name"] = info["connected_name"]
            except KeyError:
                context["name"] = "Ім'я не вказане"
            try:
                context["last_name"] = info["connected_last_name"]
            except:
                context["last_name"] = "Прізвище не вказане"
            try:
                context["connected"] = info["connected"]
            except:
                context["connected"] = False
        context["email"] = self.request.user.username 
        return context
    





"""
    
A creating of your entries

"""







class CreateNoteClass(LoginRequiredMixin,CreateView):
    template_name = "secondapp/create.html"
    form_class = CreateNoteForm
    login_url = "/"
    def form_valid(self,form):
        Note.objects.create(author=self.request.user.username,note=form.cleaned_data["note"])
        return redirect("Home")
        
    
class CreateTableClass(LoginRequiredMixin,CreateView):
    template_name = "secondapp/table.html"
    login_url = "/"
    form_class = CreateTableForm
    
    def form_valid(self,form):
        Table.objects.create(
            author = self.request.user.username,
            loan = form.cleaned_data["loan"],
            description = form.cleaned_data["description"],
            amount = form.cleaned_data["amount"]
        )
        return redirect("Home")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.user.username
        return context
    
    


"""
A deletion of your entries

"""


class DeleteNote(DeleteView):
    model = Note
    success_url = "/homepage/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.user.username
        return context
    

class DeleteTable(DeleteView):
    model = Table
    success_url = "/homepage/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.user.username
        return context


"""
A showing of task menu

"""



class TaskMenu(TemplateView):
    template_name = "secondapp/edit.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] =  self.request.user.username
        context["note"] = Note.objects.get(pk=self.kwargs["pk"])
        return context
    


"""

An updating of your entries

"""

class EditNote(UpdateView):
    queryset = Note.objects
    template_name = "secondapp/editentry.html"
    success_url = reverse_lazy("Home")
    form_class = EditNoteForm
    

class TableEdit(UpdateView,ModelFormMixin,SingleObjectMixin):
    queryset = Table.objects
    template_name = "secondapp/tableedit.html"
    success_url = reverse_lazy("Home")
    def get_form_class(self):
        if self.kwargs["name_of_option"] == "loan":
            self.form_class = TableLoanUpdateForm
            return self.form_class
        elif self.kwargs["name_of_option"] == "description":
            self.form_class = TableDescriptionUpdateForm
            return self.form_class
        elif self.kwargs["name_of_option"] == "amount":
            self.form_class = TableAmountUpdateForm
            return self.form_class
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_pk"] = self.kwargs["pk"]
        return context
    
        
        
    
    