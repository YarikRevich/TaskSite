"""second URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include

from secondapp.views import AuthorizationClass,TableEdit,EditNote,TaskMenu,RegestrationClass,DeleteTable,Profile,DeleteNote,HomePage,LogoutClass,CreateNoteClass,CreateTableClass


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    path("",AuthorizationClass.as_view(),name="Authorization"),
    path("regestration/",RegestrationClass.as_view(),name="Regestration"),
    path("logout/",LogoutClass.as_view(),name="Logout"),

    path("homepage/table/option_name=<str:name_of_option>/<int:pk>",TableEdit.as_view(),name="TableEdit"),
    path("homepage/task/note_update/<int:pk>",EditNote.as_view(),name="EditNote"),
    path("homepage/task/note=<int:pk>",TaskMenu.as_view(),name="TaskMenu"),
    path("homepage/profile",Profile.as_view(),name="Profile"),
    path("homepage/note_delete/<int:pk>",DeleteNote.as_view(),name="DeleteNote"),
    path("homepage/task",CreateNoteClass.as_view(),name="Note"),
    path("homepage/table_delete/<int:pk>",DeleteTable.as_view(),name="DeleteTable"),
    path("homepage/sheets",CreateTableClass.as_view(),name="Sheet"),
    path("homepage/",HomePage.as_view(),name="Home"),
   
    
    
    
    #path("table_edit",TableEdit.as_view(),name="Edit"),
    
    #path("editpage/editentry/",DeleteTable.as_view(),name="DeleteTable"),
    
    
    
]
