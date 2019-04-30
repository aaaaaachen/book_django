from django.conf.urls import url
from . import views

app_name = 'booklibrary'


urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'login/$',views.login,name='login'),
    url(r'register/$',views.register,name='register'),
    url(r'loginhandler/$',views.loginhandler,name='loginhandler'),
    url(r'registerhandler/$',views.registerhandler,name='registerhandler'),
    url(r'checkstuinfo/(.*?)/$',views.checkstuinfo,name='checkstuinfo'),
    url(r'updatestuinfo/(.*?)/$',views.updatestuinfo,name='updatestuinfo'),
    url(r'checkbook/(.*?)/$',views.checkbook,name='checkbook'),
    url(r'bookdetail/(.*?)/(.*?)/$',views.bookdetail,name='bookdetail'),
    # url(r'borrow/(.*?)/(.*?)/$',views.borrow,name='borrow'),
    url(r'show_borrows/$',views.show_borrows,name='show_borrows'),
    url(r'upload/$',views.upload,name='upload'),
    url(r'edit/$',views.edit,name='edit'),
    url(r'email/$',views.email,name='email'),
    url(r'active/(\d+)/$',views.active,name='active'),

]

