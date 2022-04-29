from django.db import models

# Create your models here.



class rooms(models.Model):

    room_name = models.CharField(max_length=100)
    room_id = models.CharField(max_length=8)
    room_psw = models.CharField(max_length=16)
    created_by = models.CharField(max_length=50)
    created_on = models.DateTimeField()


class chats(models.Model):

    room_id = models.CharField(max_length=8)
    msg = models.TextField()
    room_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50)
    created_on = models.DateTimeField()