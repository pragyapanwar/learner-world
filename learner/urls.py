"""learner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# These two urls would make your media folder work
from django.conf.urls import url,include

from django.conf.urls.static import  static
from django.contrib import admin
from register.views import signup,activate,index,login,profile_display,profile_update,logout,add_resource
#import register.views
from django.conf.urls import include ,url
from django.conf import settings 
from django.contrib.auth import views as auth_views
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,{'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'},name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'password_reset_complete.html'},name='password_reset_complete'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^profile_display/$', profile_display, name='profile_display'),
    url(r'^add_resource/$', add_resource, name='add_resource'),
     
    url(r'^profile_update/$',profile_update,name='profile_update'),
    #(?P<uid>[0-9]+)/
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
     activate, name='activate'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$',logout, name='logout'),
 url(r'^(?P<string>[\w\-]+)/$',index,name='index'),
  
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
