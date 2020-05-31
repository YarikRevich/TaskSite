from django.contrib import admin

from .models import Regestration,Note,Table

class RgModel(admin.ModelAdmin):
	list_display = ("email","password")
	search_fields = ("email","password")



class NoteModel(admin.ModelAdmin):
	list_display = ("note","published","note_email")
	exclude = ["note_email"]

class TableModel(admin.ModelAdmin):
	list_display = ("loan","description","amount","email")
	exclude = ['email']

admin.site.register(Regestration,RgModel)
admin.site.register(Note,NoteModel)
admin.site.register(Table,TableModel)


