from django.urls import path

from mainapp import views

app_name='main'

urlpatterns = [
    path('hostpage/',views.show_host,name='hostpage'),
    path('loginpage/',views.login_page,name='loginpage'),
    path('loginlogic/',views.login_logic,name='loginlogic'),
    path('get_code/',views.get_code,name='get_code'),
    path('add_newbanner/',views.add_newbanner,name='add_newbanner'),
    path('show_banners/',views.show_banners,name='show_banners'),
    path('banner/',views.banner,name='banner')

]