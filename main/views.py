from django.shortcuts import render, redirect
from .models import Category, Tags, Post, About, Contact, Comment
from django.core.paginator import Paginator
from .tasks import send_contact_message

# Create your views here.
def home(request):
    data = request.GET
    page = data.get('page', 1)
    categories = Category.objects.all().order_by("-created_at")
    tags = Tags.objects.all().order_by("-created_at")
    all_posts = Post.objects.filter(is_published=True).order_by("-created_at")
    popular_posts = all_posts.order_by("-view_count")[:3]
    latest_posts = all_posts[:3]
    person = About.objects.get(id=1)
    posts = all_posts
    page_obj = Paginator(all_posts, 8)
    banners = posts[:3]
    blogs = posts[3:6]
    context = {
        "home":"active",
        "categories":categories,
        "tags":tags,
        "posts":page_obj.get_page(page),
        "banners":banners,
        "blogs":blogs,
        "popular_posts": popular_posts,
        "person":person,
        "latest_posts": latest_posts
    }
    return render(request, 'index.html', context=context)

def about(request):
    data = request.GET
    page = data.get('page', 1)
    categories = Category.objects.all().order_by("-created_at")
    tags = Tags.objects.all().order_by("-created_at")
    person = About.objects.get(id=1)
    all_posts = Post.objects.filter(is_published=True).order_by("-created_at")
    page_obj = Paginator(all_posts, 8)
    latest_posts = all_posts[:3]
    popular_posts = all_posts.order_by("-view_count")[:3]
    posts = all_posts
    context = {
        "about":"active",
        "categories": categories,
        "person":person,
        "tags":tags,
        "popular_posts": popular_posts,
        "latest_posts": latest_posts,
        "posts":page_obj.get_page(page),
    }
    return render(request, 'about.html', context=context)

def category(request, slug):
    data = request.GET
    page = data.get('page', 1)
    categories = Category.objects.all().order_by("-created_at")
    tags = Tags.objects.all().order_by("-created_at")
    all_posts = Post.objects.filter(is_published=True).order_by("-created_at")
    page_obj = Paginator(all_posts, 8)
    popular_posts = all_posts.order_by("-view_count")[:3]
    latest_posts = all_posts[:3]
    ctg_name = categories.get(slug=slug).name
    posts = all_posts.filter(category__name=ctg_name)
    person = About.objects.get(id=1)
    context = {
        "category":"active",
        "categories": categories,
        "popular_posts":popular_posts,
        "posts":page_obj.get_page(page),
        "ctg_name":ctg_name,
        "person":person,
        "tags":tags,
        "latest_posts": latest_posts
    }
    return render(request, 'category.html', context=context)


def contact(request):
    if request.method == "POST":
        data = request.POST
        contact = Contact.objects.create(name=data['name'], phone=data['phone'], email=data['email'],
                                         message=data['message'])
        contact.save()

        send_contact_message.delay(contact.id)

        return redirect("/contact")

    categories = Category.objects.all().order_by("-created_at")
    tags = Tags.objects.all().order_by("-created_at")
    all_posts = Post.objects.filter(is_published=True).order_by("-created_at")
    popular_posts = all_posts.order_by("-view_count")[:3]
    latest_posts = all_posts[:3]
    person = About.objects.get(id=1)

    context = {
        "contact": "active",
        "categories": categories,
        "tags": tags,
        "person": person,
        "popular_posts": popular_posts,
        "latest_posts": latest_posts
    }

    return render(request, 'contact.html', context=context)


def detail(request, slug):
    categories = Category.objects.all().order_by("-created_at")
    tags = Tags.objects.all().order_by("-created_at")
    post = Post.objects.get(slug=slug)
    post.view_count += 1
    post.save(update_fields=["view_count"])


    all_posts = Post.objects.filter(is_published=True).order_by("-created_at")
    popular_posts = all_posts.order_by("-view_count")[:3]
    latest_posts = all_posts[:3]
    related_posts = all_posts.filter(category__slug=post.category.slug).order_by("-created_at")[:3]
    person = About.objects.get(id=1)

    if request.method == "POST":
        data = request.POST
        comment = Comment.objects.create(user=post.user, post=post, message=data['message'])
        comment.save()

        return redirect(f"/post/{slug}/")

    comments = Comment.objects.filter(post=post)
    context = {
        "post":post,
        "categories": categories,
        "tags":tags,
        "popular_posts": popular_posts,
        "person":person,
        "latest_posts":latest_posts,
        "comments":comments,
        "related_posts":related_posts
    }
    return render(request, 'blog-single.html', context=context)

def search(request):
    data = request.GET
    page = data.get('page', 1)
    categories = Category.objects.all().order_by("-created_at")
    tags = Tags.objects.all().order_by("-created_at")
    all_posts = Post.objects.filter(is_published=True).order_by("-created_at")
    popular_posts = all_posts.order_by("-view_count")[:3]
    person = About.objects.get(id=1)
    latest_posts = all_posts[:3]
    if request.method == "POST":
        data = request.POST
        query = data.get("query")

        return redirect(f"/search?q={query}")


    query = request.GET.get('q')
    if query is not None and len(query) > 1:
        posts = Post.objects.filter(is_published=True, title__icontains=query)
        page_obj = Paginator(posts, 8)
    else:
        posts = Post.objects.filter(is_published=True)
        page_obj = Paginator(posts, 8)

    context = {
        "posts": page_obj.get_page(page),
        "categories": categories,
        "tags":tags,
        "popular_posts":popular_posts,
        "person": person,
        "latest_posts": latest_posts,
    }

    return render(request, 'category.html', context)
