
from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Posts(models.Model):
    post = models.CharField(max_length=160)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(dict(post=self.post,datetime=str(self.datetime),user = str(self.user)))
    def __str__(self):
        return self.__unicode__()
    def __user__(self):
    	return self.user
    def get_user_posts(self,requestUser):
        return Posts.objects.filter(user=requestUser).order_by('id').reverse()
    def get_posts_afterid(self,lastId):
        return Posts.objects.filter(id__gt=lastId).order_by('id').reverse()
    def get_comments_posts(self):
        return Comments.objects.filter(post = self).order_by('datetime')
    def get_follows_posts(self,requestUser):
        return Posts.objects.filter(user=UserProfile.objects.get(user = requestUser).follows.all().values('user')).order_by('id').reverse()

class Comments(models.Model):
    comment = models.CharField(max_length=160)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    #postId = models.CharField(max_length=10,null=True)
    post = models.ForeignKey(Posts)

    def __unicode__(self):
        return str(dict(comment=self.comment,datetime=str(self.datetime),user = str(self.user),postId=str(self.post.id)))
    def __str__(self):
        return self.__unicode__()
    def __user__(self):
        return self.user

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    age = models.IntegerField(blank=True,null=True) # add birthday and calculate the age later
    bio = models.CharField(blank=True, max_length=430,null=True)
    pic = models.FileField(upload_to="profile_pics",null=True,default="profile_pics/empty.png",)
    content_type = models.CharField(max_length=50)
    follows = models.ManyToManyField('self',blank=True,symmetrical=False,related_name = 'followers')
    #content_type = models.CharField(max_length=50)

    def __unicode__(self):  
         return str(dict(age=self.age,bio=str(self.bio),user = str(self.user)))
    def __str__(self):
        return self.__unicode__()
    def __user__(self):
        return self.user
    def get_user_info(self,requestUser):
        user_info = User.objects.get(username=requestUser)
        user_profile = UserProfile.objects.get(user=requestUser)
        return (dict(age=user_profile.age,bio=(user_profile.bio),firstname = (user_info.first_name),lastname=  (user_info.last_name)))