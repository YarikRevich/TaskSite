from django.db import models

class Regestration(models.Model):
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=50)



class Note(models.Model):
    note = models.CharField(max_length=50)
    published = models.DateTimeField(auto_now_add=True,db_index=True)
    note_email = models.EmailField(max_length=254)
    class Meta:
        ordering = ["-published"]


class Table(models.Model):
    loan = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    email = models.EmailField(max_length=254)
    
