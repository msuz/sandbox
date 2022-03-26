from django.core.management.base import BaseCommand
from polls.models import Question

class Command(BaseCommand):
    def handle(self, *args, **options):
        questions = Question.objects.all()
        for q in questions:
            self.stdout.write(f"[{q.id}] {q.question_text}")
            for c in q.choices.all():
                self.stdout.write(f" - {c.choice_text} [{c.votes} votes]")
