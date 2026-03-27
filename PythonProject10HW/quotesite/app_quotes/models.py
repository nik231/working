from django.db import models

import json

class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField()
    born_location = models.CharField(max_length=200)
    description = models.TextField()
    #created_at = models.DateField(auto_now_add=True)

   # def __str__(self):
      #  return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)
    quote = models.TextField()
    #created_at = models.DateField(auto_now_add=True)


    #def get_tags(self):
     #   """Get tags as a Python list"""
      #  # JSONField already returns the value as a Python object
       # if isinstance(self.tags, list):
        #    return self.tags
       # return []

   # def __str__(self):
      #  return self.quote[:50]
