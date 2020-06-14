from django.contrib import admin

from .models import Note,Table



class NoteModel(admin.ModelAdmin):
	list_display = ("author","note","published")
	search_fields = ["author"]
	

class TableModel(admin.ModelAdmin):
	list_display = ("author","loan","description","amount")
	
	


admin.site.register(Note,NoteModel)
admin.site.register(Table,TableModel)


