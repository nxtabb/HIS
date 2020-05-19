from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

class User(AbstractUser,BaseModel):
    AUTHORITY = (
        (1, '管理员'),
        (2, '普通用户'),
        (3, '审查员'),
    )
    authority = models.SmallIntegerField(default=2, choices=AUTHORITY,verbose_name='身份')
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name




