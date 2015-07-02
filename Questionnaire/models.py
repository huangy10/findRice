# coding=utf-8
import uuid

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

from Activity.models import Activity

# Create your models here.


class Questionnaire(models.Model):
    """这个类是整个问卷的抽象"""
    activity = models.ForeignKey(Activity)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = "问卷"
        verbose_name_plural = "问卷"
        ordering = ["-modified_at"]


class Question(models.Model):
    """这个类是单个问题的抽象"""
    question = models.CharField(max_length=200, verbose_name="问题")
    required = models.BooleanField(default=True, help_text="这个问题是否必须回答")

    questionnaire = models.ForeignKey(Questionnaire)
    order_in_list = models.IntegerField(default=1)  # 在问卷列表中的顺序，从1开始

    class Meta:
        """这个表不需要创建，创建其子类的表即可"""
        abstract = True


class ChoiceQuestion(Question):
    """选择题"""
    # choices = models.ManyToManyField(Choice, related_name="question")

    multi_choice = models.BooleanField(default=False, verbose_name="是否为多选")

    class Meta:
        verbose_name = "选择题"
        verbose_name_plural = "选择题"


TEXT_QUESTION_TYPE = 0
FILE_QUESTION_TYPE = 1


class NonChoiceQuestion(Question):
    """主观题"""
    type = models.SmallIntegerField(verbose_name="主观题类型",
                                    choices=(
                                        (TEXT_QUESTION_TYPE, '问答题'),
                                        (FILE_QUESTION_TYPE, '文件题')
                                    ), default=0)

    class Meta:
        verbose_name = "主观题"
        verbose_name_plural = "主观题"


class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, related_name="choices")

    description = models.CharField(max_length=50)

    multi_choice = models.BooleanField(default=False, verbose_name="是否为多选")

    order_in_list = models.IntegerField(default=1)  # 在选项列表中的顺序，从1开始

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = "选项"


class AnswerSheet(models.Model):
    """答卷的抽象"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)      # 答题者
    questionnaire = models.ForeignKey(Questionnaire)     # 对应问卷

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def clean(self):
        # 检索出必答的题目
        questions = ChoiceQuestion.objects.filter(questionnaire=self.questionnaire, required=True)
        single_choice_answer_num = SingleChoiceAnswer.objects.filter(answer_sheet=self,
                                                                     question__in=questions).count()
        multi_choice_answer_num = MultiChoiceAnswer.objects.filter(answer_sheet=self,
                                                                   question__in=questions).count()
        if len(questions) != single_choice_answer_num+multi_choice_answer_num:
            raise ValidationError("有未做的必答选择题")
        questions = NonChoiceQuestion.objects.filter(questionnaire=self.questionnaire, required=True)
        text_answer_num = TextAnswer.objects.filter(answer_sheet=self, question__in=questions).count()
        file_answer_num = FileAnswer.objects.filter(answer_sheet=self, question__in=questions).count()
        if len(questions) != text_answer_num+file_answer_num:
            raise ValidationError("有未做的必答非选择题")

    class Meta:
        verbose_name = "答卷"
        verbose_name_plural = "答卷"


class Answer(models.Model):
    """答案的基类"""
    answer_sheet = models.ForeignKey(AnswerSheet)

    class Meta:
        abstract = True


class SingleChoiceAnswer(Answer):
    """单选题的答案"""
    choice = models.ForeignKey(Choice, related_name="single_choice_answers")  # 单选题
    question = models.ForeignKey(ChoiceQuestion, related_name="single_choice_answer_set")

    def clean(self):
        def consistence_check():
            """这个函数在保存之前检查数据之间的一致性"""
            if self.question.multi_choice:
                raise ValidationError("类型冲突：多选题配单选答案")
            if self.choice.multi_choice:
                raise ValidationError("类型冲突：单选答案配多选选项")
            choice_set = Choice.objects.filter(question=self.question)
            if choice_set is None or self.choice not in choice_set:
                raise ValidationError("类型冲突：选项与问题不匹配")
            return True
        consistence_check()

    def save(self, *args, **kwargs):
        self.clean()
        super(SingleChoiceAnswer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "单选题"
        verbose_name_plural = "单选题"


class MultiChoiceAnswer(Answer):
    """多选题的答案"""
    choices = models.ManyToManyField(Choice, related_name="multi_choice_answers")
    question = models.ForeignKey(ChoiceQuestion, related_name="multi_choice_answers")

    def clean(self):
        def consistence_check():
            """这个函数在保存之前检查数据之间的一致性，注意选项与问题的匹配在这里无法完成，会放在form中做"""
            if not self.question.multi_choice:
                raise ValidationError("类型冲突：多选题配单选答案")
            choice_set = Choice.objects.filter(question=self.question)
            if choice_set is None:
                raise ValidationError("类型冲突：问题无答案")
            return True
        consistence_check()

    def save(self, *args, **kwargs):
        self.clean()
        super(MultiChoiceAnswer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "多选题"
        verbose_name_plural = "多选题"


class TextAnswer(Answer):
    """文字题的答案"""
    text = models.TextField()
    question = models.ForeignKey(NonChoiceQuestion)

    class Meta:
        verbose_name = "简答题"
        verbose_name_plural = "简答题"


def get_file_name_from_date(act, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    tz = timezone.get_current_timezone()
    time = tz.normalize(act.created_at)
    return "file_answers/%s/%s/%s/%s" % (time.year, time.month, time.day, filename)


class FileAnswer(Answer):
    file = models.FileField(upload_to=get_file_name_from_date)
    question = models.ForeignKey(NonChoiceQuestion)

    class Meta:
        verbose_name = "文件题"
        verbose_name_plural = "文件题"