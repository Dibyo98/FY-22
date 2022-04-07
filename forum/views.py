from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Question, Answer 
from .forms import NewAnswerForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):

    all_posts = Question.newmanager.all()

    return render(request, 'forum/index.html', {'posts': all_posts})


def post_single(request, post):

    post = get_object_or_404(Question, slug=post, status='published')

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
    }
    return render(request, 'forum/single.html', context )

 