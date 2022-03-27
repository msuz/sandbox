from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from polls.models import Question, Choice
import logging

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'membersite/index.html'
    def get(self, request, *args, **kwargs):
        logging.debug('Debug Message')
        logging.info('Info Message')
        logging.error('Error Message')
        context = super(IndexView, self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.all().prefetch_related('choices')
        return render(self.request, self.template_name, context)

class ResultsView(PermissionRequiredMixin, TemplateView):
    template_name = 'membersite/index.html'
    permission_required = ('polls.view_question', 'polls.view_choice')
    def get(self, request, *args, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.all().prefetch_related('choices')
        return render(self.request, self.template_name, context)
