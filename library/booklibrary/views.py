from django.shortcuts import render,redirect,reverse
from django.http import request,HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail,send_mass_mail
from .models import *
from PIL import Image,ImageDraw,ImageFont
import random,io
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired
# Create your views here.

def index(request):
    hotpics = Hotpic.objects.all().order_by('index')
    messages = Message.objects.all()
    return render(request,'booklibrary/index.html',{'hotpics':hotpics,'messages':messages})


def login(request):
    return render(request,'booklibrary/reader_login.html')


def loginhandler(request):
    username = request.POST['username']
    pwd = request.POST['password']
    verifycode = request.POST["verifycode"]

    try:
        stu = StudentUser.objects.get(username=username)
        # print(stu.password,pwd)
        if stu.is_active:
            if stu.password == pwd:
                if verifycode == request.session["verifycode"]:
                    return render(request, 'booklibrary/reader.html', {'stu': stu})
                else:
                    return HttpResponse("验证码错误")
                # return render(request,'booklibrary/reader.html',{'stu':stu})
                # return HttpResponse('success')
            else:
                return render(request, 'booklibrary/reader_login.html', {'error': '密码错误'})
        else:
            return render(request, 'booklibrary/reader_login.html', {'error': '账户未激活'})
    except:
        # return HttpResponse('error')
        return render(request, 'booklibrary/reader_login.html', {'error': '用户名或密码错误'})


def verify(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20,100),
    random.randrange(20,100),
    random.randrange(20,100))
    width = 100
    heigth = 25
    # 创建画面对象
    im = Image.new('RGB',(width,heigth),bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, heigth))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('pala.ttf', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    request.session['verifycode'] = rand_str
    f = io.BytesIO()
    im.save(f,'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')


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

    try:
        if pwd == cpwd:
            user = StudentUser()
            user.username = username
            user.password = pwd
            user.college = college
            user.sno = sno
            user.email = email
            user.is_active = False


            user.save()
            id = StudentUser.objects.get(username = username).id
            serutil = Serializer(settings.SECRET_KEY,300)
            idstr = serutil.dumps({'userid':id}).decode('utf-8')
            send_mail('激活账户', '<a href = "http://127.0.0.1:8000/booklibrary/active/%s">点击激活</a>' % (idstr,),settings.DEFAULT_FROM_EMAIL,[email])
            return redirect(reverse('booklibrary:login'))
    except:
        return HttpResponse('error')


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
        if reader.status == False:
            reader = None
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
            if reader.status:
                print("aaaaaaaaaaa")
                error = '借阅过'
            else:
                saveborrowinfo(bookid, stuid)
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


def edit(request):
    if request.method == 'GET':
        return render(request,'booklibrary/edit.html')
    elif request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        msg = Message(title = title, message = message)
        msg.save()
        return redirect(reverse('booklibrary:index'))


def email(request):
    try:
        send_mail('Django send email','django send email',settings.DEFAULT_FROM_EMAIL,['1195741928@qq.com'])
    except:
        return HttpResponse('send error')

    return HttpResponse('send success')

def active(request,idstr):
    try:
        dser = Serializer(settings.SECRET_KEY,300)
        obj = dser.loads(idstr)
        user = StudentUser.objects.get(id=obj['userid'])
        user.is_active = True
        user.save()
        return redirect(reverse('booklibrary:login'))
    except SignatureExpired as e:
        return HttpResponse('error')


def ajax(request):
    return render(request,'booklibrary/ajax.html')

def ajaxajax(request):
    return HttpResponse('success')


def echarts(request):
    return render(request,'booklibrary/echarts.html')










