from multiprocessing import context
from turtle import pos
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Question, Answer 
from .forms import NewAnswerForm,PostSearchForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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

