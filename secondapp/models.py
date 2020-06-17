from django.db import models
from django.contrib.auth.models import User




class Note(models.Model):
    author = models.CharField(max_length=200,name="author")
    note = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=300,null=True)
    published = models.DateTimeField(auto_now_add=True,db_index=True)

    def __str__(self):
        return self.note

    class Meta:
        ordering = ["-published"]




class Table(models.Model):
    author = models.CharField(max_length=200,name="author")
    loan = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()

    def __str__(self):
        return self.loan

    def __str__(self):
        return self.description
    
    

    
