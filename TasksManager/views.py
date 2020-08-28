from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Choice, Question
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'TasksManager/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        return the last five published questions.
        """
        # return Question.objects.order_by('pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


def get_queryset():
    """
    Excludes any questions that aren't published yet
    """
    return Queston.objescts.filter(pub_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = Question
    template_name = 'TasksManager/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'TasksManager/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'TasksManager/detail.html',
                      {'question': question, 'error_message': "you didn't select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always return an HttpResponseRedirect after succesfully dealing
        # with POST data. this prevents data from being posted twice if a
        # user hits the back button twice
        return HttpResponseRedirect(reverse('TasksManager:results', args=(question.id,)))

    # return HttpResponse("you're voting on question %s." % question_id)

# # Create your views here.
# def index(request):
#     latest_question_list=Question.objects.order_by('pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     template = loader.get_template('TasksManager/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


# def detail(request, question_id):
#     # try:
#         # question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'TasksManager/detail.html', {'question' : question})
#     # return HttpResponse("you're looking at question %s." % question_id)


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'TasksManager/results.html', {'question':question})
#     # response = "you're looking at the response of question %s."
#     # return HttpResponse(response % question_id)
