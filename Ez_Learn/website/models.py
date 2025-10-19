from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Learner(models.Model):
        username = models.CharField(max_length=50)
        first_name = models.CharField(max_length=50, default='')
        last_name = models.CharField(max_length=50, default='')
        profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
        email = models.EmailField()
        ph_number = models.CharField(max_length=15, blank=True, null=True)
        DOB = models.DateField( null = True, default='2001-01-01')
        user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
        dno = models.CharField(max_length=100, null=True, blank=True, default='--')
        street = models.CharField(max_length=100, null=True, blank=True, default='--')
        city = models.CharField(max_length=100, null=True, blank=True, default='--')
        state = models.CharField(max_length=100, null=True, blank=True, default='--')
        country = models.CharField(max_length=100, null=True, blank=True, default='--')
        pincode = models.CharField(max_length=100, null=True, blank=True, default='--')
        
        def __str__(self):
                return f'{self.username}'
        
class Developer(models.Model):
        developer_name = models.CharField(max_length=50)
        email = models.EmailField()
        user = models.OneToOneField(User, on_delete=models.CASCADE , default=None)

        def __str__(self):
                return f'{self.developer_name}'
        

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField( null=True, blank=True)

    def __str__(self):
         return f'{self.name}'


class learnings(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, default=None)
    course_learning = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    activation = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
          return f'{self.learner}'


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice
    
class Submission_quiz(models.Model):
    Learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    Quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE )
    score = models.IntegerField(blank=True, null=True, default = 0)

    def __str__(self):
        return f"{self.Learner.username if self.Learner else 'No Learner'} - {self.Quiz.title if self.Quiz else 'No Quiz'}"
     
    
class Payment(models.Model):
    order_id = models.CharField(max_length=300, null=True, blank= True)
    payment_id = models.CharField(max_length=300, null=True, blank=True)
    status = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)


    def __str__(self):
         return self.order_id or f"Payment for {self.learner.username if self.learner else 'Unknown'}"



class Query(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, null=True, blank=True)
    query = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
         return self.query or f"Query from {self.learner.username if self.learner else 'Unknown User'}"

