from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Comment
from django.template import loader  # obsolete, not needed after 'shorcut' used
from django.http import Http404  # obsolete, not needed after 'shorcut' used
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#from django_comments.forms import CommentForm
#from django_comments.models import Comment
from .forms import CommentForm


#class ModifiedCommentForm(CommentForm):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        del self.fields['url']  # modataan URL-kenttä pois Djangon valmiista kommentointifomista



#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    return HttpResponse('List of polls: ' + output)

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse('List of polls: ' + template.render(context, request))

# sama shortcutilla
##def index(request):
##    latest_question_list = Question.objects.order_by('-pub_date')[:5]
##    context = {'latest_question_list': latest_question_list}
##    return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

#def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)

#def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question': question})

# sama shortcutilla
##def detail(request, question_id):
##    question = get_object_or_404(Question, pk=question_id)
##    return render(request, 'polls/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

#def results(request, question_id):
#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % question_id)

##def results(request, question_id):
##    question = get_object_or_404(Question, pk=question_id)
##    return render(request, 'polls/results.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#def vote(request, question_id):
#    return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
def leave_comment(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    print("Kysymyksen id on:", question_id)
    print("Form data on:", request.POST)

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

#    if request.method == 'POST':
#        print("\nQuestion:", question)
#        form = CommentForm(request.POST, target_object=question)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('thankyou/')
#    else:
#        form = CommentForm(target_object=question)
#    return render(request, 'polls/comment_leave_comment.html', {
#        'form': form,
#        'question': question
#    })

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

