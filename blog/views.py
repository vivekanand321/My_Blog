from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView,DetailView
from django.views import View
from .forms import CommentForm 
class Starting_Page(ListView):
        template_name="blog/index.html"
        model=Post
        ordering= ["-date"]
        context_object_name="posts"
        
        def get_queryset(self):
             queryset=super().get_queryset()
             data=queryset[:3]
             return data

#  def sort_def(po):
#     print("po is",po)
#     return po["date"]

# def starting_page(request):
#     latest_post=Post.objects.all().order_by("-date")[:3]
#     # sorted_post=sorted(all_posts,key=sort_def)
    
#     # latest_post=sorted_post[-3:]
#     return render(request,"blog/index.html",{
#         "posts":latest_post
#     })

class AllPostsView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    ordering=['-date']
    context_object_name="posts"
# def posts(request):
#     all_posts=Post.objects.all().order_by("-date")
#     return render(request,"blog/all-posts.html",{
#         "posts":all_posts
#     })

class SinglePostView(View):
    def get(self,request,slug):
        try:
            post=Post.objects.get(slug=slug)
            context={
                "post":post,
                "post_tags":post.tags.all(),
                "comment_form":CommentForm(),
                "comments":post.comments.all().order_by("-id")
            }
            return render(request,"blog/post-detail.html",context)
        except:
            return render(request,"blog/404.html")



    def post(self,request,slug):
        comment_form=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)#data is not stored till now ,it is in commnet variable
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id")

        }    
        return render(request,"blog/post-detail.html",context)

    # template_name="blog/post-detail.html"
    # model=Post
    
    # # as tag was not appeard for that
    # def get_context_data(self, **kwargs):
    #      context=super().get_context_data(**kwargs)
    #      context["post_tags"]=self.object.tags.all()
    #      context["comment_form"]=CommentForm()
    #      return context

# def post_detail(request,slug):
#     identified_post=get_object_or_404(Post,slug=slug)
#     # identified_post=Post.objects.get(slug=slug)
#     return render(request,"blog/post-detail.html",{
#         "post":identified_post,
#         "post_tags":identified_post.tags.all()
    
#     })


class ReadLaterView(View):
    def get(self,request):
        stored_posts=request.session.get("stored_posts")
        print("stored post is",stored_posts)
        context={}

        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context["has_posts"]=False
        else:
            posts=Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_posts"]=True

        return render(request,"blog/stored-posts.html",context)        

    def post(self,request):
        stored_posts=request.session.get("stored_posts")
        print("in post stored post is",stored_posts)
        if stored_posts is None:
            stored_posts=[]

        post_id=int(request.POST["post_id"])
        print("in post fetching ",post_id)

        if post_id not in stored_posts:
            print("appending in stored_posts")
            stored_posts.append(post_id)
            print("after appending",stored_posts)
            request.session["stored_posts"]=stored_posts
            print("printing finale",request.session["stored_posts"])
            

        return HttpResponseRedirect('/')
        


