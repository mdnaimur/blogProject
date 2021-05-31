from django.db.models import query
from django.http.response import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from urllib import quote_plus
from django.db.models import Q
from urllib.parse import quote 
from django.utils import timezone
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm
from .models import Post
from comments.models import Comment
# Create your views here.
def post_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"yeah done... successfully...")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"oh noo ... failed...")
    context = {
        'form':form
    }
    return render(request,'post_form.html',context)

def post_detail(request,id):
    instance = get_object_or_404(Post,id=id)
    if instance.draft or instance.publish>timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote(instance.content)
    content_type = ContentType.objects.get_for_model(Post)
    obj_id = instance.id
    comments = Comment.objects.filter(content_type=content_type,object_id = obj_id)
    #comments = Comment.objects.filter(user=request.user)
    context = {
        "title":instance.title,
        "instance":instance,
        "share_string":share_string,
        "comments":comments
    }
    return render(request,'post_detail.html',context)

def post_list(request):
    today = timezone.now()
    queryset_list = Post.objects.active()#filter(draft=False).filter(publish__lte=timezone.now())#all()#.order_by("-timestap")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__icontains=query)
        
        ).distinct()
    paginator = Paginator(queryset_list, 2) # Show 25 contacts per page.

    page = request.GET.get('page')
    try:
        queryset= paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list":queryset,
        "title":"List",
        "today":today
    }
    return render(request,'post_list.html',context)



def post_update(request,id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"yeah done... successfully updated...")
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        "title":instance.title,
        "instance":instance,
        "form":form,
    }
    return render(request,'post_form.html',context)
    
def post_delete(request,id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,"yeah done... successfully...")
    return redirect("posts:list")
