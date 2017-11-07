from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from .validators import validate_file_extension
# Create your models here.
#MVC MODEL VIEW CONTROLLER 

def upload_location(instance,filename):
    return "%s/%s" %(instance.id, filename,)

  
class Archivos(models.Model):
    artista = models.CharField(max_length=120)
    album = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __unicode__(self):
        return self.album
    
    def __str__(self):
        return self.album
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})


class Post(models.Model):
    nombrealbum = models.ForeignKey(Archivos,related_name ='nomalb')
    usuar = models.ForeignKey('auth.User',related_name ='usrname',default=1)
    titulo = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    imagen = models.ImageField(upload_to=upload_location, 
                        null=True, blank=True,
                        width_field="width_field",
                        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    cancion = models.FileField(upload_to=upload_location, null=True, blank=True, validators=[validate_file_extension])
    Letra = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __unicode__(self):
        return self.titulo
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.titulo)
    if new_slug is not None:
        slug = new_slug
    qs =Post.objects.filter(slug=slug).order_by("-id")
    exists= qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
        
        
def pre_save_post_reciver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    
    
    
pre_save.connect(pre_save_post_reciver, sender=Post)
    
    