from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta,datetime
from tinymce.models import HTMLField
# import datetime
# Create your models here.
class StudentUser(User):
     college = models.CharField(max_length=20,null=True,blank=True)
     sno = models.IntegerField(null=True,blank=True)
     def __str__(self):
          return self.username



class Book(models.Model):
     bookname = models.CharField(max_length=20)
     author = models.CharField(max_length=20)
     publish_com = models.CharField(max_length=20)
     publish_date = models.DateField()
     def __str__(self):
          return self.bookname

class History(models.Model):
     book = models.ForeignKey(Book,on_delete=models.CASCADE)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     date_borrow = models.DateTimeField(default=datetime.now())
     date_return = models.DateTimeField(default=datetime.now()+timedelta(days=30))
     status = models.BooleanField()


class Hotpic(models.Model):
    name = models.CharField(max_length=20)
    index = models.SmallIntegerField(unique=True)
    pic = models.ImageField(upload_to='hotpic')

    def __str__(self):
        return self.name

class Message(models.Model):
    title = models.CharField(max_length=30)
    message = HTMLField()

    def __str__(self):
        return self.title