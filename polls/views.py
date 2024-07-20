from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Comment
from django.template import loader  # obsolete, not needed after 'shorcut' used
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#from django_comments.forms import CommentForm
#from django_comments.models import Comment
from .forms import CommentForm
import requests
from django.db.models import Q
from django.db.models import Count 
from django.db import connection


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #"""Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')[:5]

        most_popular_poll = Question.objects.annotate(num_votes=Count('choice')).order_by('-num_votes')[:2]
        return most_popular_poll


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):

    # changed the service to "anybody can vote"
    # if not request.user.is_authenticated:           # this fixes the tampering of detail.html user authentication (mimt-attack against incomplete user authentication)
    #    return HttpResponseForbidden("You must be logged in to vote !")

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
def leave_comment(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    #print("Kysymyksen id on:", question_id)
    #print("Form data on:", request.POST)
    comments = Comment.objects.filter(question=question).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            return HttpResponseRedirect(reverse('polls:comment_thanks', args=(question.id,)))
    else:
        form = CommentForm()

    return render(request, 'polls/comment_leave_comment.html', {'question': question, 'comments': comments, 'form': form})


def comment_thanks(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        comments = Comment.objects.filter(question=question).order_by('-created_at')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'polls/comment_thank_you.html', {
        'question': question,
        'comments': comments
    })

def go_to_homepage(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    try:
        response = requests.get(comment.url)
        content = response.text
        print('kommentin url', comment.url)
        #print('content', content)
    except requests.RequestException as e:
        return HttpResponse(f"An error occurred: {e}")

    return render(request, 'polls/comment_show_homepage.html', {'name': comment.name, 'url': comment.url, 'content': content})

def search(request):
    query = request.GET.get('q')
    if query:
        questions = Question.objects.filter(
            Q(question_text__icontains=query) |      # Hae kysymyksiä ja
            Q(choice__choice_text__icontains=query)  # vaihtoehtoja
        ).distinct()                                 # Poistaatuplat

    else:
        questions = Question.objects.all()

    return render(request, 'polls/polls_search.html', {'questions': questions, 'query': query})








""" MUISTISSA ITSELLE; ALLA OLEVA EI LÄHDE TOIMIMAAN haluamallani tavalla (liittyy SQL-injectioniin)

def search(request):
    query = request.GET.get('q', '')
    print('query', query)
    if query:
        sql_query = 
            SELECT * 
            FROM polls_question 
            WHERE question_text LIKE ?
        
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [f'%{query}%'])
            questions = cursor.fetchall()
        print('questions', questions)
    else:
        questions = Question.objects.all()
        print('questions', questions)

    return render(request, 'polls/polls_search.html', {'questions': questions, 'query': query})


"""

