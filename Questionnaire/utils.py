# coding=utf-8
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Questionnaire
from .models import ChoiceQuestion, NonChoiceQuestion
from .models import TEXT_QUESTION_TYPE, FILE_QUESTION_TYPE
from .models import Choice
from .models import SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer, AnswerSheet


QUESTIONNAIRE_ERROR_MESSAGES = {
    "question_type_error": "错误的问题类型",
    "wrong_choice_number": "错误的选项数量",
    "no_questionnaire_found": "未找到问卷数据",
    "missing_element": "问卷元素缺失"
}


def json_is_valid(json):
    if "criteria" not in json:
        raise ValidationError(QUESTIONNAIRE_ERROR_MESSAGES["no_questionnaire_found"],
                              code="no_questionnaire_found")
    questions_json = json["criteria"]
    for q in questions_json:
        if "q" not in q or "type" not in q:
            raise ValidationError(QUESTIONNAIRE_ERROR_MESSAGES["missing_element"],
                                  code="missing_element")
        if q["type"] not in ["radio", "checkbox", "question", "upload"]:
            raise ValidationError(QUESTIONNAIRE_ERROR_MESSAGES["question_type_error"],
                                  code="question_type_error")
        if q["type"] == "radio" or q["type"] == "checkbox":
            if "a" not in q:
                raise ValidationError(QUESTIONNAIRE_ERROR_MESSAGES["missing_element"],
                                      code="missing_element")
            else:
                if len(q) < 2 or len(q) > 30:
                    raise ValidationError(QUESTIONNAIRE_ERROR_MESSAGES["wrong_choice_number"],
                                          code="wrong_choice_number")
    return None


def create_questionnaire_with_json(json, activity, is_active=True):
    """
    这个函数通过json格式的数据为一个给定的活动创建问卷
    json数据会先利用上面定义的json_is_valid来检查integrity
    """
    # 首先检查传递过来的json字典是否符合格式
    json_is_valid(json)
    questionnaire = Questionnaire.objects.create(activity=activity, is_active=is_active)
    questions_json = json["criteria"]
    i = 1
    for question_json in questions_json:
        if question_json["type"] == "radio":
            question = ChoiceQuestion.objects.create(questionnaire=questionnaire,
                                                     order_in_list=i,
                                                     question=question_json["q"],
                                                     multi_choice=False)
            i += 1
            k = 0
            for c in question_json["a"]:
                Choice.objects.create(question=question,
                                      description=c,
                                      multi_choice=False,
                                      order_in_list=k)
                k += 1
        elif question_json["type"] == "checkbox":
            question = ChoiceQuestion.objects.create(questionnaire=questionnaire,
                                                     order_in_list=i,
                                                     question=question_json["q"],
                                                     multi_choice=True)
            i += 1
            k = 0
            for c in question_json["a"]:
                Choice.objects.create(question=question,
                                      description=c,
                                      multi_choice=True,
                                      order_in_list=k)
                k += 1
        elif question_json["type"] == "question":
            NonChoiceQuestion.objects.create(questionnaire=questionnaire,
                                             order_in_list=i,
                                             question=question_json["q"],
                                             type=TEXT_QUESTION_TYPE)
            i += 1
        elif question_json["type"] == "upload":
            NonChoiceQuestion.objects.create(questionnaire=questionnaire,
                                             order_in_list=i,
                                             question=question_json["q"],
                                             type=FILE_QUESTION_TYPE)
            i += 1
    return questionnaire


def answer_json_is_valid(json, request):
    pass


def create_answer_set_with_json(json, request, questionnaire, user):
    """
    这个函数利用json的数据创建一个针对给定问卷的答案
    这里还需要通过创建这个回答的用户
    以及request对象，这个函数会从request.FILE里面获取文件题的答案
    同样，在执行创建任务之前，会先检查json数据的完整性
    """
    answer_json_is_valid(json, request)
    # 创建一个答卷
    answer_set = AnswerSheet.objects.create(user=user,
                                            questionnaire=questionnaire)
    questions = list(questionnaire.choicequestion_set.all()) + list(questionnaire.nonchoicequestion_set.all())
    try:
        for (q, q_json) in zip(questions, json["answer"]):
            if q_json["type"] == "radio":
                c = Choice.objects.get(question=q, order_in_list=q_json["result"])
                SingleChoiceAnswer.objects.create(answer_sheet=answer_set,
                                                  choice=c,
                                                  question=q)
            elif q_json["type"] == "checkbox":
                answer = MultiChoiceAnswer.objects.create(answer_sheet=answer_set,
                                                          question=q)
                choice_set = q.choices.all().order_by("order_in_list")
                for c_no in q_json["result"]:
                    answer.choices.add(choice_set[c_no])
            elif q_json["type"] == "question":
                TextAnswer.objects.create(answer_sheet=answer_set,
                                          question=q,
                                          text=q_json["result"])
            elif q_json["type"] == "upload":
                FileAnswer.objects.create(answer_sheet=answer_set,
                                          question=q,
                                          file=request.FILES[q_json["name"]])
    except (ObjectDoesNotExist, IndexError):
        # 发生错误之后删除已经创建的答卷
        answer_set.delete()
        raise ValidationError()
    return answer_set
