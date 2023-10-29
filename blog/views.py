from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')


def contact(request):
    return render(request,'blog/contact.html')

def dashboard(request):

    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        fullname=user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/dashboard.html',{"posts":posts,'fullname':fullname,'gps':gps})
    else:
        return HttpResponseRedirect('/login/')

def user_signup(request):

    if request.method == 'POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'congratulations you have become an Author!!! ')
            user=form.save()
            group=Group.objects.get(name='author')
            user.groups.add(group)
            form=SignupForm()
    else:
        form=SignupForm()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
        form=LoginForm(request=request,data=request.POST)
        if form.is_valid():
            un=form.cleaned_data['username']
            pw=form.cleaned_data['password']
            user=authenticate(username=un,password=pw)
            if user is not None:
                login(request,user)
                messages.success(request,'you have logged in sucessfully!')
                return HttpResponseRedirect('/dashboard/')
          
    else:
        form=LoginForm()
   
    return render(request,'blog/login.html',{'form':form})
  else:
      return HttpResponseRedirect('/dashboard/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#add post to blog
def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                messages.success(request,'You have suceffully added your blog!!')
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
