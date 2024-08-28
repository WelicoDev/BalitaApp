from django.shortcuts import render, redirect
from .models import Post, Category, Tag, Comment, Contact
from django.core.paginator import Paginator
from decouple import config
import requests
# Create your views here.

def home(request):
    data = request.GET
    page = data.get('page', 1)
    latest_posts = Post.objects.filter(is_published=True).order_by("-pk")[:4]
    categories = Category.objects.all()
    slide_posts = Post.objects.filter(is_published=True).order_by("-view_count")[:3]
    blog_posts = Post.objects.filter(is_published=True).order_by("-view_count")[3:6]
    more_posts = Post.objects.filter(is_published=True).order_by("-view_count")[6:9]
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    page_obj = Paginator(posts, 10)
    tags = Tag.objects.all()

    context = {
        "categories":categories,
        "posts": page_obj.get_page(page),
        "latest_posts":latest_posts,
        "slide_posts":slide_posts,
        "blog_posts":blog_posts,
        "more_posts":more_posts,
        "tags":tags
    }

    return render(request, 'index.html', context=context)

def category(request, slug):
    data = request.GET
    page = data.get('page', 1)
    slide_posts = Post.objects.filter(is_published=True).order_by("-view_count")[:3]
    latest_posts = Post.objects.filter(is_published=True).order_by("-pk")[:4]
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category, is_published=True).order_by("-created_at")
    page_obj = Paginator(posts, 10)
    tags = Tag.objects.all()

    context = {
        "categories": categories,
        "latest_posts": latest_posts,
        "posts":page_obj.get_page(page),
        "category":category,
        "slide_posts": slide_posts,
        "tags":tags
    }
    return render(request, 'category.html', context=context)


def views(request, slug):
    post = Post.objects.filter(is_published=True).get(slug=slug)
    if request.method == "POST":
        data = request.POST
        comment = Comment.objects.create(user=post.user, post=post, message=data['message'])
        comment.save()

        return redirect(f"/posts/{slug}/")

    latest_posts = Post.objects.filter(is_published=True).order_by("-pk")[:4]
    slide_posts = Post.objects.filter(is_published=True).order_by("-view_count")[:3]
    categories = Category.objects.all()
    blog_posts = Post.objects.filter(is_published=True).order_by("-view_count")[3:6]
    tags = Tag.objects.all()
    post.view_count += 1
    post.save(update_fields=["view_count"])
    comments = Comment.objects.filter(is_public=True, post=post)
    context = {
        "categories": categories,
        "latest_posts": latest_posts,
        "slide_posts": slide_posts,
        "post":post,
        "tags":tags,
        "comments":comments,
        "blog_posts":blog_posts
    }

    return render(request, 'blog-single.html', context=context)

def about(request):
    data = request.GET
    page = data.get('page', 1)
    latest_posts = Post.objects.filter(is_published=True).order_by("-pk")[:4]
    categories = Category.objects.all()
    slide_posts = Post.objects.filter(is_published=True).order_by("-view_count")[:3]
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    page_obj = Paginator(posts, 10)
    context = {
        "categories": categories,
        "latest_posts": latest_posts,
        "slide_posts": slide_posts,
        "tags": tags,
        "posts": page_obj.get_page(page),
    }

    return render(request, 'about.html', context=context)

def contact(request):
    if request.method == "POST":
        data = request.POST
        contact = Contact.objects.create(name=data['name'], email=data['email'], phone=data['phone'],
                                         message=data['message'])
        contact.save()
        message = (f"Project : BalitaApp.uz\nID : {contact.id}\nUser : {contact.name}\nEmail :  {contact.email}\nPhone : "
                   f"{contact.phone}\nMessage : {contact.message}\nTime : {contact.created_at.date()}  // "
                   f" {contact.created_at.hour}:{contact.created_at.minute}:{contact.created_at.second}")

        BOT_TOKEN = config("BOT_TOKEN")
        CHAT_ID = config("CHAT_ID")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        response = requests.get(url)

        print(response)
        return redirect("/contact")

    latest_posts = Post.objects.filter(is_published=True).order_by("-pk")[:4]
    slide_posts = Post.objects.filter(is_published=True).order_by("-view_count")[:3]
    tags = Tag.objects.all()
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "latest_posts": latest_posts,
        "slide_posts": slide_posts,
        "tags": tags
    }

    return render(request, 'contact.html', context=context)
