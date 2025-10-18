from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    
    path('hello/', views.say_hello, name='say_hello' ),
    #main
     path('', views.main, name='main'),
    #learners
    path('l_login/', views.learner_login, name='learner_login'),
    path('l_register/', views.register_learner, name='register_learner'),
    path('otp/', views.otp_view, name='otp'),
    path('validate_lregistration/', views.valdate_lregistration, name='validate_lregistration'),
    path('complete_profile/<int:id>',views.complete_profile ,name='complete_profile'),
    path('learner_profile/<int:id>', views.learner_profile, name='learner_profile'),
    path('logout/', views.leaner_logout, name='logout'),

    #developer
    path('d_login/', views.developer_login, name='developer_login'),
    path('d_register/', views.register_developer, name='register_developer'),
    path('dotp/', views.developer_otp_view, name='dotp'),
    path('validate_dregistration/', views.valdate_dregistration, name='validate_dregistration'),
    path('d_home/<int:id>', views.developer_home, name='developer_home'),
    path('learner_list/<int:id>', views.learners_list, name='learners_list'),
    path('courses_list/<int:id>', views.courses_list, name='courses_list'),
    path('quiz_list/<int:id>', views.quiz_list, name='quiz_list'),
    path('add_course/<int:id>', views.add_course, name='add_course' ),
    path('edit_course/<int:course_id>/<int:did>', views.edit_course, name='edit_course'),
    path('manage_course_content/<int:course_id>/<int:did>', views.manage_course_content, name='manage_course_content'),
    path('delete_course/<int:id>/<int:did>', views.delete_course, name='delete_course'),
    path('create_quiz/<int:id>', views.quiz_creation_view, name='create_quiz'),
    path('edit_quiz/<int:quiz_id>/<int:did>', views.edit_quiz, name='edit_quiz'),
    path('delete_quiz/<int:id>/<int:did>', views.delete_quiz, name='delete_quiz'),
    path('remove_one_question_from_all_quizzes/<int:did>', views.remove_one_question_from_all_quizzes, name='remove_one_question_from_all_quizzes'),
    path('developer_logout/', views.developer_logout, name='d_logout'),

    #regarding courses
    path('home/<int:id>', views.home, name='home'),
    path('inside_course/<int:id>/<int:cid>', views.course_content, name='learn_course'),
    
    #payments
    path('check_payment/<int:id>/<str:name>', views.check_payment, name='check_payment'),
    path('making_payment/<int:id>', views.making_payment, name='making_payment'),
    path('confirm_payment/<int:id>/<int:lid>', views.confirm_payment, name='confirm_payment'),
    path('verify', views.verify, name='verify'),

    #regarding Quiz
    path('get_quiz/<str:title>/<int:id>/', views.get_into_quiz, name='get_quiz' ),
    path('quiz/<str:title>/<int:id>/', views.take_quiz_view, name='take_quiz'),

    #compiler
    path('run/<int:id>', views.runcode, name='runcode'),
    path('index/<int:id>', views.index, name='index'),

    #certification
    path('get_certificate/<int:id>/<int:cid>', views.get_certificate, name='get_certificate'),

    #others
    path('count', views.choices, name='choices'),
    #query
    path('query/<int:id>', views.query, name='query'),


]

