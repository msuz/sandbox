from io import StringIO
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.management import call_command
from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_future_questions(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_two_past_question(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        question = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertContains(response, question.question_text)

class VoteSummaryCommandTests(TestCase):

    def test_no_questions(self):
        q1 = create_question(question_text="Question 1", days=0)
        q1.choices.create(choice_text="Choice 1-1", votes=1)
        q1.choices.create(choice_text="Choice 1-2", votes=3)
        q2 = create_question(question_text="Question 2", days=0)
        q2.choices.create(choice_text="Choice 2-1", votes=2)
        q2.choices.create(choice_text="Choice 2-2", votes=4)

        o = StringIO()
        call_command('vote_summary', stdout=o)
        v = o.getvalue()

        self.assertIn("[1] Question 1", v)
        self.assertIn(" - Choice 1-1 [1 votes]", v)
        self.assertIn(" - Choice 1-2 [3 votes]", v)
        self.assertIn("[2] Question 2", v)
        self.assertIn(" - Choice 2-1 [2 votes]", v)
        self.assertIn(" - Choice 2-2 [4 votes]", v)
