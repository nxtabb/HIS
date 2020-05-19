from django.contrib import admin
from django.core.cache import cache
class BaseModelAdmin(admin.ModelAdmin):
    #更新表中数据时调用
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.delete('index_page_data')
    def delete_model(self, request, obj):
        super().delete_model(request,obj)

