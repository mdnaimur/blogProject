from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe
# Create your models here.

class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        #Post.objects.all() = super(PostManager,self).all()
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance,filename):
    #filebase,extention = filename.split(".")
    #return "%s/%s.%s"%(instance.id,instance.id,extention)
    return "%s/%s"%(instance.id,filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestap = models.DateTimeField(auto_now = False,auto_now_add = True)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post_detail",kwargs={"id":self.id})
        #return "/posts/%s/" %(self.id)
    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))
    
    class Meta:
        ordering = ["-timestap","-updated"]


def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s"%(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_reveiver(sender,instance,*args,**kwargs):
    # slug = slugify(instance.title)
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    #     slug = "%s-%s"%(slug,instance.id)
    # instance.slug =slug
    if not instance.slug:
        instance.slug= create_slug(instance)

pre_save.connect(pre_save_post_reveiver,sender=Post)