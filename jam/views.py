from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def index(request):
    return render(request, 'index.html')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')

    user = User.objects.get(email=request.POST['email'])
    request.session['user'] = user.first_name 
    request.session['id'] = user.id
    return redirect('/home')


def create(request):
    return render(request, 'create.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
            return redirect('/create')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user'] = new_user.first_name
        request.session['id'] = new_user.id 
        return redirect('/blog')


def blog(request):
    if 'user' in request.session:
        context = {
            'wall_messages': Wall_Message.objects.all(),
            'logged_user': User.objects.get(id=request.session['id'])
        }
        return render(request, 'home_logged.html', context)
    else:
        context = {
            'wall_messages': Wall_Message.objects.all()
        }
        return render(request, 'blog.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.login_validator(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user'] = user.first_name
    request.session['id'] = user.id
    return redirect('/blog')

    

def profile(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        context = {
            'logged_user': User.objects.get(id=request.session['id'])
        }
        return render(request, 'profile_logged.html', context)

def create_blog_post(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        Wall_Message.objects.create(message = request.POST['message'], poster = User.objects.get(id=request.session['id']))
        return redirect('/blog')

def like(request, id):
    if 'user' not in request.session:
        return redirect('/')
    else:
        liked_message = Wall_Message.objects.get(id=id)
        user_liking = User.objects.get(id=request.session['id'])
        liked_message.user_likes.add(user_liking)
        return redirect('/blog')

def comment(request, id):
    if 'user' not in request.session:
        return redirect('/')
    else: 
        poster = User.objects.get(id=request.session['id'])
        message = Wall_Message.objects.get(id=id)
        Comment.objects.create(comment= request.POST['comment'], poster=poster, Wall_Message=message)
        return redirect('/blog')

def delete_comment(request, id):
    varx = Comment.objects.get(id=id)
    if request.session['id'] == varx.poster.id:
        Comment.objects.filter(id=id).delete()
        return redirect('/blog')
    else:
        return redirect ('/blog')

def delete_post(request, id):
    varz = Wall_Message.objects.get(id=id)
    if request.session['id'] == varz.poster.id:
        Wall_Message.objects.filter(id=id).delete()
        return redirect('/blog')
    else:
        return redirect('/blog')

def edit_post(request, id):
    vary = Wall_Message.objects.get(id=id)
    if request.session['id'] != vary.poster.id:
        return redirect('/blog')
    else:
        context = {
            'wall_message': Wall_Message.objects.get(id=id)
        }
        return render(request, 'edit_post.html', context)

def edit_post_success(request, id):
    updated_message = Wall_Message.objects.get(id=id)
    updated_message.message = request.POST['message']
    updated_message.save()
    return redirect('/blog')

def edit_profile(request, id):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'edit_profile.html', context)

def delete_profile(request, id):
    deleted_user = User.objects.get(id=id)
    deleted_user.delete()
    request.session.clear()
    return redirect ('/home')

def update_user(request, id):
    if request.method == "GET":
        return redirect('/')
    else:
        updated_user = User.objects.get(id=id)
        updated_user.first_name = request.POST['first_name']
        updated_user.last_name = request.POST['last_name']
        updated_user.instruments_played = request.POST['instruments_played']
        updated_user.bio = request.POST['bio']
        updated_user.save()
        return redirect('/profile')

def musicians(request):
    if 'user' in request.session:
        context = {
            'musicians': Musician.objects.all()
        }
        return render(request, 'musicians_logged.html', context)
    else:
        context = {
            'musicians': Musician.objects.all()
        }
        return render(request, 'musicians.html', context)

def create_musician(request):
    if request.method == "GET":
        return redirect('/')
    else:
        poster = User.objects.get(id=request.session['id'])
        Musician.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], gear=request.POST['gear'], preferred_genres=request.POST['preferred_genres'], instruments_played=request.POST['instruments_played'], contact_info=request.POST['contact_info'], poster=poster)
        return redirect('/musicians')

def delete_musician(request, id):
    varb = Musician.objects.get(id=id)
    if request.session['id'] == varb.poster.id:
        Musician.objects.filter(id=id).delete()
        return redirect('/musicians')
    else:
        return redirect('/musicians')

def gig_wall(request):
    if 'user' in request.session:
        context = {
            'gigs':Gig.objects.all()
        }
        return render(request, 'gig_wall.html', context)
    else:
        context = {
            'gigs':Gig.objects.all()
        }
        return render(request, 'gig_wall.html', context)

def create_gig(request):
    if request.method == "GET":
        return redirect('/')
    else:
        Gig.objects.create(
            poster=User.objects.get(id=request.session['id']), details=request.POST['details'], contact_info=request.POST['contact_info'],
        )
        return redirect('/gig_wall')

def delete_gig(request, id):
    vara = Gig.objects.get(id=id)
    if request.session['id'] == vara.poster.id:
         Gig.objects.filter(id=id).delete()
         return redirect('/gig_wall')
    else:
        return redirect('/gig_wall')
    
def view_profile(request, id):
        context = {
            'logged_user': User.objects.get(id=id)
        }
        return render(request, 'profile.html', context)
    
    
  
