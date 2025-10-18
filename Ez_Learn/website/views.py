from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import urllib.parse
from django.core.mail import send_mail
import math
import random
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .models import Learner,learnings, Course, Choice, Question, Quiz, Payment, Submission_quiz, Query
from .models import Developer as D
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import razorpay
from Ez_Learn.settings import KEY_ID, KEY_SECRET, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, razorpay_client, RAZORPAY_CURRENCY
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .forms import ImageForm, imageForm
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

#sending mail with improved error handling and configuration
def sending_mail(message, otp, email):
    """
    Enhanced email sending function with better error handling and configuration
    """
    from django.conf import settings
    from django.core.mail import send_mail
    from django.core.mail.backends.console import EmailBackend
    import smtplib
    
    try:
        # Prepare email content
        subject = "Ez-Learn Registration OTP"
        email_content = f"{message} {otp}" if otp else message
        
        # Always print OTP to console for development/debugging
        print(f"🔐 OTP for {email}: {otp}")
        print(f"📧 Attempting to send email to: {email}")
        
        # Check email configuration
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            print("⚠️ Email credentials not configured, using console fallback")
            print("💡 TO FIX: Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables")
            # Use console backend as fallback
            console_backend = EmailBackend()
            send_mail(
                subject=f"[CONSOLE] {subject}",
                message=email_content,
                from_email="console@ez-learn.com",
                recipient_list=[email],
                fail_silently=False,
                connection=console_backend
            )
            print(f"📋 Email sent to console (credentials not configured)")
            print(f"🔐 OTP for {email}: {otp}")
            return "console"  # Return status to indicate console fallback
        
        # Get sender email from settings
        sender_email = settings.EMAIL_HOST_USER
        
        try:
            # Send email using configured SMTP
            print(f"📤 Sending email via {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
            send_mail(
                subject=subject,
                message=email_content,
                from_email=sender_email,
                recipient_list=[email],
                fail_silently=False
            )
            print(f"✅ Email sent successfully to {email}")
            return True
            
        except smtplib.SMTPAuthenticationError as auth_error:
            print(f"❌ SMTP Authentication failed: {auth_error}")
            print("💡 Check your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
            print("   For Gmail, make sure to use an App Password, not your regular password")
            
        except smtplib.SMTPConnectError as conn_error:
            print(f"❌ SMTP Connection failed: {conn_error}")
            print(f"💡 Check if {settings.EMAIL_HOST}:{settings.EMAIL_PORT} is accessible")
            
        except Exception as smtp_error:
            print(f"❌ SMTP Error: {smtp_error}")
            print(f"💡 Error details: {type(smtp_error).__name__}")
        
        # Fallback to console if SMTP fails
        print("🔄 Falling back to console email...")
        try:
            console_backend = EmailBackend()
            send_mail(
                subject=f"[CONSOLE FALLBACK] {subject}",
                message=email_content,
                from_email="console@ez-learn.com",
                recipient_list=[email],
                fail_silently=False,
                connection=console_backend
            )
            print(f"📋 Email sent to console as fallback for {email}")
            return True
            
        except Exception as console_error:
            print(f"❌ Console fallback failed: {console_error}")
            return False
        
    except Exception as e:
        print(f"❌ Email sending failed completely: {str(e)}")
        print(f"🔐 OTP still available in console: {otp}")
        return False

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



# function for registering a learner (enhanced)
def register_learner(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '').strip()
        
        # Validation
        errors = []
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists. Please choose a different username.')
        
        # Check if email already exists
        if Learner.objects.filter(email=email).exists():
            errors.append('Email already registered. Please use a different email.')
        
        # Basic validation
        if len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        
        if not firstname or not lastname:
            errors.append('First name and last name are required.')
        
        if errors:
            context['errors'] = errors
            context['form_data'] = {
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'phone': phone
            }
        else:
            # Store in session for OTP verification
            request.session['registration_data'] = {
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'password': password,
                'phone': phone
            }
            request.session['otp'] = generateOTP()
            
            # Send OTP email
            message = 'Your OTP to complete the registration for Ez-Learn is:'
            email_status = sending_mail(message, request.session['otp'], email)
            
            if email_status == True:
                print(f"✅ OTP sent successfully to {email}: {request.session['otp']}")
                return redirect('otp')
            elif email_status == "console":
                print(f"⚠️ Email sent to console - credentials not configured")
                # Still proceed with registration but show helpful message
                context['info_messages'] = [
                    '📧 Email Configuration Notice:',
                    'OTP was sent to console instead of email because email credentials are not configured.',
                    '',
                    '🔧 TO RECEIVE ACTUAL EMAILS:',
                    '1. Set up Gmail App Password',
                    '2. Run: export EMAIL_HOST_USER=\"your-gmail@gmail.com\"',
                    '3. Run: export EMAIL_HOST_PASSWORD=\"your-app-password\"',
                    '4. Restart Django server',
                    '',
                    '💡 For now, check the console output for your OTP to complete registration.'
                ]
                # Still redirect to OTP page since console email was successful
                return redirect('otp')
            else:
                print(f"❌ Email sending failed for {email}")
                context['errors'] = [
                    'Unable to send OTP email. This could be due to:',
                    '• Email service not configured properly',
                    '• Network connectivity issues', 
                    '• Invalid email address',
                    '',
                    'For development/testing, check the console for the OTP.',
                    'The OTP has been logged for your convenience.'
                ]
                context['form_data'] = {
                    'username': username,
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                    'phone': phone
                }
    
    return render(request, 'learner_register.html', context)

#showing otp template
def otp_view(request):
    return render(request, 'otp.html')

#validating registered details (enhanced)
def valdate_lregistration(request):
    context = {}
    
    print(f"🔍 OTP Validation Debug - Method: {request.method}")
    print(f"🔍 Session data keys: {list(request.session.keys())}")
    
    # Check if registration data exists in session
    if 'registration_data' not in request.session or 'otp' not in request.session:
        print("❌ Missing session data for OTP validation")
        context['error_message'] = 'Registration session expired. Please register again.'
        return render(request, 'learner_register.html', context)
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        stored_otp = request.session.get('otp', '')
        
        print(f"🔍 Entered OTP: '{entered_otp}'")
        print(f"🔍 Stored OTP: '{stored_otp}'")
        print(f"🔍 OTP Match: {entered_otp == stored_otp}")
        
        if entered_otp == stored_otp:
            try:
                # Get registration data from session
                reg_data = request.session['registration_data']
                username = reg_data['username']
                firstname = reg_data['firstname']
                lastname = reg_data['lastname']
                email = reg_data['email']
                password = reg_data['password']
                phone = reg_data.get('phone', '')
                
                # Create User account
                user = User.objects.create_user(
                    username=username, 
                    password=password,
                    email=email,
                    first_name=firstname,
                    last_name=lastname
                )
                
                # Create Learner profile
                learner_ = Learner.objects.create(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    ph_number=phone,
                    user=user
                )
                
                # Create learning records for all courses
                courses = Course.objects.all()
                for course in courses:
                    learnings.objects.create(
                        learner=learner_,
                        course_learning=course,
                        activation=False
                    )
                
                # Clear session data
                del request.session['registration_data']
                del request.session['otp']
                
                print(f"✅ Learner registered successfully: {learner_.username}")
                return render(request, 'learner/successful.html', {'learner': learner_})
                
            except Exception as e:
                print(f"❌ Registration error: {e}")
                context['error_message'] = 'Registration failed. Please try again.'
                # Clean up any partially created objects
                try:
                    if 'user' in locals():
                        user.delete()
                except:
                    pass
        else:
            print("❌ OTP validation failed - incorrect OTP")
            context['error_message'] = 'Invalid OTP. Please check your email and try again.'
    
    return render(request, 'otp.html', context)


#complete profile
def complete_profile(request, id):
    try:
        learner = Learner.objects.get(id=id)
    except Learner.DoesNotExist:
        return render(request, 'learner_login.html', {'error': 'Learner not found'})
    
    if request.method == 'GET':
        try:
            print(f"🔍 Loading profile for learner: {learner}")
            form = imageForm()
            print(f"🔍 Form created: {form}")
            return render(request, 'personal.html', {'learner': learner, 'form': form})
        except Exception as e:
            print(f"❌ Error loading profile page: {e}")
            return render(request, 'learner_login.html', {'error': 'Error loading profile page'})
    
    if request.method == 'POST':
        try:
            form = imageForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.cleaned_data.get('profile_picture')
                print(f"🔍 Profile picture: {img}")
                
                # Update learner fields safely
                learner.dno = request.POST.get('house_no', '')
                learner.street = request.POST.get('street', '')
                learner.city = request.POST.get('city', '')
                learner.state = request.POST.get('state', '')
                learner.country = request.POST.get('country', '')
                learner.pincode = request.POST.get('pincode', '')
                learner.ph_number = request.POST.get('phone_no', learner.ph_number)
                
                # Handle date field safely
                dob_str = request.POST.get('dob', '')
                if dob_str:
                    learner.DOB = dob_str
                
                # Handle image safely
                if img:
                    learner.profile_picture = img
                
                learner.save()
                print(f"✅ Profile saved for learner: {learner.username}")
                
                # Automatically log in the user after profile completion
                if learner.user:
                    login(request, learner.user)
                    print(f"✅ User automatically logged in after profile completion")
                    return redirect('home', learner.id)
                else:
                    # Fallback if no user account found
                    print(f"❌ No user account found for learner")
                    return redirect('learner_login')
            else:
                print(f"❌ Form validation errors: {form.errors}")
                return render(request, 'personal.html', {
                    'learner': learner, 
                    'form': form,
                    'error': 'Please correct the errors below'
                })
        except Exception as e:
            print(f"❌ Error saving profile: {e}")
            return render(request, 'personal.html', {
                'learner': learner, 
                'form': imageForm(),
                'error': 'Error saving profile. Please try again.'
            })
        


#learner login function
@ensure_csrf_cookie
def learner_login(request):
    context = {}
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            
            if not username or not password:
                context['error'] = 'Please enter both username and password'
                return render(request, 'learner_login.html', context)
            
            u = authenticate(username=username, password=password)
            if u is not None:
                try:
                    learner = Learner.objects.get(user=u)
                    login(request, u)
                    return redirect('home', learner.id)
                except Learner.DoesNotExist:
                    context['error'] = 'User account not found'
            else:
                context['error'] = 'Invalid username or password'
        except Exception as e:
            print(f"❌ Login error: {e}")
            context['error'] = 'An error occurred during login. Please try again.'
    
    return render(request, 'learner_login.html', context)


# home page of learner
@login_required
def home(request, id):
    try:
        learner = Learner.objects.get(id=id)
    except Learner.DoesNotExist:
        print(f"❌ Learner not found: {id}")
        return redirect('learner_login')
    
    courses = Course.objects.all()
    
    # Get learner's learning progress
    learner_learnings = learnings.objects.filter(learner=learner)
    course_progress = {}
    
    for learning in learner_learnings:
        course_progress[learning.course_learning.name] = {
            'has_access': learning.activation,
            'course_id': learning.course_learning.id
        }
    
    # Get recent quiz scores
    recent_quizzes = Submission_quiz.objects.filter(Learner=learner).order_by('-id')[:5]
    
    # Calculate stats
    total_courses = courses.count()
    enrolled_courses = len([l for l in course_progress.values() if l['has_access'] or True])  # All courses have free access
    premium_courses = len([l for l in course_progress.values() if l['has_access']])
    
    return render(request, 'learner/home.html', {
        'learner': learner,
        'courses': courses,
        'course_progress': course_progress,
        'recent_quizzes': recent_quizzes,
        'total_courses': total_courses,
        'enrolled_courses': enrolled_courses,
        'premium_courses': premium_courses
    })

def highest_score(request, id):
    pass


#getting learners personal details
def learner_profile(request, id):
    try:
        learner = Learner.objects.get(id=id)
        
        # Get additional profile data
        from django.db.models import Count
        from .models import learnings, Submission_quiz
        
        # Get course stats
        total_courses = Course.objects.count()
        enrolled_courses = learnings.objects.filter(learner=learner, activation=True).count()
        
        # Get quiz stats
        quiz_submissions = Submission_quiz.objects.filter(Learner=learner)
        total_quizzes_taken = quiz_submissions.count()
        latest_score = quiz_submissions.order_by('-id').first()
        latest_score_value = latest_score.score if latest_score else 0
        
        # Get recent activity
        recent_quizzes = quiz_submissions.order_by('-id')[:5]
        
        context = {
            'learner': learner,
            'total_courses': total_courses,
            'enrolled_courses': enrolled_courses,
            'total_quizzes_taken': total_quizzes_taken,
            'latest_score': latest_score_value,
            'recent_quizzes': recent_quizzes,
        }
        
        return render(request, 'learner/profile.html', context)
        
    except Learner.DoesNotExist:
        return render(request, 'learner/profile.html', {'error': 'Learner not found'})
    except Exception as e:
        print(f"❌ Error loading learner profile: {e}")
        return render(request, 'learner/profile.html', {'error': 'Error loading profile'})


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
                    return render(request, 'payment/bying_course.html', {
                        'learnt': learning, 
                        'learner': learner,
                        'course': course,
                        'message': 'Please purchase the course to access intermediate content.'
                    })
            if request.POST.get('advanced') == 'advanced':
                if has_full_access:
                    return render(request, 'courses/python/advanced.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {
                        'learnt': learning,
                        'learner': learner,
                        'course': course, 
                        'message': 'Please purchase the course to access advanced content.'
                    })
        return render(request, 'courses/python/open.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access, 'learning': learning})
    elif course.name == 'HTML':
        if request.method == 'POST':
            if request.POST.get('basics') == 'basics':
                return render(request, 'courses/html/basics.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
            if request.POST.get('intermediate') == 'intermediate':
                if has_full_access:
                    return render(request, 'courses/html/intermediate.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {
                        'learnt': learning,
                        'learner': learner,
                        'course': course,
                        'message': 'Please purchase the course to access intermediate content.'
                    })
            if request.POST.get('advanced') == 'advanced':
                if has_full_access:
                    return render(request, 'courses/html/advanced.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {
                        'learnt': learning,
                        'learner': learner,
                        'course': course,
                        'message': 'Please purchase the course to access advanced content.'
                    })
        return render(request, 'courses/html/open.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access, 'learning': learning})
    elif course.name == 'CSS':
        if request.method == 'POST':
            if request.POST.get('basics') == 'basics':
                return render(request, 'courses/css/basics.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
            if request.POST.get('intermediate') == 'intermediate':
                if has_full_access:
                    return render(request, 'courses/css/intermediate.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {
                        'learnt': learning,
                        'learner': learner,
                        'course': course,
                        'message': 'Please purchase the course to access intermediate content.'
                    })
            if request.POST.get('advanced') == 'advanced':
                if has_full_access:
                    return render(request, 'courses/css/advanced.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access})
                else:
                    return render(request, 'payment/bying_course.html', {
                        'learnt': learning,
                        'learner': learner,
                        'course': course,
                        'message': 'Please purchase the course to access advanced content.'
                    })
        return render(request, 'courses/css/open.html', {'learner': learner, 'course': course, 'has_full_access': has_full_access, 'learning': learning})




#getting quizes layed by the particular persona
def get_into_quiz(request, title, id):
    try:
        learner = Learner.objects.get(id=id)
        course = Course.objects.get(name=title)
        
        # Check if quiz exists for this course
        try:
            quiz = Quiz.objects.get(course=course)
        except Quiz.DoesNotExist:
            # No quiz exists for this course yet
            return render(request, 'quiz/no_quiz.html', {
                'learner': learner, 
                'course': course,
                'message': 'No quiz available for this course yet. Please check back later.'
            })
        
        # Get submissions if any
        submissions = Submission_quiz.objects.filter(Learner=learner, Quiz=quiz).order_by('-id')
        # Get total questions for proper score display
        total_questions = Question.objects.filter(quiz=quiz).count()
        # Get best score
        best_score = max([sub.score for sub in submissions]) if submissions else 0
        
        return render(request, 'quiz/quizs_played.html', {
            'learner': learner, 
            'course': course, 
            'submissions': submissions,
            'quiz': quiz,
            'total_questions': total_questions,
            'best_score': best_score
        })
    except Learner.DoesNotExist:
        return redirect('learner_login')
    except Course.DoesNotExist:
        return render(request, 'quiz/no_quiz.html', {
            'learner': learner,
            'course': None,
            'message': 'Course not found.'
        })


@login_required
def take_quiz_view(request, title, id):
    try:
        learner = Learner.objects.get(id=id)
        course = Course.objects.get(name=title)
        quiz = Quiz.objects.get(course=course)
        questions = Question.objects.filter(quiz=quiz).order_by('question_number')
        
        if not questions.exists():
            return render(request, 'quiz/no_quiz.html', {
                'learner': learner,
                'course': course,
                'message': 'No questions available for this quiz yet.'
            })

        if request.method == 'POST':
            submitted_answers = [request.POST.get(str(question.id)) for question in questions]
            score = 0
            results = []
            total_questions = len(questions)
            
            for i, question in enumerate(questions):
                try:
                    correct_choice = Choice.objects.get(question=question, is_correct=True)
                    submitted_answer_id = submitted_answers[i]
                    
                    # Check if answer is correct
                    if submitted_answer_id and submitted_answer_id == str(correct_choice.id):
                        score += 1
                    
                    # Get submitted choice text if provided
                    if submitted_answer_id:
                        try:
                            submitted_choice = Choice.objects.get(id=submitted_answer_id)
                            submitted_text = submitted_choice.choice
                        except Choice.DoesNotExist:
                            submitted_text = 'Invalid choice selected'
                    else:
                        submitted_text = 'Not answered'
                    
                    # Get all choices for this question
                    choices = Choice.objects.filter(question=question)
                    
                    result = {
                        'question_number': question.question_number,
                        'question_text': question.question,
                        'submitted_answer': submitted_text,
                        'correct_answer': correct_choice.choice,
                        'is_correct': submitted_answer_id == str(correct_choice.id) if submitted_answer_id else False,
                        'choices': choices
                    }
                    results.append(result)
                    
                except Choice.DoesNotExist:
                    # Handle case where no correct choice exists
                    result = {
                        'question_number': question.question_number,
                        'question_text': question.question,
                        'submitted_answer': 'Not answered',
                        'correct_answer': 'No correct answer set',
                        'is_correct': False,
                        'choices': []
                    }
                    results.append(result)

            # Calculate percentage first
            percentage = (score / total_questions * 100) if total_questions > 0 else 0
            
            # Save submission with percentage score (rounded to integer)
            submission = Submission_quiz.objects.create(Learner=learner, Quiz=quiz, score=int(round(percentage)))
            
            context = {
                'quiz': quiz, 
                'questions': questions, 
                'results': results, 
                'score': score,  # Raw score (number of correct answers)
                'total_questions': total_questions,
                'percentage': percentage,  # Calculated percentage
                'learner': learner,
                'course': course,
                'submission': submission
            }
            return render(request, 'quiz/result.html', context)

        return render(request, 'quiz/take_quiz.html', {
            'quiz': quiz, 
            'questions': questions, 
            'course': course, 
            'learner': learner
        })
        
    except Learner.DoesNotExist:
        return redirect('learner_login')
    except Course.DoesNotExist:
        return redirect('home', id)
    except Quiz.DoesNotExist:
        return render(request, 'quiz/no_quiz.html', {
            'learner': learner,
            'course': course,
            'message': 'Quiz not found for this course.'
        })

def get_certificate(request, id, cid):
    try:
        learner = Learner.objects.get(id=id)
        course = Course.objects.get(id=cid)
        
        # Get all quizzes for this course
        quizzes = Quiz.objects.filter(course=course)
        if not quizzes.exists():
            error = f"No quizzes found for {course.name} course"
            return render(request, 'quiz/no_quiz_taken.html', {
                'error': error, 
                'learner': learner, 
                'course': course
            })
        
        # Calculate the best score across all quizzes for this course
        best_score = 0
        for quiz in quizzes:
            try:
                submissions = Submission_quiz.objects.filter(Learner=learner, Quiz=quiz)
                if submissions.exists():
                    quiz_best_score = max([submission.score for submission in submissions])
                    best_score = max(best_score, quiz_best_score)
            except Exception as e:
                print(f"Error processing quiz {quiz.id}: {e}")
                continue
        
        # Check if learner meets certificate requirements
        # Changed from 15 to 60% to be more reasonable
        required_score = 60  # 60% minimum score
        
        if best_score >= required_score:
            try:
                if pisa is not None:
                    template_path = 'certificate.html'
                    context = {
                        'learner': learner,
                        'course': course,
                        'score': best_score,
                        'completion_date': timezone.now().date()
                    }
                    
                    response = HttpResponse(content_type='application/pdf')
                    filename = f"{learner.username}_{course.name}_Certificate.pdf"
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    
                    template = get_template(template_path)
                    html = template.render(context)
                    
                    # Create PDF
                    pisa_status = pisa.CreatePDF(html, dest=response)
                    if pisa_status.err:
                        return HttpResponse('Error generating PDF. Please try again later.')
                    
                    return response
                else:
                    # Fallback when xhtml2pdf is not available - show certificate page
                    context = {
                        'learner': learner,
                        'course': course,
                        'score': best_score,
                        'completion_date': timezone.now().date()
                    }
                    return render(request, 'certificate_display.html', context)
            except Exception as e:
                print(f"Error generating certificate: {e}")
                return render(request, 'quiz/no_quiz_taken.html', {
                    'error': f'Error generating certificate: {str(e)}', 
                    'learner': learner, 
                    'course': course
                })
        else:
            error = f'Your best score in {course.name} is {best_score}%. You need a minimum score of {required_score}% to earn a certificate.'
            return render(request, 'quiz/no_quiz_taken.html', {
                'error': error, 
                'learner': learner, 
                'course': course, 
                'score': best_score
            })
            
    except Learner.DoesNotExist:
        return render(request, 'quiz/no_quiz_taken.html', {
            'error': 'Learner not found', 
            'learner': None, 
            'course': None
        })
    except Course.DoesNotExist:
        return render(request, 'quiz/no_quiz_taken.html', {
            'error': 'Course not found', 
            'learner': None, 
            'course': None
        })
    except Exception as e:
        print(f"Unexpected error in get_certificate: {e}")
        return render(request, 'quiz/no_quiz_taken.html', {
            'error': f'An unexpected error occurred: {str(e)}', 
            'learner': None, 
            'course': None
        })
    

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
    try:
        learnt = learnings.objects.get(id=id)
        course = learnt.course_learning
        learner = learnt.learner
        
        # Get message from URL parameters or context
        message = request.GET.get('message', '')
        
        if request.method == 'POST':
            # Calculate amount in paise (Razorpay expects amount in smallest currency unit)
            amount_in_paise = int(course.price) * 100
            
            # Use the global razorpay_client if available
            if razorpay_client and RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
                try:
                    # Create Razorpay order with proper metadata
                    order = razorpay_client.order.create({
                        'amount': amount_in_paise, 
                        'currency': RAZORPAY_CURRENCY,
                        'receipt': f'course_{course.id}_{learner.id}_{learnt.id}',
                        'notes': {
                            'course': course.name,
                            'learner': learner.username,
                            'learning_id': learnt.id
                        }
                    })
                    print(f"✅ Razorpay order created: {order['id']}")
                except Exception as e:
                    print(f"❌ Razorpay order creation failed: {e}")
                    # Fallback for Razorpay errors
                    order = {'id': f'error_order_{learner.id}_{course.id}_{random.randint(1000, 9999)}'}
            elif KEY_ID and KEY_SECRET:
                # Fallback to direct client creation
                try:
                    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
                    order = client.order.create({
                        'amount': amount_in_paise, 
                        'currency': RAZORPAY_CURRENCY,
                        'receipt': f'course_{course.id}_{learner.id}_{learnt.id}'
                    })
                    print(f"✅ Razorpay order created (fallback): {order['id']}")
                except Exception as e:
                    print(f"❌ Razorpay client creation failed: {e}")
                    order = {'id': f'fallback_order_{learner.id}_{course.id}_{random.randint(1000, 9999)}'}
            else:
                # Development mode when Razorpay keys are not set
                order = {'id': f'dev_order_{learner.id}_{course.id}_{learnt.id}_{random.randint(1000, 9999)}'}
                print(f"🔧 Development order created: {order['id']}")
            
            # Create payment record
            payment = Payment.objects.create(
                order_id=order['id'], 
                course=course, 
                learner=learner
            )
            
            return redirect('confirm_payment', payment.id, learner.id)
            
        return render(request, 'payment/bying_course.html', {
            'learnt': learnt,
            'learner': learner,
            'course': course,
            'message': message
        })
    except learnings.DoesNotExist:
        return redirect('home', 1)  # Redirect to a default page or handle error

#confirming payment
def confirm_payment(request, id, lid):
    try:
        payment = Payment.objects.get(id=id)
        learner = Learner.objects.get(id=lid)
        
        # Additional context for better user experience
        context = {
            'payment': payment,
            'learner': learner,
            'course': payment.course,
            'order_age': payment.id,  # Could be used for time-based logic
            'razorpay_key': RAZORPAY_KEY_ID or KEY_ID,  # Pass Razorpay key to template
            'razorpay_configured': bool(RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET)
        }
        
        return render(request, 'payment/confirm_payment.html', context)
        
    except Payment.DoesNotExist:
        return render(request, 'payment/confirm_payment.html', {
            'error': 'Payment not found',
            'learner_id': lid
        })
    except Learner.DoesNotExist:
        return render(request, 'payment/confirm_payment.html', {
            'error': 'Learner not found',
            'payment_id': id
        })


#verifying payment
@csrf_exempt
def verify(request):
    if request.method == 'POST':
        try:
            data = request.POST
            print(f"Payment verification data: {data}")
            
            # Get payment details from Razorpay
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            
            if not all([razorpay_order_id, razorpay_payment_id]):
                print("❌ Missing payment details")
                return HttpResponse("Missing payment details", status=400)
            
            # Get payment record
            try:
                payment = Payment.objects.get(order_id=razorpay_order_id)
            except Payment.DoesNotExist:
                print(f"❌ Payment not found for order: {razorpay_order_id}")
                return HttpResponse("Payment not found", status=404)
            
            # Verify signature if Razorpay keys are configured
            signature_verified = False
            if razorpay_client and razorpay_signature:
                try:
                    # Create signature verification string
                    body = razorpay_order_id + "|" + razorpay_payment_id
                    
                    # Import hmac and hashlib for signature verification
                    import hmac
                    import hashlib
                    
                    # Generate expected signature
                    expected_signature = hmac.new(
                        RAZORPAY_KEY_SECRET.encode('utf-8'),
                        body.encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()
                    
                    # Verify signature
                    signature_verified = hmac.compare_digest(expected_signature, razorpay_signature)
                    
                    if signature_verified:
                        print(f"✅ Signature verified for order: {razorpay_order_id}")
                    else:
                        print(f"❌ Signature verification failed for order: {razorpay_order_id}")
                        
                except Exception as e:
                    print(f"⚠️ Signature verification error: {e}")
            
            # For development orders, skip signature verification
            if (razorpay_order_id.startswith('dev_order') or 
                razorpay_order_id.startswith('error_order') or 
                razorpay_order_id.startswith('fallback_order')):
                signature_verified = True
                print(f"🔧 Development order - skipping signature verification: {razorpay_order_id}")
            
            # Update payment record
            payment.payment_id = razorpay_payment_id
            payment.status = True
            payment.save()
            print(f"✅ Payment updated: {payment.order_id}")
            
            # Activate course access for learner
            try:
                learnt_list = learnings.objects.filter(
                    course_learning=payment.course, 
                    learner=payment.learner
                )
                if learnt_list.exists():
                    learnt = learnt_list[0]
                    learnt.activation = True
                    learnt.save()
                    print(f"✅ Course access activated for {payment.learner.username}: {payment.course.name}")
                else:
                    print(f"⚠️ No learning record found for payment: {payment.order_id}")
            except Exception as e:
                print(f"❌ Error activating course access: {e}")
            
            # Redirect to home page
            return redirect('home', payment.learner.id)
            
        except Exception as e:
            print(f"❌ Payment verification error: {e}")
            return HttpResponse(f"Payment verification failed: {e}", status=500)
    
    return HttpResponse("Method not allowed", status=405)

# developer registration
def register_developer(request):
    context = {}
    if request.method == 'POST':
        developer_name = request.POST.get('developer_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Validation
        errors = []
        
        # Check if username already exists
        if User.objects.filter(username=developer_name).exists():
            errors.append('Developer name already exists. Please choose a different name.')
        
        # Check if email already exists
        if D.objects.filter(email=email).exists():
            errors.append('Email already registered. Please use a different email.')
        
        # Basic validation
        if len(developer_name) < 3:
            errors.append('Developer name must be at least 3 characters long.')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        
        if errors:
            context['errors'] = errors
            context['form_data'] = {
                'developer_name': developer_name,
                'email': email
            }
        else:
            # Store in session for OTP verification
            request.session['developer_registration_data'] = {
                'developer_name': developer_name,
                'email': email,
                'password': password
            }
            request.session['otp'] = generateOTP()
            
            # Send OTP email
            message = 'Your OTP to complete the developer registration for Ez-Learn is:'
            email_sent = sending_mail(message, request.session['otp'], email)
            
            if email_sent:
                print(f"✅ Developer OTP sent to {email}: {request.session['otp']}")
                return redirect('dotp')
            else:
                print(f"❌ Developer email sending failed for {email}")
                context['errors'] = [
                    'Unable to send OTP email. This could be due to:',
                    '• Email service not configured properly',
                    '• Network connectivity issues', 
                    '• Invalid email address',
                    '',
                    'For development/testing, check the console for the OTP.',
                    'The OTP has been logged for your convenience.'
                ]
                context['form_data'] = {
                    'developer_name': developer_name,
                    'email': email
                }
    
    return render(request, 'developer_register.html', context)



def developer_otp_view(request):
    return render(request, 'developer_otp.html')



def valdate_dregistration(request):
    context = {}
    
    # Check if registration data exists in session
    if 'developer_registration_data' not in request.session or 'otp' not in request.session:
        context['error_message'] = 'Registration session expired. Please register again.'
        return render(request, 'developer_register.html', context)
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        
        if entered_otp == request.session['otp']:
            try:
                # Get registration data from session
                reg_data = request.session['developer_registration_data']
                developer_name = reg_data['developer_name']
                email = reg_data['email']
                password = reg_data['password']
                
                # Create User account
                user = User.objects.create_user(
                    username=developer_name,
                    password=password,
                    email=email
                )
                
                # Add to developer group
                try:
                    developer_group = Group.objects.get(name='developer')
                    user.groups.add(developer_group)
                except Group.DoesNotExist:
                    # Create developer group if it doesn't exist
                    developer_group = Group.objects.create(name='developer')
                    user.groups.add(developer_group)
                
                # Create Developer profile
                developer = D.objects.create(
                    user=user,
                    developer_name=developer_name,
                    email=email
                )
                
                # Clear session data
                del request.session['developer_registration_data']
                del request.session['otp']
                
                print(f"✅ Developer registered successfully: {developer.developer_name}")
                return render(request, 'developer/successful.html', {'developer': developer})
                
            except Exception as e:
                print(f"❌ Developer registration error: {e}")
                context['error_message'] = 'Registration failed. Please try again.'
                # Clean up any partially created objects
                try:
                    if 'user' in locals():
                        user.delete()
                except:
                    pass
        else:
            context['error_message'] = 'Invalid OTP. Please check your email and try again.'
    
    return render(request, 'developer_otp.html', context)

#developer login
@ensure_csrf_cookie
def developer_login(request):
    context = {}
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            
            if not username or not password:
                context['error'] = 'Please enter both username and password'
                return render(request, 'developer_login.html', context)
            
            u = authenticate(username=username, password=password)
            if u is not None:
                try:
                    developer = D.objects.get(user=u)
                    login(request, u)
                    return redirect('developer_home', developer.id)
                except D.DoesNotExist:
                    context['error'] = 'Developer account not found'
            else:
                context['error'] = 'Invalid username or password'
        except Exception as e:
            print(f"❌ Developer login error: {e}")
            context['error'] = 'An error occurred during login. Please try again.'
    
    return render(request, 'developer_login.html', context)


#@permission_required('school.change_student', login_url='login')
@login_required
def developer_home(request, id):
    try:
        developer = D.objects.get(id=id)
        return render(request, 'developer/dhome.html', {'developer': developer})
    except D.DoesNotExist:
        print(f"❌ Developer not found: {id}")
        return redirect('developer_login')
    except Exception as e:
        print(f"❌ Error in developer_home: {e}")
        return redirect('developer_login')



@login_required
def learners_list(request, id):
    try:
        developer = D.objects.get(id=id)
        Learners = Learner.objects.all()
        return render(request, 'developer/learners_list.html', {'developer':developer,'learners' : Learners})
    except D.DoesNotExist:
        print(f"❌ Developer not found: {id}")
        return redirect('developer_login')
    except Exception as e:
        print(f"❌ Error in learners_list: {e}")
        return redirect('developer_login')



@login_required
def courses_list(request, id):
    try:
        developer = D.objects.get(id=id)
        courses = Course.objects.all()
        return render(request, 'developer/courses_list.html', {'developer': developer,'courses': courses})
    except D.DoesNotExist:
        print(f"❌ Developer not found: {id}")
        return redirect('developer_login')
    except Exception as e:
        print(f"❌ Error in courses_list: {e}")
        return redirect('developer_login')



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
def edit_course(request, course_id, did):
    developer = D.objects.get(id=did)
    course = Course.objects.get(id=course_id)
    
    if request.method == 'POST':
        try:
            course.name = request.POST.get('course_name', course.name)
            course.price = request.POST.get('course_price', course.price)
            course.description = request.POST.get('course_description', course.description)
            course.discount = request.POST.get('course_discount', course.discount)
            course.save()
            print(f"✅ Course updated: {course.name}")
            return redirect('courses_list', developer.id)
        except Exception as e:
            print(f"❌ Error updating course: {e}")
            return render(request, 'developer/edit_course.html', {
                'developer': developer, 
                'course': course,
                'error': 'Error updating course. Please try again.'
            })
    
    return render(request, 'developer/edit_course.html', {'developer': developer, 'course': course})


@login_required
def manage_course_content(request, course_id, did):
    developer = D.objects.get(id=did)
    course = Course.objects.get(id=course_id)
    
    # This view will handle course content management
    # For now, we'll provide a basic structure
    # You can extend this to manage actual content files/templates
    
    if request.method == 'POST':
        # Handle content updates here
        print(f"Content management for course: {course.name}")
        # This could be extended to save content to files or database
        return redirect('courses_list', developer.id)
    
    return render(request, 'developer/manage_course_content.html', {
        'developer': developer, 
        'course': course
    })


@login_required
def delete_course(request, id , did):
    course = Course.objects.get(id = id)
    course.delete()
    return redirect('courses_list', did)



@login_required
def quiz_list(request, id):
    developer = D.objects.get(id=id)
    courses = Course.objects.all()
    quizzes = Quiz.objects.all()
    return render(request, 'developer/quiz_list.html', {
        'developer': developer,
        'courses': courses,
        'quizzes': quizzes
    })



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


# Force reload to fix caching issues - edit_quiz function
@login_required
def edit_quiz(request, quiz_id, did):
    """
    Edit quiz view for developers to modify existing quizzes
    Updated to fix server reload issues and caching problems
    """
    try:
        developer = D.objects.get(id=did)
    except D.DoesNotExist:
        print(f"❌ Developer not found: {did}")
        return redirect('developer_login')
    
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz).order_by('question_number')
        courses = Course.objects.all()
        
        if request.method == 'POST':
            # Handle quiz title update
            new_title = request.POST.get('quiz_title', quiz.title)
            course_id = request.POST.get('course_id', quiz.course.id)
            
            quiz.title = new_title
            quiz.course = Course.objects.get(id=course_id)
            quiz.save()
            
            print(f"✅ Quiz updated: {quiz.title}")
            return redirect('quiz_list', developer.id)
        
        # Get questions and choices for display
        quiz_data = []
        for question in questions:
            choices = Choice.objects.filter(question=question)
            quiz_data.append({
                'question': question,
                'choices': choices
            })
        
        return render(request, 'developer/edit_quiz.html', {
            'developer': developer,
            'quiz': quiz,
            'questions_data': quiz_data,
            'courses': courses
        })
        
    except Quiz.DoesNotExist:
        print(f"❌ Quiz not found: {quiz_id}")
        return redirect('quiz_list', developer.id)
    except Exception as e:
        print(f"❌ Error editing quiz: {e}")
        return redirect('quiz_list', developer.id)


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
    try:
        learner = Learner.objects.get(id=id)
    except Learner.DoesNotExist:
        return render(request, 'query.html', {'error': 'Learner not found'})
    
    success_message = None
    
    if request.method == 'POST': 
        query_text = request.POST.get('query', '').strip()
        topic = request.POST.get('topic', '').strip()
        
        if query_text and topic:
            # Create query record
            Query.objects.create(learner=learner, query=query_text, topic=topic)
            success_message = 'Your query has been successfully submitted!'
            
            # Send confirmation email to learner
            confirmation_message = f'Thank you for contacting Ez-Learn support. Your query regarding "{topic}" has been received and will be addressed shortly.'
            sending_mail(confirmation_message, '', learner.email)
            
            # Send support notification to admin email (configured email)
            from django.conf import settings
            admin_email = getattr(settings, 'EMAIL_HOST_USER', 'jayanthyadav237@gmail.com')
            
            # Create support notification email
            support_subject = f"[Ez-Learn Support] New Query: {topic}"
            support_message = f"""
New Support Query Received:

From: {learner.username} ({learner.email})
Topic: {topic}
Query: {query_text}

Please respond to this query through the admin panel or contact the user directly.

Learner Details:
- Name: {learner.first_name} {learner.last_name}
- Username: {learner.username}
- Email: {learner.email}
- Phone: {getattr(learner, 'ph_number', 'Not provided')}

Query ID: {Query.objects.filter(learner=learner).latest('id').id if Query.objects.filter(learner=learner).exists() else 'N/A'}
"""
            
            # Send to configured email address
            try:
                from django.core.mail import send_mail
                send_mail(
                    subject=support_subject,
                    message=support_message,
                    from_email=admin_email,
                    recipient_list=[admin_email],
                    fail_silently=False
                )
                print(f"✅ Support query notification sent to admin: {admin_email}")
            except Exception as e:
                print(f"❌ Failed to send support notification: {e}")
            
            return render(request, 'query.html', {'learner': learner, 'success_message': success_message, 'admin_email': admin_email})
    
    # Handle GET request and any errors
    from django.conf import settings
    admin_email = getattr(settings, 'EMAIL_HOST_USER', 'jayanthyadav237@gmail.com')
    return render(request, 'query.html', {'learner': learner, 'error': None, 'admin_email': admin_email})
