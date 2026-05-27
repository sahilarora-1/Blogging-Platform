from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db.models import Q
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.http import Http404


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
        action = request.POST.get('action')

        if not title or not title.strip() or not content or not content.strip():
            messages.error(request, "Title and content are required.")
            return redirect('/create-post/')
        
        if image:
            allowed_extensions=['jpg', 'jpeg', 'png']
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                messages.error(request,"Only JPG, JPEG, and PNG images are allowed.")
                return redirect('/create-post/')

        base_slug = slugify(title)
        slug=base_slug
        counter=1

        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Post.objects.create(
            title=title,
            slug=slug,
            content=content,
            author=request.user,
            image=image,
            is_published=(action == 'publish')
            )
        if action == 'publish':
            messages.success(request, "Post published successfully.")
        else:
            messages.success(request, "Draft saved successfully.")
        return redirect('/dashboard/')
    
    return render(request,'create_post.html')


def post_detail(request, slug):
    post=get_object_or_404(Post,slug=slug)
    if not post.is_published:
        if not request.user.is_authenticated or request.user != post.author:
            raise Http404()
    return render(request, 'post_detail.html',{'post':post})

@login_required
def edit_post(request,id):
    post=get_object_or_404(Post,id=id, author=request.user)

    if request.method =='POST':
        new_title=request.POST.get('title')
        new_content=request.POST.get('content')
        new_image = request.FILES.get('image')
        action = request.POST.get('action')
        new_publish_state = (action == 'publish')


        
         # validation for blocks
        if (not new_title or not new_title.strip() or not new_content or not new_content.strip()):
            messages.error(request, "Title and content cannot be empty.")
            return redirect(f'/edit-post/{post.id}/')
        

        if (new_title == post.title and new_content == post.content and not new_image and new_publish_state == post.is_published):
            messages.info(request, "No changes were made.")
            return redirect('/dashboard/')
        
        post.title = new_title
        post.content = new_content

        
        if new_image:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            file_extension = new_image.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                messages.error(request,"Only JPG, JPEG, and PNG images are allowed.")
                return redirect(f'/edit-post/{post.id}/')
            post.image = new_image

        base_slug=slugify(new_title)
        slug=base_slug
        counter=1

        while Post.objects.filter(slug=slug).exclude(id=post.id).exists():
            slug=f"{base_slug}-{counter}"
            counter+=1

        old_publish_state = post.is_published
        post.slug=slug
        post.is_published = (action == 'publish')

        post.save()
        
        if old_publish_state and new_publish_state:
            messages.success(request, "Post updated successfully.")
        elif not old_publish_state and new_publish_state:
            messages.success(request, "Draft published successfully.")
        elif old_publish_state and not new_publish_state:
            messages.success(request, "Post moved to drafts.")
        else:
            messages.success(request, "Draft updated successfully.")
        
        return redirect('/dashboard/')
    
    return render(request, "edit_post.html", {"post":post})

@login_required
def delete_post(request,id):
    if request.method == 'POST':
        post=get_object_or_404(Post,id=id,author=request.user)
        post.delete()
        messages.success(request,"Post deleted successfully")

    return redirect('/dashboard/')

