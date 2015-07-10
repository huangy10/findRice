# coding=utf-8
import os

from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from Activity.models import Activity
from Questionnaire.utils import create_questionnaire_with_json
from Questionnaire.models import Questionnaire
from Questionnaire.models import AnswerSheet, SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer
from Questionnaire.models import Choice

def test_create_question():
    json = {
        "criteria": [
            {
                "q": "单选题",
                "type": "radio",
                "a": ["A", "B", "C"]
            }, {
                "q": "多选题",
                "type": "checkbox",
                "a": ["A", "B", "C"]
            }, {
                "q": "文字题",
                "type": "question",
            }, {
                "q": "文件题",
                "type": "upload",
            }
        ]
    }

    activity = Activity.objects.all()[1]
    create_questionnaire_with_json(json, activity)


def test_create_answer():
    test_file_obj = open(os.path.join(settings.MEDIA_ROOT, "default_avatars", "default_avatar.jpg"))
    test_file = File(test_file_obj)
    json = {
        "answer": [
            {
                "result": 1,
                "type": "radio"
            }, {
                "result": [0, 1],
                "type": "checkbox"
            }, {
                "result": "这是一个测试答案",
                "type": "question"
            }, {
                "result": test_file,
                "type": "upload"
            }
        ]
    }
    q = Questionnaire.objects.all()[0]
    u = get_user_model().objects.filter(username="lena")[0]
    test_create_answer_set_with_dict(json, q, u, test_file)
    test_file.close()


def test_create_answer_set_with_dict(dict, questionnaire, user, test_file):

    answer_set = AnswerSheet.objects.create(user=user,
                                            questionnaire=questionnaire)

    try:
        for (q, q_json) in zip(questionnaire.choicequestion_set.all(), dict["answer"]):
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
                                          file=test_file)
    except (ObjectDoesNotExist, IndexError):
        # 发生错误之后删除已经创建的答卷
        print "A"
        answer_set.delete()
        return False

    return True