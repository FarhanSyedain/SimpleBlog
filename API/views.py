from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view

from itertools import chain
from operator import attrgetter
import json
import random

from Configrations.models import *
from Configrations.serilizers import PostSerilizer,CommentSerilizer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class RecommendedPostsAPI(ListAPIView):
    serializer_class = PostSerilizer
    pagination_class = None
    
    def get_queryset(self):
        """
        If user is authenticated:Return queryset containing posts by the authors user follows. Incase the posts by the authors, users follows, aren't enough, then\n
        add the posts which belong to the category user loves —ie:has visited— the most.\n

        If the user is not authenticated, then return queryset containing the posts , belonging to the cateogry user has visited the most\n
        
        If posts arn't sufficent till now , for both — user is authticated and ain't authentiated—  cases, then add random posts.
        """
        
        post_count = 0
        minimum_posts = 6#The number of posts needed atleat. 
        posts_required = 8 #The number of posts needed.
        posts_added = 0
        to_be_returned = []
        categories_visited = None
       
       
        if self.request.user.is_authenticated: #For authenticated user: Check how many posts the author(s) he/she follows have posted.
            
            obj, created  = Following.objects.get_or_create(user=Profile.objects.get(user=self.request.user))
            all_authors_following = obj.users_following.all()

            for author in all_authors_following:
                post_count += BlogPost.objects.filter(author=Profile.objects.get(user=author),released=True).count()
                
                if post_count >= posts_required: #If Posts counted till now are equeal to or grater than posts needed , break.
                    break
     
        if post_count <= minimum_posts: #Pursue only if posts_count —Posts by author user folllows—  are >= to minimum posts needed
            
            #Now checking the cateogries user has visted and based on the data , reccomond posts
            
            if not self.request.user.is_authenticated: #If not authenticated, check coookies
                
                try:
                    categories_visited = self.request.COOKIES['categories_visited'] #Get model id , if any
                    
                    if UserHistories.objects.filter(id=int(categories_visited)).exists(): #Get model, if any
                        categories_visited = UserHistories.objects.get(id=int(categories_visited))
                        categories_visited = json.loads(categories_visited.history)
                    
                    else:
                        categories_visited = None
                    
                    
                except KeyError:
                    categories_visited = None
                
                add_posts = True #Add posts reccomonded from the categories
                add_random = False #If posts reccemmoned are'nt enough, add random posts
                             
            else: #Check history, if authenitcated
                
                user = Profile.objects.get(user=self.request.user)
                if not user.history is None:
                    try:
                        categories_visited = json.loads(user.history) 
                    except:
                        pass 
                
                for author in all_authors_following:
                    blogs = list(BlogPost.objects.filter(released=True,author=Profile.objects.get(user=author))[:posts_required-posts_added])
                    to_be_returned = set(chain(to_be_returned,blogs))
                    posts_added += len(blogs)
                    print(to_be_returned,'hello world')
                add_posts = True
                add_random = False
                
        else:#if post count >= than minimum posts
            
            for author in all_authors_following:
                blogs = list(BlogPost.objects.filter(released=True,author=Profile.objects.get(user=author))[:posts_required-posts_added])
                to_be_returned = set(chain(to_be_returned,blogs))
                posts_added += len(blogs)
                
                if posts_added >= posts_required:
                    break
                
            add_posts = False    
                        
            if len(to_be_returned) < posts_required and len(to_be_returned) > minimum_posts:
                add_posts = True
                add_random = False #Add reccomended posts only, don't add random posts.
        
        if add_posts:
            
            try:
                try:
                    if user.user.is_authenticated and categories_visited is None:#May be we've not set cateogries_visited 
                        if not user.history is None:
                            try:
                                categories_visited = json.loads(user.history) 
                            except:
                                raise KeyError
                        else:
                            categories_visited = None
                except UnboundLocalError:
                    pass
                
                if categories_visited is None:
                    raise KeyError #Add random posts in "except" secceion
                
                categories_visited = sorted(categories_visited,key=lambda instance: categories_visited[instance],reverse=True)
                categories_selected = []
                
                for category in categories_visited: #Add category to selected, from which we will add posts and stop when we've enogh posts
                    post_count += Category.objects.filter(category=category).count()
                    categories_selected.append(category)
                    
                    if post_count >= posts_required:
                        break
                
                
                if post_count >= minimum_posts:
                    
                    for category in categories_visited:
                        blogs = list(BlogPost.objects.filter(category__category=category,released=True)[:posts_required-posts_added])
                        to_be_returned = set(chain(to_be_returned,blogs))
                        posts_added += len(blogs)
                        
                        if posts_added >= posts_required:
                            break
                else:
                    
                    for category in categories_visited:
                        blogs = list(BlogPost.objects.filter(category__category=category,released=True)[:posts_required-posts_added])
                        to_be_returned = set(chain(to_be_returned,blogs))
                        posts_added += len(blogs)
                    
                    raise KeyError    
                    
            except KeyError:
                
                if not add_random and  len(to_be_returned) > minimum_posts:
                    to_be_returned = to_be_returned[:minimum_posts]
                   
                else:
                    
                    all_blogs = list(BlogPost.objects.filter(released=True))
                    while True:
                       
                        if len(all_blogs) == 0:
                            break
                        
                        choise = random.choice(all_blogs)
                        
                        if not choise in to_be_returned:
                            to_be_returned.append(choise)
                            all_blogs.remove(choise)
                            posts_added += 1  
                        
                        else:
                            all_blogs.remove(choise)
                          
                        if add_random and posts_added >= posts_required or not add_random and posts_added >= minimum_posts:
                            break
        return list(to_be_returned)
    

class YouMayLikeAPI(ListAPIView):
    serializer_class = PostSerilizer
    pagination_class = None
    
    def get_queryset(self):
        
        limit = 6
        
        for i in range(1,4):    
            try:
                all_blogs = list(sorted(BlogPost.objects.filter(released=True),key=attrgetter('relivence'),reverse=True))[:limit]
            except IndexError:
                limit -= 1
        
        return all_blogs


class AllBlogsAPI(ListAPIView):
    serializer_class = PostSerilizer
    queryset = BlogPost.objects.filter(released=True).order_by('-created')
    pagination_class = PageNumberPagination
    

class FilteredBlogsAPI(ListAPIView):
    serializer_class = PostSerilizer
    queryset = BlogPost.objects.filter(released=True).order_by('-created')
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter,SearchFilter]
    ordering_fields = ['created']
    search_fields = ['key_words']
    

    def get_queryset(self):
        
        get = dict(self.request.GET)
        
        category = get.get('category',False)
        tag = get.get('tag',False)

        search_filter = {}
        
        if category:
            search_filter.update({'category__category':category[0]})
            
        if tag:
            search_filter.update({'tags__tag':tag[0]})
            
        return BlogPost.objects.filter(released=True,**search_filter)


class CommentAPI(ListAPIView):
    serializer_class = CommentSerilizer
    pagination_class = PageNumberPagination
    
    
    def get_queryset(self):
        
        get = dict(self.request.GET)
        post_id = get.get('post')
        post = BlogPost.objects.get(id=post_id[0])
        comments = Comment.objects.filter(post=post)
    
        return comments
    
@csrf_exempt
def post_comment(request):
    
    data = json.loads(request.body)
    body = data['body']
    post_id = data['post']
    
    post = BlogPost.objects.get(id=post_id)
    
    user = Profile.objects.get(user=request.user)
    
    try:
        
        comment = Comment()
        comment.comment_body = body 
        comment.user = user 
        comment.post = post
        comment.save()
        
        return JsonResponse({'success':True,'Comment_body':body,'dated':comment.posted,'author':comment.user.username},safe=False)
    
    except:
    
        return JsonResponse({'success':False},safe=False) 
    
    
class MyPostsAPI(ListAPIView):
    serializer_class = PostSerilizer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter,SearchFilter]
    ordering_fields = ['created','views']
    search_fields = ['key_words']
    
    
    def get_queryset(self):
        
        get_queries = dict(self.request.GET)
        
        search_filters = {}
        
        released = get_queries.get('released',None)
        
        if released is not None:
            search_filters.update({'released':bool(int(released[0]))})
        
        qs = BlogPost.objects.filter(**search_filters)
        
        return qs
 
    
@api_view(['POST'])
def follow_author(request):
    try:
        if request.user.is_authenticated:
            
            data = request.data 
            post_id = data['blog_post_id']
            
            blog = BlogPost.objects.get(id=post_id)
            
            author = blog.author 
            
            user = Profile.objects.get(user=request.user)
            
            follow_obj, created = Following.objects.get_or_create(user=user) 
            
            if not follow_obj.users_following.all().filter(username=author.username).exists():
                
                follow_obj.users_following.add(author.user)
                staff_obj = Staff.objects.get(user=author)
                staff_obj.followers = staff_obj.followers + 1
                
                staff_obj.save()
                follow_obj.save()
            
                return Response({'success':True})
            raise
    except:
        return Response({'success':False})
    
        
@api_view(['POST'])
def unfollow_user(request):
    try:
        if request.user.is_authenticated:
            
            data = request.data 
            post_id = data['blog_post_id']
            
            blog = BlogPost.objects.get(id=post_id)
            
            author = blog.author 
            
            user = Profile.objects.get(user=request.user)
            
            follow_obj, created = Following.objects.get_or_create(user=user) 
            
            if follow_obj.users_following.all().filter(username=author.username).exists():
                
                follow_obj.users_following.remove(author.user)
                staff_obj = Staff.objects.get(user=author)
                staff_obj.followers = staff_obj.followers - 1
                
                staff_obj.save()
                follow_obj.save()
            
                return Response({'success':True})
            raise
    except:
        return Response({'success':False})



@api_view(['POST'])
def like_post(request):
 
    if request.user.is_authenticated:
        
        try:
            data = request.data 
            
            post_id = data['post_id']
            post = BlogPost.objects.get(id=post_id)   
            post.stars.add(request.user)
            post.save()
            return Response({'success':True})       
        except:
            return Response({'success':False})
        

@api_view(['POST'])
def unlike_post(request):
    
    if request.user.is_authenticated:
        
        try:
            data = request.data 
            
            post_id = data['post_id']
            post = BlogPost.objects.get(id=post_id)
            post.stars.remove(request.user)
            post.save()
            return Response({'success':True}) 
        except: 
            return Response({'success':False})
