from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import simplejson as json

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail

from django.http import HttpResponse,Http404
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from mimetypes import guess_type

from time import localtime, strftime
from django.core import serializers

from socialnetwork.models import *
from socialnetwork.forms import *


@login_required
def home(request): 
    try:
        global_stream = Posts.objects.all().order_by('datetime').reverse()
        logged_in_user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(user=request.user)

        context = {'Posts':global_stream,'User':request.user,
                    'follows': user_profile.follows.all().values_list('user', flat=True),
                    'view':'home','Post_form':PostsForm()}
        print global_stream
    except: # catch *all* exceptions
        context = {'User':request.user}
    return render(request, 'home.html', context)

@login_required
def profile(request):
    try:
        username = request.path.split('/')[-1]#implement the get part
    #1print request.path
        if not username:
                username = request.user
        requested_user = User.objects.get(username=username)
    #ask TA for correctness
        user_stream = Posts.get_user_posts(Posts(),requested_user)#Posts.objects.filter( user= requested_user).order_by('datetime').reverse()
        comments=Comments.objects.all()
        context = {'Comments':comments,'Posts':user_stream,'User':request.user,'view':'profile'}
    #print context
    except: # catch *all* exceptions
        context = {'User':request.user}
    return  render(request, 'profile.html', context)

@login_required
def followers(request):
    try:
        requested_user = User.objects.get(username=request.user)
        followers_stream = Posts.get_follows_posts(Posts(),requested_user)
        comments=Comments.objects.all()
        context = {'Comments':comments,'Posts':followers_stream,'User':request.user,'view':'follower'}
    #print context
    except: # catch *all* exceptions
        context = {'User':request.user}
    return  render(request, 'profile.html', context)

@login_required
def follow_user(request,post_user):
    try:
        user_profile = UserProfile.objects.get(user = request.user)
        
        #print user_profile
        post_user_profile = UserProfile.objects.get(user = User.objects.get(username = post_user))
        if not post_user_profile in user_profile.follows.all():
           # print post_user_profile
            user_profile.follows.add(post_user_profile)
        print(post_user)
    except: # catch *all* exceptions
        context = {'User':request.user}
    return redirect(reverse('home'))

@login_required
def un_follow_user(request,post_user):
    try:
        user_profile = UserProfile.objects.get(user = request.user)
        #print user_profile
        post_user_profile = UserProfile.objects.get(user = User.objects.get(username = post_user))
        if post_user_profile in user_profile.follows.all():
            #print post_user_profile
            user_profile.follows.remove(post_user_profile)
        #print user_profile.follows.all()
    except: # catch *all* exceptions
        context = {'User':request.user}
    return redirect(reverse('home'))

@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    try:
        if request.method == 'GET':
            entry = {'User':User.objects.get(username=request.user)}
            user_info = UserProfile.get_user_info(UserProfile(),request.user)
            form = RegistrationForm(initial=user_info)#(exclude={'username'})
            form.fields.pop('username')
            form.fields.pop('password1')
            form.fields.pop('password2')
            form.fields.pop('email')
            context = { 'entry': entry, 'form': form,'view':'edit_profile','User':request.user }
        #print form.fields
            return render(request, 'edit_profile.html', context)

        form = RegistrationForm(request.POST,request.FILES)
        form.fields.pop('username')
        form.fields.pop('password1')
        form.fields.pop('password2')
        form.fields.pop('email')
        context['form'] = form

        if not form.is_valid():
            return render(request, 'edit_profile.html', context)

    # If we get here the form data was valid.  Register and login the user.
        user_data = User.objects.select_for_update().get(username=request.user)
        user_data.first_name = form.cleaned_data['firstname']
        user_data.last_name = form.cleaned_data['lastname']
        user_data.save()

        user_info = UserProfile.objects.select_for_update().get(user=request.user)
        user_info.age=form.cleaned_data['age']
        user_info.bio=form.cleaned_data['bio']
        user_info.pic=form.cleaned_data['pic']
        user_info.save()
    #print new_user_profile
    except: # catch *all* exceptions
        context = {'User':request.user}
    return redirect(reverse('home'))

@login_required
@transaction.atomic
def create_post(request):
    errors = []
    new_post = Posts()
    context={}
    try:
    
        if not 'post_message' in request.POST or not request.POST['post_message']:
            errors.append('You must enter an post to add.')
        form = PostsForm(request.POST)
        context['form'] = form

        if not form.is_valid():
            return HttpResponse("Character limit for a post exceded",content_type="text/html")
        else:
            print form.cleaned_data['post']
            new_post = Posts(post=form.cleaned_data['post'], user=request.user)
            new_post.save()

    except: 
        context = {'User':request.user}    
    return redirect(reverse('home'))


@login_required
def profile_picture(request,user):
    try:
        user_id = User.objects.get(username=user)
        user_profile = get_object_or_404(UserProfile,user=user_id)
        if not user_profile.pic:
            raise Http404
        content_type = guess_type(user_profile.pic.name)
    except: # catch *all* exceptions
        context = {'User':request.user} 
        return redirect(reverse('home'))
    return HttpResponse(user_profile.pic,content_type= content_type)

@login_required
def new_posts(request):
    context = {}
    try:
    #print request.path
        post_id = request.path.split('/')[-1]
        view = request.path.split('/')[-2]
        new_stream = Posts.get_posts_afterid(Posts(),post_id)
        comments = {}

        if (view == 'home'):
            user_profile = UserProfile.objects.get(user=request.user)
            context = {'Comments':comments,'Posts':new_stream,'User':request.user,'follows': user_profile.follows.all().values_list('user', flat=True),'view':'home'}
        elif (view == 'profile'):
            user_stream = Posts.get_posts_afterid(Posts(),post_id).filter(user=request.user)
            context = {'Comments':comments,'Posts':user_stream,'User':request.user,'view':'profile'}
        elif (view == 'follower'):
            followers_stream = new_stream.filter(user=UserProfile.objects.get(user = request.user).follows.all().values('user')).order_by('id').reverse()
            context = {'Comments':comments,'Posts':followers_stream,'User':request.user,'view':'follower'}
    except:
        context = {'User':request.user} 
        return redirect(reverse('home'))
    #print(context)
    return HttpResponse(render(request,'posts.html',context),content_type="text/html")

@login_required
def create_comment(request):
    errors = []
    new_post = Posts()
    try:
        if not 'comment' in request.POST or not request.POST['comment']:
            errors.append('You must enter an comment to add.')
        if not 'postId' in request.POST or not request.POST['postId']:
            errors.append('Post informaton not available')

        else:
            new_comment = Comments(comment=request.POST['comment'],user=request.user,post=Posts.objects.get(id=request.POST['postId']))#,datetime= dateTime)
           
            new_comment.save()
        print new_comment
        context = {'User':request.user,'comment':new_comment}
    except:
        context = {'User':request.user} 
        return redirect(reverse('home'))
    return HttpResponse(render(request,'comments.html',context),content_type="text/html")

@transaction.atomic
def confirm_registration(request, username, token):
    try:
        print username + "::" + token
        print User.objects.all()
        user = get_object_or_404(User, username=username)
    
    # Send 404 error if token is invalid
        if not default_token_generator.check_token(user, token):
            raise Http404

    # Otherwise token was valid, activate the user.
        user.is_active = True
        user.save()
        
    except:
        context = {'User':request.user}

    return redirect(reverse('home'))
    