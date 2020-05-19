from django.contrib import admin
from user.models import User
# Register your models here.
from django.core.cache import cache
class BaseModelAdmin(admin.ModelAdmin):
    #更新表中数据时调用
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        #清除首页缓存数据
        cache.delete('index_page_data')
    def delete_model(self, request, obj):
        super().delete_model(request,obj)

class UserAdmin(BaseModelAdmin):
    pass
admin.site.register(User,UserAdmin)