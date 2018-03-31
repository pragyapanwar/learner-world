from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django import forms
from .forms import SignupForm ,UserFormlog,ProfileForm ,AddResourceForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
#from django.contrib.auth.models import check_password
from django.core.mail import EmailMessage
from django.contrib import auth
from .models import Profile,subject,subcategory,resource
from django.shortcuts import render_to_response, get_object_or_404
from register.functions import add_mmkey 
from register.bs import score 

#from django.contrib.auth.models import check_password

def index(request,string=None):
  msgs=''
  a=string
  profile_form=ProfileForm(request.GET)
  template = a+'.html'
  if a=='profile':
    if request.user.username:
      # for empty form
      user= request.user
      p_user = Profile.objects.get(user=user)
      if p_user.status==1:
        return redirect('/profile_display/' )
      if request.method == 'GET':
  
        return render(request, template,{'profile_form':profile_form})

       # for submission of profile form
      if request.method == 'POST':
           profile_form =ProfileForm(request.POST,request.FILES)
           user1= request.user
           iduser=user1.pk
           user_pro=Profile.objects.get(user=user1)
           if profile_form.is_valid() :
             ab="form all ok"       
             #puser1= profile_form.save(commit=False)
           
           #prof= profile_form.save()
             user_pro.full_name = profile_form.cleaned_data['full_name']
             user_pro.about_yourself = profile_form.cleaned_data['about_yourself']
             user_pro.Education = profile_form.cleaned_data['Education']
             user_pro.Experience = profile_form.cleaned_data['Experience']
             user_pro.skills = profile_form.cleaned_data['skills']
             user_pro.Work = profile_form.cleaned_data['Work']
             user_pro.interst1 = profile_form.cleaned_data['interest1']
             
             user_pro.status = 1
             
             pp=request.FILES.get('profile_photo')
             res=request.FILES.get('resume')
             print user_pro.full_name
             print pp
             

             if pp:
              user_pro.profile_photo=request.FILES['profile_photo']#,False]
              user_pro.resume=request.FILES['resume']#,False]

           user_pro.save() 
           user1.save()
           return render(request, 'profile_display.html',{'pro':user_pro})
  
           #else:
            # user1._profile_photo='abc1.jpg'
           
           
    else:
       template='login.html'
      # profile_form =ProfileForm(request.GET)
       return redirect('/login/')

  return render(request, template,{'profile_form':profile_form})


# this view is responsible for ADDING A NEW RESOURCE IN THE DATABASE
def add_resource(request):

  form=AddResourceForm(request.GET)
  
  if request.method == 'GET':

     return render(request, 'add_resource.html', {
        'form': form    #user_form
       })
    
  if request.method == 'POST':
           msg="Your resource has been successfully added"
           add_form =AddResourceForm(request.POST)
           user1= request.user
           #user_pro=Profile.objects.get(user=user1)
           if add_form.is_valid() :
             #ab="form all ok"       
             #puser1= profile_form.save(commit=False)
           
           #prof= profile_form.save()
             subject_name = add_form.cleaned_data['subject_name']
             subcate = add_form.cleaned_data['subcategory']
             details = add_form.cleaned_data['details']
             url = add_form.cleaned_data['url']

             # adding fields in the database
             
             subj= subject.objects.create(name=subject_name)
             subj.userid.add(user1)
             cate= subcategory.objects.create(name=subcate)
             cate.subid.add(subj)


             #calculation of score
             score_url= score(url,details)
             res= resource.objects.create(url_field=url,score=score_url)
             res.catid.add(cate)
             
             return render(request, 'add_resource.html',{'form': form,'msg':msg, 'score': score_url})
  
           #else:
            # user1._profile_photo='abc1.jpg'
           
           
           else:
             msg=" Some error occured"
             template='add_resource.html'
             return render(request, 'add_resource.html', {
                 'form': form    #user_form
                })  
      # here zoya u could manipulate the things add ur validation methods
  return render(request, 'add_resource.html', {
        'form': form    #user_form
       })    

  
# from here user login starts
def logout(request):
  auth.logout(request)
  return render(request, 'logout.html')

def login(request,string=None):
  if request.method == 'GET':
         user_form = UserFormlog(request.GET)
         return render(request, 'login.html', {
        'user_form': user_form    #user_form
    })

  if request.method == 'POST':
        user_form1 = UserFormlog(request.POST)
        user_form = UserFormlog(request.GET)
       
        if user_form1.is_valid() :
           ab="post chala"       
     
           #prof= profile_form.save()
           username = user_form1.cleaned_data['username']
           password = user_form1.cleaned_data['password']
           #profile=profile_form.save(commit=False)
           #profile.user_id=user1.id+1
           #profile.college=profile_form.cleaned_data['college']
           #profile.save()
         
           user1 = authenticate(username=username ,password=password)
           print user1
           if user1 :
             print "db me hai"
             
             ab="db me hai"
           else:
             print "db me nai hai"
           if user1 :
             auth.login(request, user1)
                #return redirect('index.html')
             return redirect('/index/')#render(request,'contribute.html',{ 'student': user1 })#,{'user_form':user_form} )
              
           else:
                #return redirect('nope.html')
                return redirect('/login/')  #render(request,'nope.html')
        
           #profile_form.save()
            #return redirect('settings:profile')
        
  return render(request, 'login.html', {'user_form': user_form })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def profile_update(request): #,uid=None):
  msgs=''
  user1= request.user
  uid=Profile.objects.filter(user=user1).first().id
  instance = get_object_or_404(Profile,id=uid)
  post_form=ProfileForm(request.POST or None,instance=instance)
  button="update profile"
  
  user_pro=Profile.objects.get(user=user1)
                   
  if post_form.is_valid() :
           ab="post chala"       
           post = post_form.save(commit=False)
            
           #prof= profile_form.save()
           user_pro.full_name = post_form.cleaned_data['full_name']
           user_pro.about_yourself = post_form.cleaned_data['about_yourself']
           user_pro.Education = post_form.cleaned_data['Education']
           user_pro.Experience = post_form.cleaned_data['Experience']
           user_pro.skills = post_form.cleaned_data['skills']
           user_pro.Work = post_form.cleaned_data['Work']
           user_pro.profile_status=1
           pp=request.FILES.get('profile_photo')
           res=request.FILES.get('resume')
           

           if pp:
              user_pro.profile_photo=request.FILES['profile_photo']#,False]
              user_pro.resume=request.FILES['resume']#,False]
           
           #profile=profile_form.save(commit=False)
           #profile.user_id=user1.id+1
           #profile.college=profile_form.cleaned_data['college']
           #profile.save()
         
           post.save()
           msgs=" Post Updated!" 
               #return redirect('index.html')
           return render(request, 'profile.html',{'profile_form':post_form})
   
  else:
             msgs=""
             button="update profile"
             return render(request, 'profile.html',{'profile_form':post_form})
   
  return render(request, 'profile.html',{'profile_form':post_form})
   

def profile_display(request):
 if  request.user.username:
     
   user=request.user
   pro= Profile.objects.filter(user=user).first()
   print pro
   #pro='kl'
   return render(request, 'profile_display.html',{'pro':pro})
 else:
   return redirect('/login/')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
