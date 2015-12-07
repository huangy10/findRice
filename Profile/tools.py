# !coding=utf-8
import os
import json
from django.conf import settings
from django.contrib.auth.models import User


def load_team_info_from_json(json_file_name='team_info.json'):
    """ 从旧版本的米团系统中导入米团关系数据,输入为json文件
    """
    file_path = os.path.join(settings.BASE_DIR, json_file_name)
    with open(file_path) as f:
        data_string = f.read()
        data = json.loads(data_string)
        for record in data:
            leader_id = record["leader_id"]
            leader = User.objects.get(id=leader_id)
            member_id = record["member_id"]
            member = User.objects.get(id=member_id)
            member.profile.team_leader = leader
            member.save()
