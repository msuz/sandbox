from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from polls.models import Question, Choice
import logging

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "membersite/index.html"

    def get(self, request, *args, **kwargs):
        logging.debug("Debug Message")
        logging.info("Info Message")
        logging.error('Error Message')
        context = super(IndexView, self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.all().prefetch_related('choices')
        return render(self.request, self.template_name, context)
