from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db.models import Q
from django.utils.text import slugify
from django.core.paginator import Paginator


# Create your views here.

def home(request):
    query=request.GET.get('q')

    posts=Post.objects.filter(is_published=True).order_by('-created_at')

    if query:
        posts=posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
        


    paginator=Paginator(posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, "home.html", {"page_obj": page_obj,'query':query})


@login_required
def create_post(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        image = request.FILES.get('image')
        base_slug = slugify(title)
        slug=base_slug
        counter=1

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect('/create-post/')

        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Post.objects.create(
            title=title,
            slug=slug,
            content=content,
            author=request.user,
            image=image,
            )
        messages.success(request, "Post published successfully.")
        return redirect('/dashboard/')
    
    return render(request,'create_post.html')


def post_detail(request, slug):
    post=get_object_or_404(Post,slug=slug)
    return render(request, 'post_detail.html',{'post':post})

@login_required
def edit_post(request,id):
    post=get_object_or_404(Post,id=id, author=request.user)

    if request.method =='POST':
        new_title=request.POST.get('title')
        new_content=request.POST.get('content')
        new_image = request.FILES.get('image')

        post.title=new_title
        post.content = new_content
        
        if not new_title or not new_content:
            messages.error(request, "Title and content cannot be empty.")
            return redirect(f'/edit-post/{post.id}/')
        

        if (new_title == post.title and new_content == post.content and not new_image):
            messages.info(request, "No changes were made.")
            return redirect('/dashboard/')
        
        if new_image:
            post.image = new_image

        base_slug=slugify(new_title)
        slug=base_slug
        counter=1

        while Post.objects.filter(slug=slug).exclude(id=post.id).exists():
            slug=f"{base_slug}-{counter}"
            counter+=1

        post.slug=slug

        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('/dashboard/')
    
    return render(request, "edit_post.html", {"post":post})

@login_required
def delete_post(request,id):
    post=get_object_or_404(Post,id=id,author=request.user)
    post.delete()
    messages.success(request,"Post deleted successfully")

    return redirect('/dashboard/')

