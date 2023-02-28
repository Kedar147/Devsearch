from email.policy import default
from operator import truediv
from pickle import TRUE
from tkinter import CASCADE
from uuid import uuid4
from django.db import models
from users.models import Profile
# Create your models here.
class Projects(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    featured_image=models.ImageField(null=True,blank=True,default='default.jpg')
    demo_link=models.CharField(max_length=200,null=True,blank=True)  
    source_link=models.CharField(max_length=200,null=True,blank=True)
    Tags=models.ManyToManyField('Tags',blank=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):
    Vote_type=(
        ('up','up vote'),
        ('down','down vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    projects=models.ForeignKey(Projects,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(choices=Vote_type,max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self) -> str:
        return self.value

class Tags(models.Model):
    
    
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self) -> str:
        return self.name