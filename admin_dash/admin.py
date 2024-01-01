from django.contrib import admin
from admin_dash.models import User, Meal, Daily_Bazar, Daily_Meal, Partial_Meal

# class UserAdmin(admin.ModelAdmin):
    # list_display = ('month', 'total_meal', 'meal_rate', 'total_bazar', 'total_mate', 'status')
admin.site.register(User)

class MealAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_meal', 'meal_rate', 'total_bazar', 'total_mate', 'status')
admin.site.register(Meal, MealAdmin)


class Daily_BazarAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'bazar', 'comment', 'status')
admin.site.register(Daily_Bazar, Daily_BazarAdmin)

class Daily_MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'lunch', 'dinner', 'comment', 'status')
admin.site.register(Daily_Meal, Daily_MealAdmin)

class Partial_MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'day', 'meal', 'status')
admin.site.register(Partial_Meal, Partial_MealAdmin)