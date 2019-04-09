import xadmin
from .models import (
    GoodsCategory,
    Goods,
    GoodsImage,
    Baner,
    IndexAd,
    HotSearchWords,
    )

class GoodsAdmin(object):
    # 显示的列
    list_display = [
        "name", "click_num", "sold_num","fav_num", 
        "shop_price", "goods_brief", "goods_desc", "is_new", "is_hot", "add_time" 
    ]
    # 搜索的列
    search_fields = ['name', ]
    # 列表页可以直接编辑
    list_editable = ["is_hot", 'is_new']

    #过滤器
    list_filter = [
        "name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
        "shop_price", "is_new", "is_hot", "add_time", "category__name"
    ]
    #在添加商品的时候可以添加商品图片
    class GoodsImagesInline(object):
        model = GoodsImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [GoodsImagesInline]

xadmin.site.register(Goods, GoodsAdmin)

class GoodsCategoryAdmin(object):
    """商品类目"""
    list_display = ['name', 'category_type', 'parent_categroy', 'is_tab', 'add_time']
    list_filter = ["category_type", "parent_categroy", "name"]
    search_fields = ['name', ] # 搜索

xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)


class GoodsBrandAdmin(object):
    """首页轮播商品"""
    list_display = ['category', 'image', 'name', 'desc']
    # def get_content(self):
    #     context = super(GoodsBrandAdmin, self).get_content()
    #     if 'form' in context:
    #         context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
    #     return context

class BanerGoodsAdmin(object):
    list_display = ["goods", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]



xadmin.site.register(Baner, BanerGoodsAdmin)
# xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)

xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)