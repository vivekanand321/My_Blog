from django.core.validators import MinLengthValidator
from statistics import mode
from django.db import models

# Create your models here.
class Tag(models.Model):
    caption=models.CharField(max_length=100)
    
    def __str__(self):
        return self.caption 


class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email_address=models.EmailField()

    def full_name(self):
        return f"{self.first_name }{self.last_name}"

    def __str__(self):
        return self.full_name()    


class Post(models.Model):
    title=models.CharField(max_length=100)
    excerpt=models.CharField(max_length=100)
    # image_name=models.CharField(max_length=100),using fileuplpad instead
    image=models.ImageField(upload_to="posts",null=True)
    date=models.DateField(auto_now=True)
    slug=models.SlugField(unique=True,db_index=True)#by default db_index is true but 
    #it is used for database to do quesris based on the slug in stored datas. 
    content=models.TextField(validators=[MinLengthValidator(10)])
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")
    #here on_delete is set to null
    #this is becoz if author for the post will delete than deleting the whole post it will set null to it.
    #also if have to cross access post by author than instead of posts_set we can use related_name which is posts.
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name=models.CharField(max_length=120)
    email=models.EmailField()
    text=models.TextField(max_length=200)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

