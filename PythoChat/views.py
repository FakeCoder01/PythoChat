import django
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from chatapp.models import chats, rooms
import datetime, json

def index(request):
    return render(request, 'home.html')


def reg(request):
    if request.method == 'POST':

        user_name = request.POST.get('user_name')
        room_name = request.POST.get('room_name')
        room_psw = request.POST.get('room_psw')

        if rooms.objects.filter(room_name=room_name, room_psw=room_psw).exists():
            qs = rooms.objects.filter(room_name=room_name, room_psw=room_psw).first()
            context = {
                'room_id' : qs.room_id,
                'room_name' : room_name,
                'user_name' : user_name,
                'created_by' : qs.created_by,
                'created_on' : qs.created_on
            }
            request.session['user'] = {
                'room_id' : qs.room_id,
                'room_name' : room_name,
                'user_name' : user_name
            }
            return render(request, 'chat.html', {'context':context})
        else:
                
            created_on = datetime.datetime.now()
            room_id = get_random_string(8)
            create_room = rooms(room_name=room_name, room_id=room_id, room_psw=room_psw, created_by=user_name, created_on=created_on)
            create_room.save()
            context = {
                'room_id' : room_id,
                'room_name' : room_name,
                'user_name' : user_name,
                'created_by' : user_name,
                'created_on' : created_on
            }
            request.session['user'] = {
                'room_id' : room_id,
                'room_name' : room_name,
                'user_name' : user_name
            }
        return render(request, 'chat.html', {'context':context})      
    else:
        try: 
            
            if rooms.objects.filter(room_id = request.session['user'].get('room_id'), room_name = request.session['user'].get('room_name')).exists() and request.session['user'].get('room_id') != None:
                qs = rooms.objects.filter(room_name=request.session['user'].get('room_name'), room_id = request.session['user'].get('room_id')).first()
                context = {
                    'room_id' : request.session['user'].get('room_id'),
                    'room_name' : request.session['user'].get('room_id'),
                    'user_name' : request.session['user'].get('user_name'),
                    'created_by' : qs.created_by,
                    'created_on' : qs.created_on
                }
                return render(request, 'chat.html', {'context':context})
        except KeyError: 
            return redirect('/')    

def valid_req(request):

    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        user_name = request.GET.get('user_name')
        room_name = request.GET.get('room_name')

        if room_id and user_name and room_name :
            if rooms.objects.filter(room_id=room_id , room_name=room_name).exists():
                return True
            else:
                return False
        else:
                return False

    elif request.method == 'POST':
        room_id = request.POST.get('room_id')
        user_name = request.POST.get('user_name')
        room_name = request.POST.get('room_name')
        msg = request.POST.get('msg')

        if room_id and user_name and room_name  and msg:
            if rooms.objects.filter(room_id=room_id , room_name=room_name).exists():
                return True
            else:
                return False
        else:
                return False
    else:
        return False

def addChats(request):
    if valid_req(request):
        if request.method == 'POST':
            msg = request.POST.get('msg')
            room_id = request.POST.get('room_id')
            room_name = request.POST.get('room_name')
            user_name = request.POST.get('user_name')
            created_on = datetime.datetime.now()
            save_msg = chats(room_id=room_id, msg=msg, room_name=room_name, user_name=user_name, created_on=created_on)
            save_msg.save()
            return JsonResponse(json.dumps({'res':'messaged'}), safe=False)
        else:
            return redirect('/')
    else:
        return redirect('/')


def loadChats(request):
    if valid_req(request):
        if request.method == 'GET':
            room_id = request.GET.get('room_id')
            room_name = request.GET.get('room_name')
            allChats = chats.objects.filter(room_id = room_id, room_name=room_name)
            return JsonResponse({"chats" : list(allChats.values())})
        else:
            return redirect('/')
    else:
        return redirect('/')