from django.contrib import admin
from .models import Learner, learnings, Course, Quiz, Question, Choice, Developer, Payment, Submission_quiz

# Register your models here.

admin.site.register([Learner, Developer, Course, learnings, Quiz, Question, Choice, Payment, Submission_quiz])

