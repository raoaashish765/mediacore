from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    vdata=upallvideo.objects.all()
    odd_lots = vdata[0::2]
    return render(request, 'channel/index.html', {'vid':odd_lots})


def create(request):
    currentuser=request.user.username
    if request.method=="POST":
        cname=request.POST['cnlname']
        newch=Channeldet.objects.create(user=currentuser, chname=cname)
        newch.save()
        return redirect('cstudio/'+currentuser)
    else:
        if Channeldet.objects.filter(user=currentuser):
            return redirect('cstudio/'+currentuser)
    return render(request, 'channel/create.html')


def studio(request):
    currentuser=request.user.username
    return redirect('cstudio/'+currentuser)

def cstudio(request, cid):
    cuser=request.user.username
    if request.method=="POST":
        vttle=request.POST['vidtitle']
        viddes=request.POST['viddes']
        vide=request.FILES['vidfile']
        chnl=Channeldet.objects.get(user=cuser)
        chaname=chnl.chname
        updata=upallvideo.objects.create(user=cuser, chname=chaname, titlle=vttle, details=viddes, video=vide)
        updata.save()
        return redirect('create')
    else:
        if Channeldet.objects.filter(user=cid):
            vdata=upallvideo.objects.filter(user=cuser)
            odd_lots = vdata[0::2]
            return render(request, 'channel/studio.html', {'vid':odd_lots})
        return redirect('create')

def video(request, vid):
    cuser=request.user.username
    if videoview.objects.filter(vid=vid).filter(user=cuser):
        pass
    else:
        addview=videoview.objects.create(vid=vid, user=cuser)
        addview.save()
    videodt=upallvideo.objects.filter(vid=vid)
    if len(videodt)==0:
        return HttpResponse("no video found!!!")
    else:
        videodt2=upallvideo.objects.get(vid=vid)
        likes=videolikes.objects.filter(vid=vid)
        videodt2.likes=len(likes)
        for x in likes:
            if x.user == cuser:
                videodt2.liked=True
            else:
                videodt2.liked=False
        views=videoview.objects.filter(vid=vid)
        videodt2.views=len(views)
        com=videocom.objects.filter(vid=vid)
        videodt2.comments=com
        return render(request, 'channel/videdit.html', {'data':videodt2})

def vidlk(request):
    cuser=request.user.username
    id=request.POST['like']
    if videolikes.objects.filter(vid=id).filter(user=cuser):
        dta=videolikes.objects.filter(vid=id).get(user=cuser)
        print(dta)
        dta.delete()
        return redirect('/channel/video/'+id)
    else:
        datasave=videolikes.objects.create(vid=id, user=cuser)
        datasave.save()
        return redirect('/channel/video/'+id)

def vidcmt(request):
    cuser=request.user.username
    id=request.POST['cmntid']
    comm=request.POST['cmnt']
    datasave=videocom.objects.create(vid=id, comment=comm, user=cuser)
    datasave.save()
    messages.error(request, "comment added to video : "+id)
    return redirect('/channel/video/'+id)


def videdt(request):
    cuser=request.user.username
    id=request.POST['vidid']
    tpk=request.POST['vtopic']
    dsk=request.POST['vtext']
    updata=upallvideo.objects.get(vid=id)
    if updata.user==cuser:
        updata.titlle=tpk
        updata.details=dsk
        updata.save()
        messages.error(request, "Video Updated Successfully!")
        return redirect('video/'+id)
    else:
        messages.error(request, "Something Went Wrong!!!")
        return redirect('home')

def viddelete(request):
    cuser=request.user.username
    id=request.POST['dltid']
    dltdata=upallvideo.objects.get(vid=id)
    if dltdata.user==cuser:
        dltdata.delete()
        messages.success(request, "video deleted!")
    return redirect('home')