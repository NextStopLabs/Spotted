from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from posts.models import Post, PostFiles, Comment, Friendship
from mods.models import Mod
from main.models import FeatureToggle
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def following_api(request):
    user = request.user
    if user.is_authenticated:
        people_qs = User.objects.filter(followers__follower=user)
        people = list(people_qs.values('id', 'username'))
        return JsonResponse({'people_following': people})
    return JsonResponse({'error': 'Authentication required'}, status=401)

def following_feed_api(request):
    if request.user.is_authenticated:
        following = User.objects.filter(followers__follower=request.user)
        followed_posts = Post.objects.filter(author__in=following).order_by('-created_at')

        for item in followed_posts:
            setattr(item, 'recent_comments', Comment.objects.filter(post=item).order_by('-created_at')[:6])

        posts_data = []
        for post in followed_posts:
            # build tags per-post
            raw_tags = post.tags.split(' ') if post.tags else []
            tags = []
            for t in raw_tags:
                t = t.strip()
                if not t:
                    continue
                t = t.lower().replace(',', '')
                t = t.lower().replace(' ', '_')
                if not t.startswith('#'):
                    t = f"#{t}"
                tags.append(t)
            serialize_comments = []
            for comment in post.recent_comments:
                serialize_comments.append({
                    'author': comment.author.username,
                'comment': comment.comment,
                'created_at': comment.created_at.isoformat(),
            })
            # serialize files as objects with url for the client-side code
            files_qs = PostFiles.objects.filter(post=post)[:6]
            file_list = [{'url': pf.file.url} for pf in files_qs]

            posts_data.append({
                'slug': post.slug,
                'title': post.title,
                'author': post.author.username,
                'description': post.description,
                'recent_comments': serialize_comments,
                'full_file_count': PostFiles.objects.filter(post=post).count(),
                'files': file_list,
                'tags': tags,
                'created_at': post.created_at.isoformat(),
                'updated_at': post.updated_at.isoformat(),
                'likes': post.total_likes(),
                'dislikes': post.total_dislikes(),
            })

        return JsonResponse({'posts': posts_data})
    else:
        return JsonResponse({'error': 'Authentication required'}, status=401)

def home(request):
    feature_toggles = FeatureToggle.objects.filter(name="home_page").first()
    if feature_toggles and (feature_toggles.is_coming_soon or feature_toggles.is_enabled):
        return render(request, 'coming_soon.html')

    random_posts = Post.objects.order_by('?')[:6]

    following_usernames = []
    if request.user.is_authenticated:
        following_usernames = list(
            request.user.following.values_list('following__username', flat=True)
        )

    if request.user.is_authenticated:
        following = User.objects.filter(followers__follower=request.user)
    else:
        following = []

    followed_posts = Post.objects.filter(author__in=following).order_by('-created_at')[:6]

    # Attach a `recent_comments` attribute to each Post instance (don't overwrite the
    # model's reverse related manager `comments` which raises on assignment).
    for item in followed_posts:
        setattr(item, 'recent_comments', Comment.objects.filter(post=item).order_by('-created_at')[:6])

    context = {
        'random_posts': random_posts,
        'following_usernames': following_usernames,
        'following': following,
        'followed_posts': followed_posts,
    }
    return render(request, 'home.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    mods = Mod.objects.filter(creator=user)

    is_following = False
    if request.user.is_authenticated:
        is_following = Friendship.objects.filter(follower=request.user, following=user).exists()

    context = {
        'mods': mods,
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'user_profile.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_files = PostFiles.objects.filter(post=post)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    context = {
        'post': post,
        'post_files': post_files,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users away from signup

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        post.dislikes.remove(user)

    return JsonResponse({'likes': post.total_likes(), 'dislikes': post.total_dislikes()})


@login_required
def toggle_dislike(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.dislikes.add(user)
        post.likes.remove(user)

    return JsonResponse({'likes': post.total_likes(), 'dislikes': post.total_dislikes()})


@login_required
def toggle_follow(request, username):
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, username=username)
    user = request.user

    friendship, created = Friendship.objects.get_or_create(follower=user, following=target_user)
    if not created:
        friendship.delete()
        following = False
    else:
        following = True

    return JsonResponse({'following': following})

@login_required
@csrf_exempt
def add_comment(request, slug):
    if request.method == 'POST':
        post = Post.objects.get(slug=slug)
        data = json.loads(request.body)
        comment_text = data.get('comment', '').strip()
        if comment_text:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                comment=comment_text
            )
            return JsonResponse({
                'success': True,
                'author': request.user.username,
                'comment': comment.comment
            })
    return JsonResponse({'success': False})
