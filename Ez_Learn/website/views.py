from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import math
import random
from django.contrib.auth.models import User, Group
from .models import Learner,learnings, Course, Choice, Question, Quiz, Payment, Submission_quiz, Query
from .models import Developer as D
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import razorpay
from Ez_Learn.settings import KEY_ID,KEY_SECRET
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
import sys
from django.template.loader import get_template
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None


# Create your views here.

#saying hello (for basic configuration)

def say_hello(request):
    return HttpResponse(f'<h1>Hello how are welocome to my project of ez_learn <h1>')

#generating otp
def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

#sending main while logged in
def sending_mail(message, otp, email):
    if otp != '':
        send_mail("hello somu", f'{message} {otp}', "somasekhar_devisetty3@gmail.com",[email])
    else:
        send_mail("hello somu", f'{message}', "somasekhar_devisetty3@gmail.com",[email])

#compiler functions
def index(request, id):
    learner = Learner.objects.get(id=id)
    return render(request, 'compiler/pycompiler.html', {'learner':learner})


def runcode(request, id):
    learner = Learner.objects.get(id=id)
    if request.method == "POST":
        codeareadata = request.POST['codearea']
        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(codeareadata)
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout=orig_stdout
            output = e
    return render(request , 'compiler/pycompiler.html', {"code":codeareadata , "output":output, 'learner':learner})



def main(request):
    return render(request, 'main_template.html')



# funtion for registering a learner (from here)
def register_learner(request):
    if request.method == 'POST':
        request.session['username'] = request.POST['username']
        request.session['firstname'] = request.POST['firstname']
        request.session['lastname'] = request.POST['lastname']
        request.session['email'] = request.POST['email']
        request.session['password'] = request.POST['password']
        request.session['otp'] = generateOTP()
        print(request.session['otp'])
        message = 'your otp to complete the registration of ez_learn is '
        print(message)
        sending_mail(message, request.session['otp'], request.session['email'])
        sending_mail(message, request.session['otp'], request.session['email'])
        return redirect('otp')
    return render(request, 'learner_register.html')

#showing otp template
def otp_view(request):
    return render(request, 'otp.html')

#validating registered details
def valdate_lregistration(request):
    context = {}
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        try:
            if entered_otp == request.session['otp']:
                print('somu')
                username= request.session['username']
                firstname = request.session['firstname']
                lastname = request.session['lastname']
                email = request.session['email']
                password = request.session['password']
                user = User.objects.create_user(username = username , password = password)
                print('hii')
                learner_ = Learner.objects.create(username = username, first_name= firstname, last_name = lastname, email = email, user = user)
                print('somu')
                courses = Course.objects.all()
                print(courses)
                print(learner_)
                for course in courses:
                    c = Course.objects.get(id = course.id)
                    print(c)
                    print(course)
                    learning = learnings(learner= learner_, course_learning= c, activation= False)
                    learning.save()
                print('somu')
                return render(request, 'learner/successful.html' ,{'learner' : learner_})
            else:
                context['error_message'] = 'enter valid otp'
        except:
            error = 'Username already exist'
            return render(request, 'learner_register.html', {'error': error})
    return render(request, 'otp.html', context)


#complete profile
def complete_profile(request, id):
    learner = Learner.objects.get(id=id)
    if request.method == 'GET':
        print(learner)
        form = imageForm()
        print(form)
        return render(request, 'personal.html', {'learner':learner, 'form': form})
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('profile_picture')
            print(img)
            learner.dno = request.POST.get('house_no')
            learner.street = request.POST.get('street')
            learner.city = request.POST.get('city')
            learner.state = request.POST.get('state')
            learner.country = request.POST.get('country')
            learner.pincode = request.POST.get('pincode')
            learner.ph_number= request.POST.get('phone_no')
            learner.DOB = request.POST.get('dob')
            learner.profile_picture = img
            learner.save()
            return redirect('learner_login')
        


#learner login function
def learner_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        u = authenticate(username= username , password = password)
        if u is not None:
            learner = Learner.objects.get(user = u)
            email = learner.email
            #message = 'you just logged into you ezlearn account'
            #sending_mail(message,'',email)
            login(request, u)
            courses = Course.objects.all()
            return redirect('home' , learner.id)
        else:
            context['error'] = 'wrong username or password'
    return render(request, 'learner_login.html', context)


# home page of learner
@login_required
def home(request, id):
    learner = Learner.objects.get(id=id)
    courses = Course.objects.all()
    return render(request, 'learner/home.html', {
                                                        'learner': learner,
                                                        'courses' : courses 
                                                        })

def highest_score(request, id):
    pass


#getting learners personal details
def learner_profile(request, id):
    learner = Learner.objects.get(id =id)
    return render(request, 'learner/profile.html', {'learner' : learner})


#getting into particular course
def course_content(request, id, cid):
    learner = Learner.objects.get(id = id)
    course = Course.objects.get(id = cid)
    
    # Check if learner has access to this course
    try:
        learning = learnings.objects.get(learner=learner, course_learning=course)
        has_full_access = learning.activation
    except learnings.DoesNotExist:
        # Create learning record if it doesn't exist
        learning = learnings.objects.create(learner=learner, course_learning=course, activation=False)
        has_full_access = False
    
    if course.name == 'PYTHON':
        if request.method == 'POST':
            if request.POST.get('basics') == 'basics':
                return render(request, 'courses/python/basics.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
            if request.POST.get('intermediate') == 'intermediate':
                if has_full_access:
                    return render(request, 'courses/python/intermediate.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {'learnt': learning, 'message': 'Please purchase the course to access intermediate content.'})
            if request.POST.get('advanced') == 'advanced':
                if has_full_access:
                    return render(request, 'courses/python/advanced.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {'learnt': learning, 'message': 'Please purchase the course to access advanced content.'})
        return render(request, 'courses/python/open.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access, 'learning': learning})
    elif course.name == 'HTML':
        if request.method == 'POST':
            if request.POST.get('basics') == 'basics':
                return render(request, 'courses/html/basics.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
            if request.POST.get('intermediate') == 'intermediate':
                if has_full_access:
                    return render(request, 'courses/html/intermediate.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {'learnt': learning, 'message': 'Please purchase the course to access intermediate content.'})
            if request.POST.get('advanced') == 'advanced':
                if has_full_access:
                    return render(request, 'courses/html/advanced.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {'learnt': learning, 'message': 'Please purchase the course to access advanced content.'})
        return render(request, 'courses/html/open.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access, 'learning': learning})
    elif course.name == 'CSS':
        if request.method == 'POST':
            if request.POST.get('basics') == 'basics':
                return render(request, 'courses/css/basics.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
            if request.POST.get('intermediate') == 'intermediate':
                if has_full_access:
                    return render(request, 'courses/css/intermediate.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {'learnt': learning, 'message': 'Please purchase the course to access intermediate content.'})
            if request.POST.get('advanced') == 'advanced':
                if has_full_access:
                    return render(request, 'courses/css/advanced.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {'learnt': learning, 'message': 'Please purchase the course to access advanced content.'})
        return render(request, 'courses/css/open.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access, 'learning': learning})




#getting quizes layed by the particular persona
def get_into_quiz(request, title, id):
    learner = Learner.objects.get(id=id)
    course = Course.objects.get(name=title)
    quiz = Quiz.objects.get(course=course)
    try:
        submissions = Submission_quiz.objects.filter(Learner= learner,  Quiz  = quiz)
        return render(request, 'quiz/quizs_played.html', {'learner':learner, 'course' : course, 'submissions': submissions})
    except:
        return render(request, 'quiz/quizs_played.html', {'learner':learner, 'course' : course})


@login_required
def take_quiz_view(request, title, id):
    learner = Learner.objects.get(id=id)
    course = Course.objects.get(name=title)
    print(learner.username)
    quiz = Quiz.objects.get(course=course)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        submitted_answers = [request.POST.get(str(question.id)) for question in questions]
        score = 0
        results = []
        selected_choices = {}
        for i in range(len(questions)):
            question = questions[i]
            correct_choice = Choice.objects.get(question=question, is_correct=True)
            print(correct_choice)
            submitted_answer = submitted_answers[i]

            if submitted_answer == str(correct_choice.id):
                score += 1

            choices = question.choice_set.all()
            options = [choice.choice for choice in choices]

            result = {
                'question_number':question.question_number,
                'options' : options,
                'question_text': question.question,
                'submitted_answer': Choice.objects.get(id=submitted_answer).choice if submitted_answer else 'Not answered',
                'correct_answer': correct_choice.choice,
            }
            results.append(result)
            selected_choices[str(question.id)] = submitted_answer

        submissions = Submission_quiz.objects.create(Learner=learner, Quiz= quiz, score = score)
        context = {'quiz': quiz, 'questions': questions, 'results': results, 'score': score, 'learner':learner}
        return render(request, 'quiz/result.html', context)

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions, 'course':course, 'learner':learner})

def get_certificate(request, id , cid):
    learner = Learner.objects.get(id = id)
    course = Course.objects.get(id = cid)
    quiz_ = Quiz.objects.filter(course = course)
    quiz = quiz_[0]
    try:
        submissions = Submission_quiz.objects.filter(Learner = learner, Quiz = quiz)
        maximum_score = max([submission.score for submission in submissions])
        # highest_score = request.session[f'highest_score_{course.name}']
        if maximum_score >= 15:
            if pisa is not None:
                template_path = 'certificate.html'
                context = {'learner': learner}
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'filename="report.pdf"'
                template = get_template(template_path)
                html = template.render(context)
                pisa_status = pisa.CreatePDF(html, dest=response)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            else:
                # Fallback when xhtml2pdf is not available
                return HttpResponse(f'Certificate ready for {learner.username}! (PDF generation not available)')
        else:
            error = f'Your all time highest quiz score in this course is {maximum_score}. You need to get minimum of 15 to get the certificate'
            return render(request, 'quiz/no_quiz_taken.html' , {'error': error, 'learner': learner, 'course': course, 'score': maximum_score})
    except:
        error = f'Not yet participated in any quiz'
        return render(request, 'quiz/no_quiz_taken.html' ,{'error': error, 'learner': learner, 'course': course})
    

#learner logout 
def leaner_logout(request):
    logout(request)
    return redirect('learner_login')


#payments
#checking whether the payment is already done or not
def check_payment(request, id, name):
    learner = Learner.objects.get(id= id)
    course = Course.objects.get(name= name)
    try:
        learnt_list = learnings.objects.filter(learner=learner, course_learning=course)
        if learnt_list.exists():
            learnt = learnt_list[0]
            if learnt.activation == True:
                return redirect('learn_course', learner.id, course.id)
            else:
                # Allow access to course content even without payment - basics are free
                return redirect('learn_course', learner.id, course.id)
        else:
            # Create learning record if it doesn't exist
            learnt = learnings.objects.create(learner=learner, course_learning=course, activation=False)
            return redirect('learn_course', learner.id, course.id)
    except Exception as e:
        return redirect('learn_course', learner.id, course.id)


#making_payment 
def making_payment(request, id):
    learnt = learnings.objects.get(id=id)
    course = learnt.course_learning
    learner = learnt.learner
    if request.method == 'POST':
        if KEY_ID and KEY_SECRET:
            client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
            order = client.order.create({'amount' : 50000, 'currency': 'INR'})
        else:
            # Fallback for development when Razorpay keys are not set
            order = {'id': 'test_order_123'}
        print(order)
        uid = order['id']
        payment = Payment.objects.create(order_id = uid, course = course, learner= learner)
        return redirect('confirm_payment', payment.id, learnt.learner.id)
    return render(request, 'payment/bying_course.html', {'learnt':learnt})

#confirming payment
def confirm_payment(request, id, lid):
    payment = Payment.objects.get(id=id)
    learner = Learner.objects.get(id =lid)
    return render(request, 'payment/confirm_payment.html', {'payment':payment, 'learner':learner})


#verfying payment
@csrf_exempt
def verify(request):
    if request.method == 'POST':
        data  = request.POST
        print(data)
        payment = Payment.objects.get(order_id = data['razorpay_order_id'])
        payment.payment_id = data['razorpay_payment_id']
        payment.status = True
        payment.save()
        id = payment.learner.id
        learnt_list = learnings.objects.filter(course_learning= payment.course, learner = payment.learner)
        learnt = learnt_list[0]
        learnt.activation = True
        learnt.save()
        print(learnt)
        return redirect('home', id )

# developer registration
def register_developer(request):
    if request.method == 'POST':
        request.session['name'] = request.POST['developer_name']
        request.session['email'] = request.POST['email']
        request.session['password'] = request.POST['password']
        request.session['otp'] = generateOTP()
        print(request.session['otp'])
        message = 'your otp to complete the registration of ez_learn is '
        print(message)
        sending_mail(message, request.session['otp'], request.session['email'])
        return redirect('dotp')
    return render(request, 'developer_register.html')



def developer_otp_view(request):
    return render(request, 'developer_otp.html')



def valdate_dregistration(request):
    context = {}
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session['otp']:
            name = request.session['name']
            email = request.session['email']
            password = request.session['password']
            user = User.objects.create_user(username = name , password = password)
            developer_group = Group.objects.get(name='developer')
            user.groups.add(developer_group)
            developer = D.objects.create(user = user, developer_name=name, email = email)
            return render(request, 'developer/successful.html')
    return render(request, 'otp.html', context)

#developer login
def developer_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        u = authenticate(username= username , password = password)
        if u is not None:
            developer = D.objects.get(user = u)
            email = developer.email
            #message = 'you just logged into you ezlearn account'
            #sending_mail(message,'',email)
            login(request, u)
            return redirect('developer_home', developer.id)
        else:
            context['error'] = 'wrong username or password'
    return render(request, 'developer_login.html', context)


#@permission_required('school.change_student', login_url='login')
@login_required
def developer_home(request, id):
    developer = D.objects.get(id=id)
    return render(request, 'developer/dhome.html', {'developer': developer})



@login_required
def learners_list(request, id):
    developer = D.objects.get(id=id)
    Learners = Learner.objects.all()
    return render(request, 'developer/learners_list.html', {'developer':developer,'learners' : Learners})



@login_required
def courses_list(request, id):
    developer = D.objects.get(id=id)
    courses = Course.objects.all()
    return render(request, 'developer/courses_list.html', {'developer': developer,'courses': courses})



@login_required
def add_course(request, id):
    developer = D.objects.get(id=id)
    if request.method == 'POST':
        course_name = request.POST['course_name']
        course_price = request.POST['course_price']
        course_description = request.POST['course_description']
        course_discount = request.POST['course_discount']
        course = Course.objects.create(name= course_name, discount = course_discount, price = course_price, description= course_description)
        return redirect('courses_list', developer.id)
    return render(request, 'developer/add_course.html', {'developer':developer})



@login_required
def delete_course(request, id , did):
    course = Course.objects.get(id = id)
    course.delete()
    return redirect('courses_list', did)



@login_required
def quiz_list(request, id):
    developer = D.objects.get(id=id)
    courses = Course.objects.all()
    return render(request, 'developer/quiz_list.html', {'developer':developer,'courses': courses})



@login_required
def quiz_creation_view(request, id):
    developer = D.objects.get(id=id)
    courses = Course.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        course_id = request.POST['course_id']
        print(course_id)
        course = Course.objects.get(id = int(course_id))
        questions = request.POST.getlist('question')
        print(questions)
        choices = request.POST.getlist('choice')
        correct_choices = request.POST.getlist('correct_choice')
        quiz = Quiz.objects.create(title=course.name, course = course)
        for i in range(0, len(questions)):
            question = Question.objects.create(quiz=quiz,question_number= int(i) , question=questions[i])

            for j in range(i*4, (i*4)+4):
                choice = Choice.objects.create(
                    question=question,
                    choice=choices[j],
                    is_correct=str(j) in correct_choices
                )
        return redirect('quiz_list', developer.id)
    return render(request, 'quiz/create_quiz.html', {'developer':developer,'courses': courses, 'q_range': range(1,21), 'c_range': range(1, 5)})



@login_required
def delete_quiz(request, id, did):
    quiz = Quiz.objects.get(id = id)
    quiz.delete()
    return redirect('quiz_list', did)


def developer_logout(request):
    logout(request)
    return redirect('developer_login')



def choices(request):
    course = Course.objects.get(name= 'HTML')
    quiz = Quiz.objects.get(course=course)
    questions = Question.objects.filter(quiz=quiz)
    list1 = []
    for i in range(len(questions)):
            question = questions[i]
            correct_choice = Choice.objects.get(question=question, is_correct=True)
            list1.append(correct_choice)
    return HttpResponse(f'{len(list1)}')

def query(request, id):
    learner = Learner.objects.get(id=id)
    if request.method == 'POST': 
        query = request.POST['query']
        topic = request.POST['topic']
        print(topic)
        Query.objects.create(learner = learner, query = query, topic = topic)
        message = 'your query is successfully submitted'
        sending_mail(message,'',learner.email)
        return render(request, 'query.html', {'learner':learner})
