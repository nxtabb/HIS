from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
from user.models import User

class IndexGoodsBanner(BaseModel):
    #首页轮播展示商品模型类
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播图片'
        verbose_name_plural=verbose_name
#首页分类展示模型类



class IndexPromotionBanner(BaseModel):
    #首页促销活动类
    name = models.CharField(max_length=20,verbose_name='图片名称')
    image =models.ImageField(upload_to='banner',verbose_name='图片')
    index =models.SmallIntegerField(default=0,verbose_name='展示顺序')
    class Meta:
        db_table= 'df_index_promotion'
        verbose_name='主页图片范例'
        verbose_name_plural = verbose_name
