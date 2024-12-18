from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Test, Question, Answer, UserResult

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserResult)
