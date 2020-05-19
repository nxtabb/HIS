from django.shortcuts import render,redirect
from django.views.generic import View
from plat.models import IndexGoodsBanner, IndexPromotionBanner
from django.core.paginator import Paginator
from user.models import User
from django.conf import settings
class IndexView(View):
    def get(self, request):
        # 获取首页轮播信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')  # 排序
        # 获取首页右侧图片信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        context = {'goods_banners': goods_banners,
                   'promotion_banners': promotion_banners,}

        return render(request, 'index.html', context)