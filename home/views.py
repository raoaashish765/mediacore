from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from mediacore import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, uri_to_iri
from .tokens import generate_token
from .models import *
import datetime
import os
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required()
def index(request):
    fname= request.user.first_name
    name=request.user.username
    set=setting.objects.get(user=name)
    inter=set.interest
    stint=str(inter)
    intli = list(stint.split("@"))
    fulldata=[]
    for i in intli:
        indata=Allposts.objects.filter(public=True).filter(topic=i)
        for j in indata:
            nowdata=j.post_id
            nowlike=Postlikes.objects.filter(post=nowdata)
            lenth=len(nowlike)
            j.likes=lenth
            lkdata=Postlikes.objects.filter(post=nowdata).filter(user=name)
            if len(lkdata)==0:
                j.liked=False
            else:
                j.liked=True
            comdta=Postcomments.objects.filter(post=nowdata)
            j.comments=comdta
        fulldata.append(indata)
    if len(fulldata) <=1:
        messages.error(request, "No Post To Show Please Update Your interests!!!")
    return render(request, 'home/index.html', {'fname': fname, 'ext':fulldata})

def signup(request):
    if request.method =="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request, "username already exists!!!")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "email already exists!!!")
            return redirect('signup')

        if len(username)>10:
            messages.error(request, "username must be less than 10 characters!!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "password didn't match!!!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "username must be alphanumeric!!!")
            return redirect('signup')

        myuser= User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False

        myuser.save()
        messages.success(request, "Account Created Successfully!!!, Please Confirm Your email To Activate Your Account")

        #follow model creation for this user
        Follow.objects.create(user=username, followers='@', following='@')
        setting.objects.create(user=username, interest='')

        #code to send email
        subject= "Media-Core Account Activation 'Required'!!"
        message= "Hello ! Dear "+ myuser.first_name+". \n Your Email Is Used To Create An Account On Our Site (https://mediacore.com) \n Media-Core Welcome You To Our Community \n your username : " +myuser.username
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #email Confirmation send mail
        current_site=get_current_site(request)
        subject2= "Media-core Email Confirmation (Required)"
        message2= render_to_string('e_c.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email= EmailMessage(
            subject2,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently =True
        email.send()
        return redirect('usersettings')
    return render(request, 'home/signup.html')

def signin(request):
    if request.method =="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']

        user= authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname= user.first_name
            if setting.objects.filter(user=username):
                return render(request, "home/index.html", {'fname': fname})
            else:
                return render(request, "home/usersettings.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credintials!")
            return redirect('signin')
    return render(request, 'home/signin.html')

@login_required()
def signout(request):
    logout(request)
    messages.success(request, "logged out!!")
    return render(request, 'home/signin.html')

@login_required()
def activate(request, uidb64, token):
    try:
        uid = uri_to_iri(urlsafe_base64_decode(uidb64))
        myuser =User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active =True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Email Verified Successfully!!")
        return redirect('home')
    else:
        return redirect(request, 'failed.html')

@login_required()
def usersettings(request):
    if request.method == "POST":
        inter= request.POST['interest']
        pri = request.POST.get('pri', False)
        pass1=request.POST['pass1']
        name=request.user.username
        useraut= authenticate(username=name, password=pass1)
        if useraut is not None:
            data=setting.objects.get(user=name)
            data.public=pri
            data.interest=inter
            data.save()
            messages.success(request, "Your Account Info Is Saved Successfully!!!")
            return redirect('home')
    return render(request, 'home/usersettings.html')

def user(request, name):
    if User.objects.filter(username=name):
        log=request.user.username
        profile=Follow.objects.get(user=name)
        followers=profile.followers
        following=profile.following
        counter1 = followers.count('@')
        counter2 = following.count('@')
        logged='@'+log+'@'
        if logged in following:
            f_val='unfollow'
        else:
            f_val='follow'
        btnshow=True
        if name==log:
            btnshow=False
            allpost=Allposts.objects.filter(user=log)
            for i in allpost:
                id=i.post_id
                cntlike=Postlikes.objects.filter(post=id)
                cnt=len(cntlike)
                i.likes=cnt
                lkdata=Postlikes.objects.filter(post=id).filter(user=name)
                if len(lkdata)==0:
                    i.liked=False
                else:
                    i.liked=True
                comdta=Postcomments.objects.filter(post=id)
                i.comments=comdta
            return render(request, 'home/user.html',{
            'name':name,
            'ing':int((counter1)/2),
            'ers':int((counter2)/2),
            'posts':allpost,
            'show':btnshow
            })
        else:
            myposts=Allposts.objects.filter(user=name)
            for i in myposts:
                id=i.post_id
                cntlike=Postlikes.objects.filter(post=id)
                cnt=len(cntlike)
                i.likes=cnt
                lkdata=Postlikes.objects.filter(post=id).filter(user=name)
                if len(lkdata)==0:
                    i.liked=False
                else:
                    i.liked=True
                comdta=Postcomments.objects.filter(post=id)
                i.comments=comdta
            prof=setting.objects.get(user=name)
            pub=prof.public
            if pub:
                return render(request, 'home/user.html',{
                    'name':name,
                    'ing':int((counter1)/2),
                    'ers':int((counter2)/2),
                    'btn':f_val,
                    'posts':myposts,
            'show':btnshow
                })
            else:
                return render(request, 'home/user.html',{
                'name':name,
                'ing':int((counter1)/2),
                'ers':int((counter2)/2),
                'btn':f_val,
            'show':btnshow
            })
    else:
        return render(request, '404error.html')

@login_required()
def followview(request):
    if request.method=="POST":
        now=request.POST['now']
        name=request.POST['user']
        log=request.user.username
        if Unfpenalty.objects.filter(user=log):
            data=Unfpenalty.objects.filter(user=log)
            lenthdata=len(data)
            print(lenthdata)
            if lenthdata>=50:
                loggeduser=User.objects.get(username=log)
                loggeduser.is_active=False
                loggeduser.save()
                logout(request)
                messages.success(request, "Your Account Has Been Blocked Please Contact Support!!")
                return render(request, 'home/signin.html')
            else:
                unfus=[]
                undt=[]
                for i in data:
                    tempfus=i.unfollow
                    tempdt=i.time
                    unfus.append(tempfus)
                    undt.append(tempdt)
                if name in unfus:
                    nowt=datetime.date.today()
                    m=len(undt)
                    totim=undt[m-1]
                    penti=totim.date()
                    if penti>nowt:
                        messages.error(request, "Your Can Follow This User After 2 Days")
                        return redirect('user/'+name)
                    else:
                        if(now=='follow'):
                            profile=Follow.objects.get(user=name)
                            following=profile.following
                            removed1=following.replace("['", '')
                            removed2=removed1.replace("']", '')
                            logged='@'+log+'@'
                            res=removed2+logged
                            upuser=Follow.objects.get(user=name)
                            upuser.following=res
                            upuser.save()
                            #for current user
                            profile2=Follow.objects.get(user=log)
                            followers=profile2.followers
                            removed3=followers.replace("['", '')
                            removed4=removed3.replace("']", '')
                            logged2='@'+name+'@'
                            res2=removed4+logged2
                            upuser2=Follow.objects.get(user=log)
                            upuser2.followers=res2
                            upuser2.save()
                            return redirect('user/'+name)
                        if(now=='unfollow'):
                            profile=Follow.objects.get(user=name)
                            following=profile.following
                            removed1=following.replace("['", '')
                            removed2=removed1.replace("']", '')
                            logged='@'+log+'@'
                            res=removed2.replace(logged, '')
                            upuser=Follow.objects.get(user=name)
                            upuser.following=res
                            upuser.save()
                            #for current user
                            profile2=Follow.objects.get(user=log)
                            followers=profile2.followers
                            removed3=followers.replace("['", '')
                            removed4=removed3.replace("']", '')
                            logged2='@'+name+'@'
                            res2=removed4.replace(logged2, '')
                            upuser2=Follow.objects.get(user=log)
                            upuser2.followers=res2
                            upuser2.save()
                            #adding unfollow penalty
                            tday=datetime.date.today()
                            tdelt=datetime.timedelta(days=2)
                            ntime=tday+tdelt
                            Unfpenalty.objects.create(user=log, unfollow=name, time=ntime)
                            return redirect('user/'+name)
                else:
                    if(now=='follow'):
                        profile=Follow.objects.get(user=name)
                        following=profile.following
                        removed1=following.replace("['", '')
                        removed2=removed1.replace("']", '')
                        logged='@'+log+'@'
                        res=removed2+logged
                        upuser=Follow.objects.get(user=name)
                        upuser.following=res
                        upuser.save()
                        #for current user
                        profile2=Follow.objects.get(user=log)
                        followers=profile2.followers
                        removed3=followers.replace("['", '')
                        removed4=removed3.replace("']", '')
                        logged2='@'+name+'@'
                        res2=removed4+logged2
                        upuser2=Follow.objects.get(user=log)
                        upuser2.followers=res2
                        upuser2.save()
                        return redirect('user/'+name)
                    if(now=='unfollow'):
                        profile=Follow.objects.get(user=name)
                        following=profile.following
                        removed1=following.replace("['", '')
                        removed2=removed1.replace("']", '')
                        logged='@'+log+'@'
                        res=removed2.replace(logged, '')
                        upuser=Follow.objects.get(user=name)
                        upuser.following=res
                        upuser.save()
                        #for current user
                        profile2=Follow.objects.get(user=log)
                        followers=profile2.followers
                        removed3=followers.replace("['", '')
                        removed4=removed3.replace("']", '')
                        logged2='@'+name+'@'
                        res2=removed4.replace(logged2, '')
                        upuser2=Follow.objects.get(user=log)
                        upuser2.followers=res2
                        upuser2.save()
                        #adding unfollow penalty
                        tday=datetime.date.today()
                        tdelt=datetime.timedelta(days=2)
                        ntime=tday+tdelt
                        Unfpenalty.objects.create(user=log, unfollow=name, time=ntime)
                        return redirect('user/'+name)
        else:
            if(now=='follow'):
                profile=Follow.objects.get(user=name)
                following=profile.following
                removed1=following.replace("['", '')
                removed2=removed1.replace("']", '')
                logged='@'+log+'@'
                res=removed2+logged
                upuser=Follow.objects.get(user=name)
                upuser.following=res
                upuser.save()
                #for current user
                profile2=Follow.objects.get(user=log)
                followers=profile2.followers
                removed3=followers.replace("['", '')
                removed4=removed3.replace("']", '')
                logged2='@'+name+'@'
                res2=removed4+logged2
                upuser2=Follow.objects.get(user=log)
                upuser2.followers=res2
                upuser2.save()
                return redirect('user/'+name)
            if(now=='unfollow'):
                profile=Follow.objects.get(user=name)
                following=profile.following
                removed1=following.replace("['", '')
                removed2=removed1.replace("']", '')
                logged='@'+log+'@'
                res=removed2.replace(logged, '')
                upuser=Follow.objects.get(user=name)
                upuser.following=res
                upuser.save()
                #for current user
                profile2=Follow.objects.get(user=log)
                followers=profile2.followers
                removed3=followers.replace("['", '')
                removed4=removed3.replace("']", '')
                logged2='@'+name+'@'
                res2=removed4.replace(logged2, '')
                upuser2=Follow.objects.get(user=log)
                upuser2.followers=res2
                upuser2.save()
                #adding unfollow penalty
                tday=datetime.date.today()
                tdelt=datetime.timedelta(days=2)
                ntime=tday+tdelt
                Unfpenalty.objects.create(user=log, unfollow=name, time=ntime)
                return redirect('user/'+name)
    else:
        return redirect('home')

def fing(request, name):
    data=Follow.objects.get(user=name)
    following=data.following
    dat=str(following)
    strValue = dat.replace("@@", '#')
    strValue2 = strValue.replace("@", '')
    li = list(strValue2.split("#"))
    del li[0]
    return render(request, 'home/following.html', {'list':li})

def fers(request, name):
    data=Follow.objects.get(user=name)
    followers=data.followers
    dat=str(followers)
    strValue = dat.replace("@@", '#')
    strValue2 = strValue.replace("@", '')
    li = list(strValue2.split("#"))
    del li[0]
    return render(request, 'home/followers.html', {'list':li})

@login_required()
def posts(request):
    if request.method =="POST":
        post=Allposts()
        post.text=request.POST['text']
        post.topic=request.POST['topic']
        post.user=request.user.username
        if len(request.FILES) != 0:
            post.image=request.FILES['image']
        set=setting.objects.get(user=request.user.username)
        pri=set.public
        if pri:
            post.public=True
        else:
            post.public=False
        post.save()
        return redirect('user/'+request.user.username)

def postview(request, pid):
    if request.method=="POST":
        data=Allposts.objects.get(post_id=pid)
        if len(request.FILES) != 0:
            try:
                os.remove(data.image.path)
            except:
                print("An exception occurred")
            data.image=request.FILES['image']
        data.text=request.POST['text']
        data.topic=request.POST['topic']
        data.save()
        messages.success(request, "Successfully updated")
        return redirect('/')  
    else:
        if Allposts.objects.filter(post_id=pid):
            data=Allposts.objects.get(post_id=pid)
            com=Postcomments.objects.filter(post=pid)
            data.comments=com
            lks=Postlikes.objects.filter(post=pid)
            data.likes=len(lks)
            for i in lks:
                if i.user==request.user.username:
                    data.liked=True
                else:
                    data.liked=False
            if data.user==request.user.username:
                return render(request, 'home/postedit.html', {'data':data, 'edit':True})
            else:
                return render(request, 'home/postedit.html', {'data':data})
        else:
            messages.error(request, "NO Such Post!!!")
            return redirect('home')


def postdelete(request):
    poid=request.POST['poid']
    allpost=Allposts.objects.filter(post_id=poid)
    allpost.delete()
    messages.success(request, "post deleted!")
    return redirect('home')

@csrf_exempt
def likepst(request, lk):
    user1=request.user.username
    lkdata=Postlikes.objects.filter(post=lk).filter(user=user1)
    if len(lkdata)==0:
        postid=lk
        lkdta=Postlikes(post=postid, user=user1)
        lkdta.save()
        messages.success(request, "liked http://localhost:8000/postview/"+postid)
        return JsonResponse({'status':'liked!!'})
    else:
        lkdata.delete()
        messages.success(request, "unliked http://localhost:8000/postview/"+postid)
        return JsonResponse({'status':'unliked!!'})

@login_required()
def userr(request):
    name=request.user.username
    return redirect('user/'+name)


def cmntpst(request):
    user1=request.user.username
    cmnt=request.POST['cmnttext']
    postid=request.POST['cmtid']
    lkdta=Postcomments(post=postid, user=user1, comment=cmnt)
    lkdta.save()
    messages.success(request, "commented on http://localhost:8000/postview/"+postid)
    return redirect('postview/'+postid)


def report(request):
    if request.method=="POST":
        repo=Repo()
        repo.user=request.user.username
        repo.rtitle=request.POST['rt']
        repo.rexplain=request.POST['re']
        if len(request.FILES) != 0:
            repo.rimage=request.FILES['rm']
        repo.save()
        return HttpResponse("Report Added Successfully")
    else:
        return render(request, 'home/report.html')

def srch(request):
    txt=request.POST['srchtext']
    dta=User.objects.filter(username__contains=txt)
    return render(request, 'home/srch.html', {'sers':dta})