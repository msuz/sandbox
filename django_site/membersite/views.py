from django.shortcuts import render
from django.views.generic.base import TemplateView
from polls.models import Question, Choice

# Create your views here.
class IndexView(TemplateView):
    template_name = "membersite/index.html"

    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.all()
        return render(self.request, self.template_name, context)

