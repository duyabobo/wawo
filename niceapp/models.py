# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from wawo.settings import ONE_PAGE_LIMIT
# Create your models here.


class BaseModel(models.Model):
    """基础扩展类"""
    created_at = models.DateTimeField('创建记录时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改日期', auto_now=True)

    @classmethod
    def get_total(cls):
        """
        查询总数
        :return:
        """
        return cls.objects.all().count()

    @classmethod
    def get_items(cls, page=0, limit=ONE_PAGE_LIMIT):
        """
        分页查询最多前 limit 条记录
        :param page:
        :param limit:
        :return:
        """
        return cls.objects.all().order_by('serial_number')[page*limit: (page+1)*limit]

    class Meta:
        abstract = True


class MessageCode(BaseModel):
    """用户短信码"""
    user_id = models.IntegerField('uid', default=0)
    usage = models.IntegerField('用途：0登陆，1推荐通知，2...', default=0)
    mobile = models.IntegerField('手机号', default=0)
    code = models.IntegerField('四位短信码', default=0)

    class Meta:
        db_table = 'message_code'

    @classmethod
    def insert_message_code(cls, mobile, code, sex, usage=0):
        """
        查询一个 user_id
        :param mobile:
        :param code:
        :param sex:
        :param usage:
        :return:
        """
        user = Users.insert_user(mobile=mobile, sex=sex)
        message_code = MessageCode(user_id=user.id, mobile=mobile, code=code, usage=usage)
        return message_code.save()

    @classmethod
    def check_code(cls, mobile, code):
        """
        查询一个 user_id
        :param mobile:
        :param code:
        :return:
        """
        message_code = cls.objects.values('user_id').filter(usage=0, mobile=mobile, code=code).first()
        # todo 验证码有效期以及是否已使用检查
        return message_code['user_id'] if message_code else None


class Users(AbstractUser):
    """用户信息表"""
    # 个人必备信息
    mobile = models.IntegerField('手机号', default=0)
    sex = models.IntegerField('性别: 0女 1男', default=0)
    info_status = models.IntegerField('账号状态: 0已注册，1完善，2已接触，3已恋爱，-1已过期，-2已投诉，-3已被投诉', default=0)
    real_name_status = models.IntegerField('恋爱状态：0未实名，1一级实名，2二级实名，3三级实名，4四级实名', default=0)
    # 条件数据：女的就是期望男友条件数据，男的就是自身的条件数据
    city = models.CharField('城市名', max_length=100, default='')
    school = models.CharField('学校名', max_length=100, default='')
    stature = models.IntegerField('身高(cm)', default=0)
    weight = models.IntegerField('体重(kg)', default=0)
    appearance = models.IntegerField('相貌: 0不要求，1干净整洁，2阳光自信，3英俊帅气，12，13，23为组合...', default=0)
    character = models.IntegerField('性格：1暴躁，2温柔，3细心，4...', default=0)
    hobby = models.IntegerField('兴趣：0无，1动漫，2足球，3乒乓球，4...', default=0)
    speciality = models.CharField('特长：0无，1吉他，2诗词，3哲学，4画画，5...', max_length=100, default=0)
    habit = models.IntegerField('习惯：0无，...', default=0)
    disgust = models.IntegerField('厌恶的事情：0无，1娘娘腔，2小气鬼，3脏话连篇，4不守信用，5...', default=0)
    wealth = models.IntegerField('财富：每月生活费多少元', default=0)
    custom = models.CharField('自定义的男生的描述人生理想啊啥的或女生自定义的一些要求', max_length=255, default='')
    threshold_fee = models.IntegerField('门槛费', default=10)
    # 实名制信息
    student_identity_card_qiniu_uri = models.CharField('学生证照片七牛云存储对应的uri', max_length=500, default='')
    name = models.CharField('姓名', max_length=20, default='')
    age = models.IntegerField('年龄', default=0)
    college = models.CharField('院系名', max_length=100, default='')
    profession = models.CharField('专业名', max_length=100, default='')
    school_num = models.CharField('学号', max_length=100, default='')

    class Meta(AbstractUser.Meta):
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'

    @classmethod
    def get_one(cls, user_id):
        """
        查询一个 user 记录
        :param user_id:
        :return:
        """
        return cls.objects.filter(id=user_id).first()

    @classmethod
    def get_one_by_mobile(cls, mobile):
        """
        查询一个 user 记录
        :param mobile:
        :return:
        """
        return cls.objects.filter(mobile=mobile).first()

    @classmethod
    def get_test_user(cls):
        """
        获取测试用户
        :return:
        """
        return cls.objects.first()

    @classmethod
    def update_one_record(cls, user_id, **kwargs):
        """
        更新用户信息
        :param user_id:
        :return:
        """
        return cls.objects.filter(id=user_id).update(**kwargs)

    @classmethod
    def update_one_record_one_field(cls, user_id, **kwargs):
        """
        更新用户某个字段
        :param user_id:
        :return:
        """
        return cls.objects.filter(id=user_id).update(**kwargs)

    @classmethod
    def insert_user(cls, mobile=mobile, sex=sex):
        """
        插入一条用户记录
        :param mobile:
        :param sex:
        :return:
        """
        user = Users.get_one_by_mobile(mobile)
        if not user:  # todo 需要检查是否用户信息过期了
            user = Users(mobile=mobile, sex=sex, username=random.random())
        else:
            user.sex = sex
        user.save()
        return user


class UserRelation(BaseModel):
    """用户关系表"""
    boy_id = models.IntegerField('男孩id', default=0)
    girl_id = models.IntegerField('女孩id', default=0)
    relation = models.IntegerField('0已通知/1已查阅/2已邀请/3已接触/4已恋爱/5已分手/6已投诉', default=0)

    class Meta:
        db_table = 'user_relation'


# 性别
FEMALE = 0
MALE = 1
# 账号状态
REGISTERED = 0
SUBMIT = 1
CONNECTED = 2
FALLINLOVE = 3
EXPIRED = -1
COMPLAIN = -2
COMPLAINED = -3
# 恋爱状态
NOTREALNAME = 0
REALNAME_1 = 1
REALNAME_2 = 2
REALNAME_3 = 3
REALNAME_4 = 4
