# coding=utf-8
import datetime
import os
import random

from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Questionnaire, ChoiceQuestion, NonChoiceQuestion
from .models import AnswerSheet, SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer
from .models import Choice
from Activity.models import ActivityType, Activity
# Create your tests here.


class QuestionModelsTest(TestCase):

    def setUp(self):
        # create a default user who post the questionnaire
        self.user = get_user_model().objects.create(username="some_user")
        # create a default user who answer the questions
        self.guest = get_user_model().objects.create(username="guest")
        self.default_activity_type = ActivityType.objects.create(type_name="test",
                                                                 description="test")
        self.activity = Activity.objects.create(
            name="test",
            host=self.user,
            location="here",
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=2),
            last_length=60,
            reward=10,
            description="test",
            max_attend=10,
            activity_type=self.default_activity_type
        )
        # create a default questionnaire
        self.questionnaire = Questionnaire.objects.create(activity=self.activity)

        # available choices for multi-choice questions
        self.multi_choice = []
        # a single-choice question
        self.single_choice_question = \
            ChoiceQuestion.objects.create(question="This is a single-choice question for test",
                                          questionnaire=self.questionnaire,
                                          order_in_list=1,
                                          multi_choice=False)
        # available choices for single-choice questions
        self.single_choice = []
        for i in range(0, 4):
            self.single_choice.append(Choice.objects.create(description=("single choice%d" % i),
                                                            order_in_list=i+1,
                                                            question=self.single_choice_question))

        # a multi-choice question
        self.multi_choice_question = \
            ChoiceQuestion.objects.create(question="This is a multi-choice question for test",
                                          questionnaire=self.questionnaire,
                                          order_in_list=2,
                                          multi_choice=True)
        # add choices for this question
        for i in range(0, 4):
            self.multi_choice.append(Choice.objects.create(description=("multi choice%d" % i),
                                                           multi_choice=True,
                                                           order_in_list=i+1,
                                                           question=self.multi_choice_question))

        # create a question answered with text, and this question don't need choices
        self.text_question = \
            NonChoiceQuestion.objects.create(question="This is a text question for test",
                                             questionnaire=self.questionnaire,
                                             order_in_list=3,
                                             type=0)

        # create a question answered with a file
        self.file_question = \
            NonChoiceQuestion.objects.create(question="This is a file question for test",
                                             questionnaire=self.questionnaire,
                                             order_in_list=3,
                                             type=1)

        # 准备答题，创建一个answer_sheet
        self.answer_sheet = AnswerSheet.objects.create(user=self.guest,
                                                       questionnaire=self.questionnaire)

    """下面的测试测试回答问题的功能"""

    def test_answer_a_single_choice_question(self):
        """这个函数测试尝试回答一个单选题，检查是否能够正常检索到答案"""
        selected_choice = Choice.objects.filter(question=self.single_choice_question,
                                                order_in_list=1)[0]
        # 取出的选择应当不是可以复选的
        self.assertEqual(selected_choice.multi_choice, False)
        answer = SingleChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                   question=self.single_choice_question,
                                                   choice=selected_choice)
        # 然后检索这这个问题的所有回答
        answers = SingleChoiceAnswer.objects.filter(question=self.single_choice_question)
        self.assertEqual(answers[0], answer)

    def test_answer_a_multi_choice_question(self):
        selected_choice_1 = Choice.objects.filter(question=self.multi_choice_question,
                                                  order_in_list=1)[0]
        selected_choice_2 = Choice.objects.filter(question=self.multi_choice_question,
                                                  order_in_list=3)[0]
        self.assertTrue(selected_choice_1.multi_choice)
        self.assertTrue(selected_choice_2.multi_choice)

        answer = MultiChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                  question=self.multi_choice_question)
        answer.choices.add(selected_choice_1)
        answer.choices.add(selected_choice_2)

        answers = MultiChoiceAnswer.objects.filter(question=self.multi_choice_question)
        self.assertEqual(answers[0], answer)

    def test_answer_a_text_question(self):
        answer = TextAnswer.objects.create(answer_sheet=self.answer_sheet,
                                           text="This is a test answer",
                                           question=self.text_question)
        answers = TextAnswer.objects.filter(question=self.text_question)
        self.assertEqual(answers[0], answer)

    def test_answer_a_file_question(self):
        test_file_path = os.path.join(settings.BASE_DIR, "Activity", 'testFiles', "test1.jpg")
        answer = FileAnswer.objects.create(answer_sheet=self.answer_sheet,
                                           file=test_file_path,
                                           question=self.file_question)
        answers = FileAnswer.objects.filter(question=self.file_question)
        self.assertEqual(answers[0], answer)

    """下面测试回答的逻辑关系是否正确"""

    def test_single_choice_answer_to_multi_choice_question(self):
        """将单选的答案映射给多选的问题, 应当抛出异常"""
        with self.assertRaises(ValidationError):
            answer_single_choice = SingleChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                                     question=self.multi_choice_question,
                                                                     choice=self.single_choice[0])
            answer_single_choice.save()
        with self.assertRaises(ValidationError):
            answer_single_choice = SingleChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                                     question=self.single_choice_question,
                                                                     choice=self.multi_choice[0])
            answer_single_choice.save()
        with self.assertRaises(ValidationError):
            answer_single_choice = SingleChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                                     question=self.multi_choice_question,
                                                                     choice=self.multi_choice[0])
            answer_single_choice.save()

    def test_multi_choice_answer_to_single_choice_question(self):
        """类似的，这个测试将多选的答案映射给单选的问题, 也应当抛出异常"""
        with self.assertRaises(ValidationError):
            answer_multi_choice = MultiChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                                   question=self.single_choice_question)
            answer_multi_choice.choices.add(self.multi_choice[0])
            answer_multi_choice.save()
        with self.assertRaises(ValidationError):
            answer_multi_choice = MultiChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                                   question=self.single_choice_question)
            answer_multi_choice.choices.add(self.single_choice[0])
            answer_multi_choice.save()
        # 注意下面的这个测试要放在form测试中才能进行
        # with self.assertRaises(ValidationError):
        #     answer_multi_choice = MultiChoiceAnswer.objects.create(user=self.guest,
        #                                                            question=self.multi_choice_question)
        #     answer_multi_choice.choices.add(self.single_choice[0])

    def test_single_choice_question_inconsistent(self):
        """这个函数测试当答案选择的选项和问题不匹配时的问题"""
        # 新建一个single_choice的问题
        new_single_choice_question = \
            ChoiceQuestion.objects.create(question="This is another single-choice question for test",
                                          questionnaire=self.questionnaire,
                                          order_in_list=1,
                                          multi_choice=False)
        new_single_choice = []
        for i in range(0, 4):
            new_single_choice.append(Choice.objects.create(description=("single choice%d" % i),
                                                           order_in_list=i+1,
                                                           question=new_single_choice_question))

        with self.assertRaises(ValidationError):
            answer = SingleChoiceAnswer.objects.create(answer_sheet=self.answer_sheet,
                                                       question=self.single_choice_question,
                                                       choice=new_single_choice[0])
            answer.save()

    """下面测试作为答卷整体的完整性"""

    def test_answer_sheet_integrity_with_error(self):
        count = 0
        if random.random() > 0.5:
            self.test_answer_a_single_choice_question()
            count += 1
        if random.random() > 0.5:
            self.test_answer_a_multi_choice_question()
            count += 1
        if random.random() > 0.5:
            self.test_answer_a_text_question()
            count += 1
        if count != 3 and random.random() > 0.5:
            self.test_answer_a_file_question()
        with self.assertRaises(ValidationError):
            self.answer_sheet.clean()

    def test_answer_sheet_integrity_without_error(self):
        self.test_answer_a_single_choice_question()
        self.test_answer_a_multi_choice_question()
        self.test_answer_a_text_question()
        self.test_answer_a_file_question()
        self.answer_sheet.clean()