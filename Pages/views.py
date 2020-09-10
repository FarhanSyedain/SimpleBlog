from django.shortcuts import render,get_object_or_404,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages import success,error

from rest_framework.decorators import api_view
from rest_framework.response import Response

from Configrations.models import *
from Configrations.forms import *

from random import choice
import json



def home_page(request):
    
    featured_blogs = BlogPost.objects.filter(featured=True,released=True)[:3]
 
    count = 1
    featured_blogs_ = {} 
    for i in featured_blogs:
        featured_blogs_.update({count:i})
        count+= 1
    featured_blogs = featured_blogs_

    random_post = choice(list(BlogPost.objects.all()))

    content = {'featured_blogs':featured_blogs,'random_post':random_post,'page':'home','is_staff':is_staff(request)}
    
    return render(request,'index.html',content)


def search_page(request,search_query):
    
    top_stories = sorted(BlogPost.objects.filter(released=True),key=lambda x: x.relivence,reverse=True)[:6]
    
    content = {'page':'search','search_query':search_query,'trending':top_stories,'is_staff':is_staff(request)}
    
    return render(request,'search.html',content)


def catogory_page(request,category):
    
    top_stories = sorted(BlogPost.objects.filter(released=True),key=lambda x: x.relivence,reverse=True)[:6]
    
    content = {'page':'category','category':category,'trending':top_stories,'is_staff':is_staff(request)}
    
    return render(request,'catagory.html',content)


def tag_page(request,tag):
    
    top_stories = sorted(BlogPost.objects.filter(released=True),key=lambda x: x.relivence,reverse=True)[:6]
    
    content = {'page':'tag','tag':tag,'trending':top_stories,'is_staff':is_staff(request)}
    
    return render(request,'catagory.html',content)


def contact_page(request):
    
    feedback_send = False
    feedback_failed = False
    
    if request.method == 'POST':
        
        email = request.POST.get('email')
        name = request.POST.get('name')
        msg = request.POST.get('message')
        try:
            send_mail(
                f'Massage from {name}',
                f'with email{email} {name} sent {msg}',
                settings.EMAIL_HOST_USER,
                ['the email you want to send msg to'],
                fail_silently=False,
            )
            feedback_send = True
        
        except:
            feedback_failed = True
            feedback_send = False
            
    content = {'feedback_send':feedback_send,'feedback_failed':feedback_failed,'page':'contact','is_staff':is_staff(request)}
            
    return render(request,'contact.html',content)


def view_blog(request,slug):
    
    featured_blogs = BlogPost.objects.filter(featured=True,released=True)[:3]
    blog = get_object_or_404(BlogPost,slug=slug)
    if not (blog.released and is_staff(request)):
        return
    blog.views = blog.views + 1
    
    if request.user.is_authenticated:
        history = Profile.objects.get(user=request.user).history     
        if history is None:
            history = {f'{blog.category}':1}
        else:
            try:
                history = json.loads(history)
            except:
                history = {}
            try:
               history[blog.category.category] = history[blog.category.category] + 1
            except KeyError:
                history[blog.category.category] = 1
                
        obj = Profile.objects.get(user=request.user)
        obj.history  = json.dumps(history)
        obj.save()
        check = False
    else:
        check = True
        
    blog.save()
    
    if request.user.is_authenticated:
        has_liked = False
        follows_author = False
        
        if request.user in blog.stars.all():
            has_liked = True
        
        obj, created = Following.objects.get_or_create(user=Profile.objects.get(user=request.user))
        
        if User.objects.get(username=blog.author.username) in  obj.users_following.all():
            follows_author = True



        
    content = {'follows_author':follows_author,'has_liked':has_liked,'blog':blog,'check':check,'featured_blogs':featured_blogs,'page':'blog','is_staff':is_staff(request)}
    
    return render(request,'single-blog.html',content)


@api_view(['POST'])
def edit_history(request):
    if request.user.is_authenticated:
        return Response({''})
    data = request.data 
    id_ = data['id']
    category = data['category']
    
    if id_ is None:
        #create a new object
        
        obj = UserHistories()
        obj.history = json.dumps({category:1})
        obj.save()
        
        return Response({'id':obj.id})
    
    else:
        #Configure previus model
        
        try:
            obj = UserHistories.objects.get(id=id_)
            history = obj.history
            if history is None:
                history = {}
            else:
                history = json.loads(history)
            
            try:
                history[category] = history[category] + 1
            
            except:
                history[category] = 1
                
            obj.history = json.dumps(history)
            obj.save()
            
            return Response({'do':False})
        
        except:
            obj = UserHistories()
            obj.history = json.dumps({category:1})
            obj.save()
        
            return Response({'id':obj.id})
        

def login_user(request):
    
    incorrect_cred = False
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if not user is None:
            login(request,user)
            if request.POST.get('remember_me') is None:
                request.session.set_expiry(0)
            return redirect('home_page')
        incorrect_cred = True
    
    return render(request,'login.html',{'incorrect_cred':incorrect_cred,'page':'login','is_staff':is_staff(request)})


def register_user(request):
    
    form = CreateUser()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request,username=username,password=password)
            if not user is None:
                login(request,user)
                return redirect('home_page')
            return redirect('login')
        
    return render(request,'register.html',{'form':form,'page':'register','is_staff':is_staff(request)})


def logout_user(request):
    
    if request.user.is_authenticated:
        logout(request)
    return redirect('home_page')


def my_posts(request):
    
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user,is_staff=True).exists():
            return render(request,'admin.html',{'page':'admin','is_staff':is_staff(request)})
    
    return redirect('home_page')


def is_staff(request):
    if request.user.is_authenticated:
        return Profile.objects.filter(user=request.user,is_staff=True).exists()
    return False


def staff_profile(request,username):
    if Profile.objects.filter(username=username,is_staff=True).exists():
        user = Staff.objects.get(user=get_object_or_404(Profile,username=username))
        content = {'user':user}
        
        return render(request,'Profile.html',content)
    
def update_user(request):
    
    if request.user.is_authenticated:
        username_found = False
         
        if Profile.objects.get(user=request.user).is_staff:
            is_staff = True
            staff_form = Update_Staff(instance=Staff.objects.get(user=Profile.objects.get(user=request.user)))
        else:
            is_staff = False
            staff_form = None
            
        form = UpdateUser(request.user)
        
        if request.method == 'POST':
            
            if not request.POST.get('new_password1') is None and request.POST.get('new_password2') is None:
                form = UpdateUser(request.user,request.POST)
                
                if form.is_valid():
                    form.save()
                    
            new_username = request.POST.get('username')
            new_full_name = request.POST.get('name')
            user = Profile.objects.get(user=request.user)
            
            if not new_username == request.user.username:
                
                if Profile.objects.filter(username=new_username).exists():
                    username_found = True 
                else:
                    user.username = new_username
                    username_found = False 
                    
            if not new_full_name is None:
                user.name  = new_full_name
            
            user.save()
        
            if is_staff:
                staff_form = Update_Staff(request.POST,instance=Staff.objects.get(user=user))
                if staff_form.is_valid():
                    staff_form.save()
            
        username = Profile.objects.get(user=request.user).username
        name = Profile.objects.get(user=request.user).name
        
        content = {'form':form,'staff_form':staff_form,'username':username,'name':name,'incorrect':username_found}  
            
        return render(request,'edit_profile.html',content)
    return redirect('login_page')

