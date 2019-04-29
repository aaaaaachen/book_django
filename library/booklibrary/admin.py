from django.contrib import admin

# Register your models here.

from .models import *

class AdminStudentUser(admin.ModelAdmin):
    list_display = ['username','sno']
    search_fields = ['username','sno']


admin.site.register(StudentUser,AdminStudentUser)

class AdminBook(admin.ModelAdmin):
    list_display = ['bookname','author']
    search_fields = ['bookname','author']

admin.site.register(Book,AdminBook)


class AdminHistory(admin.ModelAdmin):
    list_display = ['status','date_borrow','date_return']

admin.site.register(History,AdminHistory)
admin.site.register(Hotpic)