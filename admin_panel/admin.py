from django.contrib import admin
from www.models import *
from user_profile.models import *

# Регистрация модели для игры
class MGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating', 'rating_count', 'status', 'date', 'creator', 'get_tags')
    search_fields = ('name', 'description')
    list_filter = ('status', 'category')
    ordering = ('-date',)

    filter_horizontal = ('category',)  # Множественный выбор категорий
    fields = ('name', 'description', 'about', 'status', 'creator', 'category', 'image', 'video')

    # Позволяет редактировать теги для игры
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tegs.all()])  # Исправлено на tag.name, если в вашей модели Teg есть поле name
    get_tags.short_description = 'Tags'

# Удалите вторую регистрацию модели MCategory
@admin.register(MCategory)  # Используйте только эту регистрацию
class MCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображаем список категорий в админке
    search_fields = ('name',)

class MStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображаем id и name в списке
    search_fields = ('name',)  # Добавляем возможность поиска по имени статуса
    list_filter = ('name',)  # Добавляем фильтрацию по имени
    ordering = ('name',)  # Сортировка по имени статуса

class MUserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'birth_date', 'profile_picture')
    search_fields = ('name', 'user__username')
    list_filter = ('birth_date',)

# Теги
class TegAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'status')  # Отображаем связанные теги
    search_fields = ('user__username', 'game__name', 'status__name')
    list_filter = ('status',)

    # Возможность добавлять теги и связывать с играми
    def save_model(self, request, obj, form, change):
        obj.save()
        # Привязка тега к игре
        if obj.game:
            obj.game.tegs.add(obj)
        super().save_model(request, obj, form, change)

class TegListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Избранные игры
class MFavoriteGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'date_added')
    search_fields = ('user__name', 'game__name')

# Регистрация моделей в админке
admin.site.register(MGame, MGameAdmin)
admin.site.register(MStatus, MStatusAdmin)
admin.site.register(MUserProfile, MUserProfileAdmin)
admin.site.register(MFavoriteGame, MFavoriteGameAdmin)
admin.site.register(Teg, TegAdmin)
admin.site.register(TegList, TegListAdmin)
