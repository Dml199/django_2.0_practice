
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    def update_rating(self):
     
        post_rating = self.post_set.aggregate(total=Sum('rating'))['total'] or 0
        post_rating *= 3
        comment_rating = self.user.comment_set.aggregate(total=Sum('rating'))['total'] or 0
       
        comments_on_posts_rating = Comment.objects.filter(post__author=self).aggregate(total=Sum('rating'))['total'] or 0

        self.rating = post_rating + comment_rating + comments_on_posts_rating
        self.save()
        
    def getRating(self):
        print(self.rating)
        
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    
        
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    
    def getValues(self):
        print(f"Author: {self.author.user.username}.    \nPost type:{self.post_type}    \nPost:{self.text}   \nRating:{self.rating}")
        
        
    def preview(self):
        return self.text[:124]+"..."
        
    def like(self):
        self.rating=self.rating+1
        self.save()
        
    def dislike(self):
        self.rating=self.rating-1
        self.save()
        


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} - {self.category.name}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating=self.rating+1
        self.save()
        
    def dislike(self):
        self.rating=self.rating-1
        self.save()
        
        
        
    def __str__(self):
        return f'Комментарий от {self.user.username} к "{self.post.title}"'