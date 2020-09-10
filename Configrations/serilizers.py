from .models import *
from rest_framework.serializers import ModelSerializer,SerializerMethodField


class PostSerilizer(ModelSerializer):
    thumbnail = SerializerMethodField('get_thumbnail')
    author = SerializerMethodField('get_author')
    category = SerializerMethodField('get_category')
    class Meta:
        model = BlogPost
        fields = ['thumbnail','slug','category','created','body','title','sub_title','author'] 
        
    
    def get_thumbnail(self,post):
        return post.thumbnail.url
    
    def get_category(self,post):
        return post.category.category if not post.category is None else "No category"
        
    
    def get_author(self,post):
        return post.author.username
    

class CommentSerilizer(ModelSerializer):
    user = SerializerMethodField('get_name')
    class Meta:
        model = Comment
        fields = '__all__'
        
    def get_name(self,instance):
        return instance.user.username