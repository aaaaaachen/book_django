from django.shortcuts import render,redirect,reverse
from django.http import request,HttpResponse,HttpResponseRedirect

from .models import *
# Create your views here.

def index(request):
    hotpics = Hotpic.objects.all().order_by('index')
    return render(request,'booklibrary/index.html',{'hotpics':hotpics})


def login(request):
    return render(request,'booklibrary/reader_login.html')

def loginhandler(request):
    username = request.POST['username']
    pwd = request.POST['password']
    try:
        stu = StudentUser.objects.get(username=username)
        # print(stu.password,pwd)

        if stu.password == pwd:
            return render(request,'booklibrary/reader.html',{'stu':stu})
            # return HttpResponse('success')
        else:
            return render(request, 'booklibrary/reader_login.html', {'error': '密码错误'})
    except:
        # return HttpResponse('error')
        return render(request, 'booklibrary/reader_login.html', {'error': '用户名或密码错误'})

def register(request):
    return render(request,'booklibrary/register.html')

def registerhandler(request):
    username = request.POST['username']
    pwd = request.POST['password']
    cpwd = request.POST['password2']
    college = request.POST['college']
    sno = request.POST['number']
    email = request.POST['email']
    print(username,pwd,cpwd,college,sno,email)

    if pwd == cpwd:
        user = StudentUser()
        user.username = username
        user.password = pwd
        user.college = college
        user.sno = sno
        user.email = email

        user.save()

        return redirect(reverse('booklibrary:login'))


def checkstuinfo(request,id):
    user = StudentUser.objects.get(pk = id)

    return render(request,'booklibrary/reader_info.html',{'user':user})

def updatestuinfo(request,id):
    if request.method == 'GET':
        user = StudentUser.objects.get(pk = id)
        print(user)
        return render(request,'booklibrary/reader_modify.html',{'user':user})
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        college = request.POST['college']
        sno = request.POST['number']
        email = request.POST['email']
        user = StudentUser.objects.get(pk = id)
        user.username = username
        user.college = college
        user.sno = sno
        user.email = email

        if pwd == '':
            pwd = user.password
            user.password = pwd
            print(username,pwd,college,sno,email)
            user.save()
        else:
            user.password = pwd
            user.save()

        return redirect(reverse('booklibrary:checkstuinfo',args=(user.id,)))

def checkbook(request,id):
    stu = StudentUser.objects.get(pk = id)
    # print(stu)
    # return HttpResponse('success')
    if request.method == 'GET':
        return render(request,'booklibrary/reader_query.html',{'stu':stu})

    if request.method == "POST":
        option = request.POST['item']
        check = request.POST['query']
        try:
            if option == 'name':
                books = Book.objects.all().filter(bookname = check)
                print(books)
                # return HttpResponse('success')
                return render(request, 'booklibrary/reader_query.html', {'stu': stu, 'books': books})
            elif option == 'author':
                books = Book.objects.all().filter(author = check)
                print(books)
                return render(request, 'booklibrary/reader_query.html', {'stu': stu, 'books': books})
        except:
            return HttpResponse('error')

def bookdetail(request,bookid,stuid):
    stu = StudentUser.objects.get(pk = stuid)
    book = Book.objects.get(pk = bookid)
    try:
        reader = History.objects.all().filter(book =book).filter(status = True)[0]
        print(reader)
    except:
        reader = None
    if request.method == "GET":

        return render(request,'booklibrary/reader_book.html',{"book":book,'reader':reader,'stu':stu})
    elif request.method == 'POST':
        if reader is None:
            error = None
            saveborrowinfo(bookid,stuid)

            print(type(reader))
            return HttpResponseRedirect('/booklibrary/bookdetail/' + str(book.id) + '/' + str(stu.id) + '/',{"error": error})

            # return reader(request,'booklibrary/reader_book.html',{"book":book,'reader':reader,'stu':stu})
        else:
            print("aaaaaaaaaaa")
            error = '借阅过'
            return render(request, 'booklibrary/reader_book.html', {"book": book, 'reader': reader, 'stu': stu, "error":error})


def saveborrowinfo(bookid,stuid):
    stu = StudentUser.objects.get(pk=stuid)
    book = Book.objects.get(pk=bookid)
    borrow = History()
    borrow.user = stu
    borrow.book = book
    borrow.status = True
    borrow.save()


def show_borrows(request):
    borrows = History.objects.all()
    return render(request,'booklibrary/reader_histroy.html',{'histroys':borrows})


def upload(request):
    if request.method == 'GET':
        return render(request,'booklibrary/reader_upload.html')
    if request.method == 'POST':
        name = request.POST['name']
        index = request.POST['index']
        pic = request.FILES['pic']

        hot = Hotpic(name= name,index= index,pic = pic)
        hot.save()
        return redirect(reverse('booklibrary:index'))







