from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete,pre_delete
from django.core.files.storage import default_storage
from django.db.models import FileField

import os

from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    username = models.CharField(max_length=50,blank=True,null=True,unique=True)
    is_staff = models.BooleanField(default=False)
    history = models.TextField(blank=True,null=True) #How many times did This Guy Vist a cateogry 
    
    def __str__(self):
        if not self.name is None:
            if len(self.name) > 0:
                return self.name
        return self.username
    
    def save(self,**kwargs):
        super().save(**kwargs)


class Staff(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    about_me = RichTextUploadingField(blank=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile_pic = models.ImageField(upload_to='users',blank=True,max_length=200)
    followers = models.IntegerField(default=0)
    
        
class Tag(models.Model):
    tag = models.CharField(max_length=30)
    
    def __str__(self):
        return self.tag

    def save(self,**kwargs):
        
        self.tag = self.tag.lower()
        
        super().save(**kwargs)

class Category(models.Model):
    category = models.CharField(max_length=30)
    
    def __str__(self):
        return self.category
    
    
    def save(self,**kwargs):
        
        self.category = self.category.lower()
        
        super().save(**kwargs)
    

class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='Blog_Thumbnails')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    body = RichTextUploadingField() #
    released = models.BooleanField(default=True)
    key_words = models.TextField()
    stars = models.ManyToManyField(User,blank=True)
    slug = models.SlugField(blank=True,null=True)
    tags = models.ManyToManyField(Tag,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    featured = models.BooleanField(default=False)
    
    @property
    def relivence(self):
        day_uploaded = self.created
        today = timezone.now()
        old = today - day_uploaded
        minutes_old = old.seconds / 60
        views = self.views if self.views > 0 else .0001
        return (views + self.stars.all().count()) / minutes_old

    def __str__(self):
        return self.title

    def save(self,**kwargs):
        
        if self.slug is None:
            self.slug = self.title
        
        self.slug = slugify(self.slug)
        
        slug_exists = False
        if BlogPost.objects.filter(slug=self.slug).exists():
            blog = BlogPost.objects.get(slug=self.slug)
            slug_exists = True
            if blog == self:
                slug_exists = False
                
        count = 0
        while slug_exists:
            
            self.slug = self.slug[:-len(str(count))] #Remove the number added at the end
            self.slug = slugify(str(self.slug + str(count)))
            count += 1
            slug_exists = BlogPost.objects.filter(slug=self.slug).exists()        
        
        self.key_words = (self.title + " " + self.sub_title + " " + self.author.username + ' ' + self.key_words )
        
        
        super().save(**kwargs)

    def delete(self, **kwargs):
        
        #write some logic to delte the respetive thumbnail images
        
        return super().delete(**kwargs)        
        

class Comment(models.Model):
    comment_body = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    

class Following(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    users_following = models.ManyToManyField(User,blank=True)
    
    
class UserHistories(models.Model):
    history = models.TextField(blank=True,null=True)
    
    
models_to_be_registerd_in_admin_pannel = [Following,Comment,BlogPost,Profile,Tag,Category,UserHistories,Staff]


def configure_profile(instance,created,**kwargs):
    if created:
        username = instance.username
        user = Profile()
        user.username = username
        user.user = instance
        user.save()
        

def update_user(instance,created,*args,**kwargs):
    if not created:
        if instance.is_staff:
            if not Staff.objects.filter(user=instance).exists():
                staff = Staff()
                staff.user = instance
                staff.save()
            
        instance.user.username = instance.username 
        
        instance.user.save()
    
post_save.connect(update_user,Profile)
post_save.connect(configure_profile,User)



@receiver(pre_delete, sender=Staff)
def mymodel_delete(sender, instance, **kwargs):

    instance.profile_pic.delete(False)

@receiver(pre_delete, sender=BlogPost)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
