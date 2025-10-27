from django.shortcuts import render, get_object_or_404, redirect
from .models import Mod, ModVersion, Comment
from .forms import ModForm, ModVersionForm, CommentForm
from django.contrib.auth.decorators import login_required

def mod_home(request):
    all_mod = Mod.objects.all()
    return render(request, 'mod_home.html', {'all_mod': all_mod})

@login_required
def mod_detail(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)
    latest_version = mod.modversion_set.filter(private=False).order_by('-id').first()
    all_versions = mod.modversion_set.all().order_by('-id')
    comments = mod.comment_set.order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.mod = mod
            comment.author = request.user
            comment.save()
            return redirect('mod_detail', mod_id=mod.id)
    else:
        form = CommentForm()

    return render(request, 'mod_detail.html', {
        'mod': mod,
        'latest_version': latest_version,
        'all_versions': all_versions,
        'comments': comments,
        'form': form,
    })

@login_required
def create_mod(request):
    if request.method == 'POST':
        form = ModForm(request.POST)
        if form.is_valid():
            mod = form.save(commit=False)
            mod.creator = request.user
            mod.save()
            return redirect('mod_detail', mod_id=mod.id)
    else:
        form = ModForm()

    return render(request, 'create_mod.html', {'form': form})


@login_required
def upload_mod_version(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)

    if request.method == 'POST':
        form = ModVersionForm(request.POST, request.FILES)
        if form.is_valid():
            version = form.save(commit=False)
            version.mod = mod
            version.save()
            return redirect('mod_detail', mod_id=mod.id)
    else:
        form = ModVersionForm()

    return render(request, 'upload_version.html', {'form': form, 'mod': mod})

@login_required
def edit_mod(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)

    # Only the creator can edit
    if mod.creator != request.user:
        return redirect('mod_detail', mod_id=mod.id)

    if request.method == 'POST':
        form = ModForm(request.POST, instance=mod)
        if form.is_valid():
            form.save()
            return redirect('mod_detail', mod_id=mod.id)
    else:
        form = ModForm(instance=mod)

    return render(request, 'edit_mod.html', {'form': form, 'mod': mod})

@login_required
def edit_mod_version(request, version_id):
    version = get_object_or_404(ModVersion, id=version_id)
    mod = version.mod

    # Only the mod creator can edit versions
    if mod.creator != request.user:
        return redirect('mod_detail', mod_id=mod.id)

    if request.method == 'POST':
        form = ModVersionForm(request.POST, request.FILES, instance=version)
        if form.is_valid():
            form.save()
            return redirect('mod_detail', mod_id=mod.id)
    else:
        form = ModVersionForm(instance=version)

    return render(request, 'edit_version.html', {'form': form, 'mod': mod, 'version': version})