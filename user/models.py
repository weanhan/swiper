import datetime

from django.db import models
from django.utils.functional import cached_property

from lib.orm import ModelMixin

class User(models.Model, ModelMixin):
    SEX = (
        ('male', '男'),
        ('female', '女')
    )
    phonenum = models.CharField(max_length=20, unique=True, verbose_name="手机号")
    nickname = models.CharField(max_length=32, unique=True, verbose_name="昵称")
    sex = models.CharField(max_length=8, choices=SEX, verbose_name="性别")
    birth_year = models.IntegerField(default=2000, verbose_name="出生年")
    birth_month = models.IntegerField(default=1, verbose_name="出生月")
    birth_day = models.IntegerField(default=1, verbose_name="出生日")
    avatar = models.CharField(max_length=200, verbose_name="个人形象")
    location = models.CharField(max_length=20, verbose_name="常居地")



    @cached_property
    def age(self):
        today = datetime.date.today()
        birth_day = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        birth_timedelta = today - birth_day
        return birth_timedelta.days // 365

    @property
    def profile(self):
        # profile, _ = Profile.objects.get_or_create(id=self.id)
        # return profile
        # 查看自身有没有查询有_profile属性，如果没有就从数据库中查询
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)

        return self._profile

    # def to_string(self):
    #     return {
    #         "phonenum": self.phonenum,
    #         "nickname": self.nickname,
    #         "sex": self.sex,
    #         "birth_year": self.birth_year,
    #         "birth_month": self.birth_month,
    #         "birth_day": self.birth_day,
    #         "avatar": self.avatar,
    #         "location": self.location
    #     }
    # def to_string(self):
    #     model_dict = {}
    #     allfields = self._meta.get_fields()
    #     for field in allfields:
    #         model_dict[field.attname] = getattr(self, field.attname)
    #     return model_dict


class Profile(models.Model, ModelMixin):
    SEX = (
        ('male', '男'),
        ('female', '女')
    )

    location = models.CharField(max_length=20, verbose_name="目标城市")
    min_distance = models.IntegerField(default=1, verbose_name="最小查找范围")
    max_distance = models.IntegerField(default=10, verbose_name="最大查找范围")
    min_dating_age = models.IntegerField(default=18, verbose_name="最小交友年龄")
    max_dating_age = models.IntegerField(default=50, verbose_name="最大交友年龄")
    dating_sex = models.CharField(max_length=8, choices=SEX, verbose_name="匹配的性别")
    vibration = models.BooleanField(default=True, verbose_name="开启震动")
    only_matche = models.BooleanField(default=True, verbose_name="不让为匹配的人看我的相册")
    auto_play = models.BooleanField(default=True, verbose_name="自动播放视频")

    # 已继承
    # def to_string(self):
    #     model_dict = {}
    #     allfields = self._meta.get_fields()
    #     for field in allfields:
    #         model_dict[field.attname] = getattr(self, field.attname)
    #     return model_dict