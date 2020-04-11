import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice

def create_question(question_text, days, with_choice = True):
    '''
    Create a question with (1)the given `question_text` and 
    (2)published the given number of `days` offset to now 
    (negative for questions published in the past, 
    positive for questions that have yet to be published).
    (3)two choices
    '''
    time = timezone.now() + datetime.timedelta(days = days)
    question = Question.objects.create(question_text = question_text, 
        pub_date = time)
    if with_choice != False:
        create_choice(question = question, choice_text = "choice 1")
        create_choice(question = question, choice_text = "choice 2")
    return question

def create_choice(question, choice_text, votes = 0):
    '''
    Create a Choice with the given 'question', 'choice_text' and the
    number of 'vote' to now. 
    '''
    return Choice.objects.create(
        question = question, choice_text = choice_text, votes = votes)
    
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() returns True for questions whose pub_date
    is within the last day.
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
        If no questions exist, an appropriate message is displayed.
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 
            "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])
    
    def test_past_question(self):
        '''
        Questions with a pub_date in the past are 
        displayed on teh index page
        '''
        create_question(
            question_text="Past question", 
            days = -30
            )
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )
    
    def test_future_question(self):
        '''
        Questions with a pub_date in the future aren't displayed
        on the index page.
        '''
        create_question(question_text='Future question', days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        '''
        Even if both future and past question exist, only past
        questions are displayed.
        '''
        create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )
    
    def test_two_past_question(self):
        '''
        The questions index page may dispaly multiple questions.
        '''
        create_question(question_text="past question 1", days = -30)
        create_question(question_text="past question 2", days = -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question 2>', 
            '<Question: past question 1>']
        )
    
    def test_past_question_with_no_choice(self):
        '''
        The questions index page does not diaplay questions without choice
        '''
        create_question(question_text="past question no choice", 
            days = 30, with_choice = False)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        '''
        future_question = create_question(
            question_text="future question",
            days = 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="past question",
        days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_past_question_with_no_choice(self):
        '''
        The detail view of a question without choice returns 404 not found
        '''
        past_question_no_choice = create_question(
            question_text="past question no choice",
            days = 30,
            with_choice = False)
        url = reverse('polls:detail', args=(past_question_no_choice.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        '''
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        '''
        future_question = create_question(
            question_text="future question",
            days = 30)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="past question",
        days=-30)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_past_question_with_no_choice(self):
        '''
        The result view of a question without choice returns 404 not found
        '''
        past_question_no_choice = create_question(
            question_text="past question no choice",
            days = 30,
            with_choice = False)
        url = reverse('polls:results', args=(past_question_no_choice.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
