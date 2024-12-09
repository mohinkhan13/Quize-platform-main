from django.db import models
from django.utils import timezone  # Import timezone for time-related fields
import datetime
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
import os
from django.conf import settings

# Custom User Model
class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128, default="")
    email = models.EmailField(unique=True)  # Add unique constraint to email
    mobile = models.PositiveBigIntegerField()
    profile = models.ImageField(upload_to='profile_pictures/',default="")
    address = models.TextField(default="")
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100,default="")
    country = models.CharField(max_length=100,default="")
    is_login = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)  # Use timezone.now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Optimize the image before saving if it exists
        if self.profile:
            try:
                # Open the image using PIL
                img = PILImage.open(self.profile)
                img = img.convert('RGB')  # Convert image to RGB format
                img.thumbnail((800, 800), PILImage.LANCZOS)  # Resize image to fit within 800x800

                # Ensure the media directory exists
                media_directory = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
                os.makedirs(media_directory, exist_ok=True)

                # Define the path to save the optimized image
                optimized_image_path = os.path.join(media_directory, os.path.basename(self.profile.name))

                # Save the optimized image
                img.save(optimized_image_path, format='JPEG', quality=85)

                # Update the profile field with the optimized image path
                self.profile.name = os.path.basename(optimized_image_path)  # Set the file name for the ImageField
                self.profile = optimized_image_path  # Assign the optimized image to the profile field

            except FileNotFoundError:
                # Handle the case where the original image might not be found
                raise ValidationError("The original image file was not found.")
            except Exception as e:
                # Handle other exceptions
                raise ValidationError(f"An error occurred while processing the image: {str(e)}")

        # Handle last login time
        if self.is_login:
            self.last_login = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name


# Exam Model
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Questions'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
        ('MX', 'Mix'),
    ]
    TIME_SETTING_CHOICES = [
        ('exam', 'Full Exam Time'),
        ('question', 'Single Question Time'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    exam_subject = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=80, choices=EXAM_TYPE_CHOICES)
    number_of_questions = models.IntegerField(default=0)
    time_setting = models.CharField(max_length=50, choices=TIME_SETTING_CHOICES)
    exam_time = models.TimeField(default=datetime.time(0, 0))
    visibility = models.CharField(max_length=50,choices=VISIBILITY_CHOICES,default="private")
    question_created = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=100,choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],default="Easy")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam_name

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    attempted = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class MCQQuestion(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)    

    def __str__(self):
        return self.question
    
class TrueFalseQuestion(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    correct_answer = models.BooleanField()    

    def __str__(self):
        return self.question
    
class ShortAnswerQuestion(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return self.question
    
class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answers = models.JSONField()  # Store user answers
    score = models.IntegerField(default=0)  # Store the score or result
    date_taken = models.DateTimeField(auto_now_add=True)
    attempt_no = models.IntegerField(default=0)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def percentage(self):
        total_questions = len(self.answers)  # Assuming answers is a list of answers
        if total_questions > 0:
            return (self.score / total_questions) * 100
        return 0

    def __str__(self):
        return f"Result for {self.exam.exam_name} by {self.user.username}"