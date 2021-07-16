from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from markdown import markdown


def config_md_text(text):
    return str(text).replace("\n", "<br>")


def get_id():
    while(True):
        rand_id = random.randint(10000000, 99999999)
        used_hex_id = UsedID.objects.all().values_list('used_id', flat=True)

        if rand_id not in used_hex_id:
            UsedID.objects.create(used_id=rand_id)
            return rand_id


class UsedID(models.Model):
    used_id = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.used_id


class Worker(models.Model):
    user = models.OneToOneField('User', on_delete=models.DO_NOTHING, related_name="worker")
    tasks = models.ManyToManyField('Task', related_name='workers')
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class User(AbstractUser):
    google_id = models.CharField(max_length=255, blank=True)
    google_name = models.CharField(max_length=255, blank=True)
    google_email = models.EmailField(blank=True)
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Task(models.Model):
    picture = models.FileField(upload_to="pictures")
    name = models.CharField(max_length=16, )
    t_id = models.PositiveIntegerField(unique=True, blank=True)
    description_md = models.TextField(blank=True, default="")
    description_md_html = models.TextField(editable=False, default="")
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.t_id = get_id()
        if self.description_md:
            self.description_md_html = config_md_text(str(markdown(self.description_md)))
