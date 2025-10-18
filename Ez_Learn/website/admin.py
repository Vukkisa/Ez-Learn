from django.contrib import admin
from .models import Learner, learnings, Course, Quiz, Question, Choice, Developer, Payment, Submission_quiz, Query

# Register your models here.

@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'ph_number')
    list_filter = ('state', 'country')
    search_fields = ('username', 'first_name', 'last_name', 'email')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('developer_name', 'email')
    search_fields = ('developer_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount')
    list_filter = ('price',)
    search_fields = ('name', 'description')

@admin.register(learnings)
class LearningsAdmin(admin.ModelAdmin):
    list_display = ('learner', 'course_learning', 'activation')
    list_filter = ('activation', 'course_learning')
    search_fields = ('learner__username', 'course_learning__name')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_number', 'quiz')
    search_fields = ('question',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice', 'question', 'is_correct')
    list_filter = ('is_correct',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'learner', 'course', 'status')
    list_filter = ('status',)
    search_fields = ('order_id', 'learner__username')

@admin.register(Submission_quiz)
class SubmissionQuizAdmin(admin.ModelAdmin):
    list_display = ('Learner', 'Quiz', 'score')
    list_filter = ('Quiz',)
    search_fields = ('Learner__username',)
    raw_id_fields = ('Learner', 'Quiz')

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('learner', 'topic')
    search_fields = ('learner__username', 'topic')

# Customize admin site
admin.site.site_header = "Ez-Learn Administration"
admin.site.site_title = "Ez-Learn Admin"
admin.site.index_title = "Welcome to Ez-Learn Administration"

