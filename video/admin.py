from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from video.models import Category, Video, Galeri, Comment, Videoglr


class ProductImageInline(admin.TabularInline):
    model = Galeri
    extra = 5

class VideoImageInline(admin.TabularInline):
    model = Videoglr
    extra = 5

class CategoryAdmin(admin.ModelAdmin):

    list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Video,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Video,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category','image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [ProductImageInline,VideoImageInline]
    prepopulated_fields = {'slug': ('title',)}

class GaleriAdmin(admin.ModelAdmin):
    list_display = ['title', 'video', 'image_tag']
    readonly_fields = ('image_tag',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'video', 'user', 'status', ]
    list_filter = ('status',)

class VideoglrAdmin(admin.ModelAdmin):
    list_display = ['title', 'videos', 'videono','video',]

admin.site.register(Category,CategoryAdmin2)
admin.site.register(Video,VideoAdmin)
admin.site.register(Galeri,GaleriAdmin)
admin.site.register(Videoglr,VideoglrAdmin)
admin.site.register(Comment,CommentAdmin)