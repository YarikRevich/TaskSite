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
from secondapp.views import ath,Home,CreateNote,TableEdit,Edit,EditEntrypage,Sheet,Reg,DeleteTable

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path("",ath,name="Forma"),
    path("homepage/",Home.as_view(),name="Home"),
    path("homepagee/sheet",Sheet.as_view(),name="Sheet"),
    path("homepagee/",CreateNote.as_view(),name="Note"),
    path("/tableedit/",TableEdit.as_view(),name="TableEdit"),
    path("regestration/",Reg.as_view(),name="Reg"),
    path("deletetable/",DeleteTable.as_view(),name="DeleteTable"),
    path("editpage/",Edit.as_view(),name="Edit"),
    path("editpage/editentry/",EditEntrypage.as_view(),name="EditEntryPage"),
    
    
    
]
