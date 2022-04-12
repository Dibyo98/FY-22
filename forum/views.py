from multiprocessing import context
from turtle import pos
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Question, Answer 
from .forms import NewAnswerForm,PostSearchForm,QuestionForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def home(request):

    all_posts = Question.newmanager.all()

    return render(request, 'forum/index.html', {'posts': all_posts})

@login_required
def post_single(request, post):

    post = get_object_or_404(Question, slug=post, status='published')
    fav=False
    if post.favourites.filter(id=request.user.id).exists():
        fav=True


    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 50)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewAnswerForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.name=request.user
            print(user_comment.name)
            user_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = NewAnswerForm()
    context= {
        'post': post, 
        'comments':  user_comment, 
        'comments': comments, 
        'comment_form': comment_form, 
        'allcomments': allcomments, 
        'fav':fav,
    }
    return render(request, 'forum/single.html', context )

 



def post_search(request):
    form = PostSearchForm()
    q = ''
    results = []
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']

            if q is not None:
                query = Q(title__contains=q)

            results = Question.objects.filter(query)
    
    context={
        'form': form,
        'q': q,
        'results': results
    }

    return render(request, 'forum/search.html',context)

@login_required
def post_create(request):
    form = QuestionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        print(instance.author)
        instance.save()
        form.save_m2m()
      
        messages.success(request, "Successfully Created")
        return redirect(instance.get_absolute_url())
    context = {
        "form": form,
        'page': 'new-post',
      
    }
    return render(request, "forum/post_form.html", context)




@login_required
def post_edit(request, post):

    page = 'post-edit'
    p = get_object_or_404(Question, slug=post, status='published')
    if p.author.id != request.user.id:
        raise PermissionDenied
    form = QuestionForm(instance=p)

    if request.method == 'POST':
        form = QuestionForm(request.POST,
                        request.FILES,
                        instance=p)
        if form.is_valid():
            form.save()
            
            messages.success(request, f'Post Updated')
            return redirect(p.get_absolute_url())

    else:
        form = QuestionForm(instance=p)

    context = {
        'form': form,
        'page': page,
        'post': p,
    }

    return render(request, 'forum/post_form.html', context)

@login_required
def deletePost(request, post):
    # p=Post.objects.get(slug=slug)

    p = get_object_or_404(Question, slug=post, status='published')
    if p.author.id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        p.delete()
        return redirect('forum:homepage')

    context = {'object': p}
    return render(request, 'forum/post_delete.html', context)

