# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, TripSchedule, Follow, Trip
import bcrypt
# the index function is called when root is visited
def index(request):
    return render(request,"tb_app/registrationForm.html")

def doregister(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        u1 = User(name = request.POST['name'], username = request.POST['username'], 
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        u1.save()
        return redirect('/main')

def login(request):
    post_password = request.POST['password']
    post_username = request.POST["username"]
    print "*****************post_username " + post_username
    print "*****************post_pass " + post_password
    
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        try:
            u = User.objects.get(username = post_username)
            print "****************successful try"
            u.save()
            print u.id
            if bcrypt.checkpw(post_password.encode(), u.password.encode()):
                print "password match"
                request.session['id']=u.id
                print "*********** "
                print request.session['id']
                return redirect('/travels')
            return redirect('/main')
        except:
            return redirect('/main')

def travels(request):
    if 'id' in request.session:
        u = User.objects.get(id = request.session['id'])
        user_name = u.name
        print "user name is " + user_name

        # t = Trip.objects.exclude(admin_id=request.session['id'])
       
        # seen_trips = set()
        # new_list = []
        # for obj in t:
        #     if obj.admin.id not in seen_trips:
        #         new_list.append(obj)
        #         seen_trips.add(obj.admin.id)
  
    tj = Follow.objects.filter(follower_id=request.session['id'])
    ot = Trip.objects.exclude(admin_id=request.session['id'])
    
    seent = set()
    nl = []
# stuff
    if len(tj) >=1:
        for data in tj:
            for otherdata in ot:
                if otherdata.trip_id not in seent:
                    if data.trip_id != otherdata.trip_id:
                        nl.append(otherdata)
                        seent.add(otherdata.trip_id)
# stuff

        


        context = {
            'user' : user_name,
            'my_trips': Trip.objects.filter(admin_id=request.session['id']),
            'trip_joined': Follow.objects.filter(follower_id=request.session['id']),
            # 'other_trips': Trip.objects.exclude(admin_id=request.session['id'])
             'other_trips': nl
        }
        return render(request, "tb_app/dashboard.html", context) 

def getatrip(request):
    return render(request, "tb_app/travelsadd.html")

def processtrip(request): 
    # errors = TripSchedule.objects.basic_validator(request.POST)
    # if len(errors):
    #     for tag, error in errors.iteritems():
    #         messages.error(request, error, extra_tags=tag)
    #     return redirect('/travels/add')
    # else:
    trip1 = TripSchedule(destination = request.POST['destination'], description = request.POST['description'], TravelDateFrom = request.POST['TravelDateFrom'], TravelDateTo = request.POST['TravelDateTo'])
    trip1.save()
    user1 = User.objects.get(id=request.session['id'])
    # user1.trip.add(trip1.id)
    Trip.objects.create(admin = user1, trip = trip1)
    return redirect ('/travels')

def jointrip(request,tid,uid):
    trip1 = TripSchedule.objects.get(id=tid)
    trip1.save()
    u1 = User.objects.get(id = uid)
    u1.save()
    Follow.objects.create(trip = trip1, follower = u1)
    return redirect ('/travels')

def destination(request,tid):
    tripSchedule = TripSchedule.objects.get(id=tid)
    trip=Trip.objects.get(trip_id=tid)
    admin = trip.admin.name

    follow_list = Follow.objects.exclude(follower_id=trip.admin.id)

    unique_follows = []
    follow_list = Follow.objects.exclude(follower_id=trip.admin.id)
    for follow in follow_list:
        print "************** * * * *   " + str(follow.follower_id)
        if follow.follower_id not in unique_follows:
            unique_follows.append(follow.follower_id)

    print"*******now, the follow list"
    for i in unique_follows:
        print"******* * * * " + str(i)
    
    seen_follows = set()
    new_list = []
    for obj in follow_list:
        if obj.follower_id not in seen_follows:
            new_list.append(obj)
            seen_follows.add(obj.follower_id)



    # unique_reviews = []
    #     reviews = Review.objects.all()
    #     for review in reviews:
    #         if review.books not in unique_reviews:
    #             unique_reviews.append(review.books)

    # u1 = TripUser.objects.get(id=tid).user.name
    # u1id = TripUser.objects.get(id=tid).user.id
    # o1 = TripUser.objects.get(id=tid).user.id.exclude(TripUser.objects.get(id=tid).user.id)
    context={
        'tripSchedule':tripSchedule,
        'name':trip.admin.name,
        'other_users': Follow.objects.exclude(follower_id=trip.admin.id),
        # 'follows': Follow.objects.get(trip_id=tid)
        # 'follows': Follow.objects.all()
        'unique_follows':new_list
    }
    return render(request, "tb_app/destination.html", context)

def logout(request):
    request.session.clear()
    return redirect("/main")