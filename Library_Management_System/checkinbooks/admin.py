from django.contrib import admin
from . import models

admin.site.register(models.Book)
admin.site.register(models.Authors)
admin.site.register(models.BookAuthors)
admin.site.register(models.BookLoans)
admin.site.register(models.Borrower)
admin.site.register(models.Fines)