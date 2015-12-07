# !coding=utf-8
from Questionnaire.models import Questionnaire
from Activity.models import Activity


def expired_questionnaire_cleaner():
    all_acts = Activity.objects.all()
    for a in all_acts:
        q = Questionnaire.objects.filter(activity=a, is_active=True).order_by('-created_at')
        if q.count() > 1:
            q.update(is_active=False)
            first_q = q[0]
            first_q.is_active = True
            first_q.save()
