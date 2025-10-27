from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, PostFiles
import json
import uuid

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('files')  # multiple file support

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(f"{post.title}-{uuid.uuid4().hex[:8]}")
            post.save()

            # Process each uploaded file
            for i, file in enumerate(files):
                desc_key = f'description_{i}'
                details_key = f'details_{i}'

                description = request.POST.get(desc_key, '')
                details_raw = request.POST.get(details_key, '')

                # try parsing JSON-style data
                try:
                    details = json.loads(details_raw)
                except json.JSONDecodeError:
                    details = {"text": details_raw}

                PostFiles.objects.create(
                    post=post,
                    file=file,
                    description=description,
                    details=details
                )

            return redirect('post_detail', slug=post.slug)
        else:
            print(post_form.errors)  # 👈 Helps debugging form validation
    else:
        post_form = PostForm()

    return render(request, 'create_post.html', {'form': post_form})
