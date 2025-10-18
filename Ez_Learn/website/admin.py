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

# Enhanced Admin Site Customization
admin.site.site_header = "🔧 Ez-Learn Administration"
admin.site.site_title = "Ez-Learn Admin Portal"
admin.site.index_title = "Welcome to Ez-Learn Administration Dashboard"

# Custom admin site configuration for better UX
admin.site.site_url = "/"
admin.site.enable_nav_sidebar = True
admin.site.empty_value_display = "❌ Not Set"

# Set custom login template
admin.site.login_template = "admin/login.html"

# Enhanced Admin Configuration with better user experience
from django.urls import path, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

@never_cache
@staff_member_required
def admin_dashboard_stats(request):
    """Custom admin dashboard with stats"""
    try:
        stats = {
            'total_learners': Learner.objects.count(),
            'total_courses': Course.objects.count(), 
            'total_payments': Payment.objects.count(),
            'successful_payments': Payment.objects.filter(status=True).count(),
            'total_quizzes': Quiz.objects.count(),
            'total_developers': Developer.objects.count(),
            'pending_payments': Payment.objects.filter(status=False).count(),
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Set custom templates
admin.site.login_template = "admin/login.html"
admin.site.index_template = "admin/index.html"

# Create a custom admin site that includes our dashboard stats
class CustomAdminSite(admin.AdminSite):
    """Custom admin site with enhanced dashboard"""
    
    def get_urls(self):
        """Add custom URLs to admin site"""
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-stats/', admin_dashboard_stats, name='admin_dashboard_stats'),
        ]
        return custom_urls + urls

# Replace the default admin site with our custom one
admin.site.__class__ = CustomAdminSite

