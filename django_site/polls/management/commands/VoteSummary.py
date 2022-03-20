from django.core.management.base import BaseCommand
from polls.models import Question

class Command(BaseCommand):
    def handle(self, *args, **options):
        questions = Question.objects.all()
        for q in questions:
            print("[%d] %s" % (q.id, q.question_text))
            for c in q.choice_set.all():
                print(" - %s [%d vote]" % (c.choice_text, c.votes))
