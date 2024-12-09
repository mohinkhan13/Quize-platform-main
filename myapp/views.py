from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseBadRequest,JsonResponse
from django.core.paginator import Paginator
import json

def login_required(view_func, login_url='login.html', message=None):
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')  
        if not user_id or not CustomUser.objects.filter(id=user_id, is_login=True).exists():
            return render(request, login_url, {
                'error': "You must be logged in to Access All Pages.",
                'next': request.path
            })
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

# Create your views here.
def index(request):
    try:
        user = CustomUser.objects.get(id=request.session['user_id'])        
        return render(request, 'index.html',{'user':user})
    except:
        return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the email or username already exists
        try:
            user = CustomUser.objects.get(email=email)
            error = "Email already exists"
            return render(request, 'register.html', {'error': error})
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(username=username)
                error = "Username already exists"
                return render(request, 'register.html', {'error': error})
            except CustomUser.DoesNotExist:
                # If both email and username do not exist, continue with registration
                if password == confirm_password:
                    hashed_password = make_password(password)
                    
                    # Create the new user
                    CustomUser.objects.create(
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        username=username,
                        email=email,
                        mobile=request.POST['mobile'],
                        password=hashed_password,
                        profile=request.FILES['profile']
                    )
                    msg = "Registration Successful! Please login."
                    return render(request, 'login.html', {'msg': msg})
                else:
                    error = "Password and confirm password do not match"
                    return render(request, 'register.html', {'error': error})

    return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)

            if check_password(password, user.password):
                user.is_login = True
                user.save()
                request.session['user_id'] = user.id 
                request.session['profile'] = user.profile.url
                exams_count = Exam.objects.filter(user=user).count()
                request.session['exams_count'] = exams_count
                return render(request, 'index.html')
            else:
                error = "Invalid Password"
                return render(request, 'login.html', {'error' : error} )
        except CustomUser.DoesNotExist:
            error = "Email not registered"
            return render(request, 'login.html', {'error' :error } )
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'login.html', context)

def logout(request):

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = CustomUser.objects.get(id=user_id)
            # Set the is_login attribute to False if you are using it
            user.is_login = False            
            user.save()  # Save the user status if needed
            del request.session['user_id']
            del request.session['profile']
        except CustomUser.DoesNotExist:
            pass  # Handle the case if the user is not found    
    return redirect('login')  # Redirect to the login page
    
def setting(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])

            context = {        
                'user':user,
            }
            return render(request, 'setting.html', context)
        except:
            error = "You Need To login First"
            return render(request, 'login.html', {'error':error})
    
def profile(request):
    if request.method == 'POST':        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        country = request.POST['country']
        city = request.POST['city']
        address = request.POST['address']
        dob = request.POST['dob']
        profile = request.FILES.get('profile')
        print(profile)
        user = CustomUser.objects.get(id=request.session['user_id'])

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.mobile = mobile
        user.country = country
        user.city = city
        user.address = address
        user.dob = dob
        try:
            user.profile = profile
        except:
            pass
        user.save()
        request.session['profile'] = user.profile.url
        return redirect('profile')

    else:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])

            context = {        
                'user':user,
            }
            return render(request, 'profile.html', context)
        except:
            error = "You Need To login First"
            return render(request, 'login.html', {'error':error})
    
def change_password(request):
    if request.method == 'POST':
        # POST request handling logic
        user = CustomUser.objects.get(id=request.session['user_id'])
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if check_password(old_password, user.password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                logout(request)
                msg = "Password Changed Successfully. Please login again."
                return render(request, 'login.html', {'msg': msg})            
            else:
                error = "Password and confirm password do not match"
                return render(request, 'change_password.html', {'error': error})
        else:
            error = "Invalid Old Password"
            return render(request, 'change_password.html', {'error': error})
    else:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])

            context = {        
                'user':user,
            }
            return render(request, 'change_password.html', context)
        except:
            error = "You Need To login First"
            return render(request, 'login.html', {'error':error})
    
def forgot_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        # Check if user is logged in based on session
        user_id = request.session.get('user_id')
        if user_id:
            try:
                CustomUser.objects.get(id=user_id)  # Check if user exists
                logout(request)
                return redirect('forgot-password')  # If user exists, redirect to logout or a different page
            except CustomUser.DoesNotExist:
                pass  # If user doesn't exist, proceed to render the forgot password page

        return render(request, 'forgot_password.html')
    
def verify_otp(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'verify_otp.html', context)

def new_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'new_password.html', context)
    
def my_all_exams(request):
    try:
        user = CustomUser.objects.get(id=request.session['user_id'])
        exam = Exam.objects.filter(user=user)

        # check for search query
        search_query = request.GET.get('search')
        if search_query:
            exam = exam.filter(exam_name__icontains=search_query)  # Filter based on search query
        # pagination
        paginator = Paginator(exam, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'exam': page_obj,
            'page_obj': page_obj,
            'search_query': search_query,
        }
        return render(request, 'my_all_exams.html', context)
    except Exam.DoesNotExist:
        
        context = {
            'exam': None            
        }
        return render(request, 'my_all_exams.html', context)

@login_required
def create_exam(request):
    if request.method == 'POST':
        print(request.POST)
        user_id = request.session.get('user_id')
        user = CustomUser.objects.get(id=user_id)

        exam = Exam.objects.create(
            user=user,
            exam_name=request.POST['exam_name'],
            exam_subject=request.POST['exam_subject'],
            exam_type=request.POST['exam_type'],
            number_of_questions=int(request.POST['number_of_questions']),
            difficulty=request.POST['difficulty'],
            time_setting=request.POST['time_setting'],
            exam_time=request.POST['exam_time'],
        )
        return redirect('create-questions', exam.id)  # Redirect to create questions view
    return render(request, 'create_exam.html')
    
def create_questions(request,id):
    exam = Exam.objects.get(id=id)
    if request.method == 'POST':
        print("Request POST Data:", request.POST)
        
        # Determine exam type
        exam_type = exam.exam_type  # Ensure your form has this input
        print(f"Exam type {exam_type}")
        if exam_type == 'MX':
            # For mixed type, capture the counts
            mcq_count = int(request.POST.get('mcq_count', 0))  # Count of MCQs
            tf_count = int(request.POST.get('tf_count', 0))    # Count of True/False questions
            
            mcq_questions = []
            tf_questions = []
            
            # Process MCQ Questions
            for i in range(1, mcq_count + 1):
                question = request.POST.get(f'question_{i}','').strip()
                option_a = request.POST.get(f'option_a_{i}','').strip()
                option_b = request.POST.get(f'option_b_{i}','').strip()
                option_c = request.POST.get(f'option_c_{i}','').strip()
                option_d = request.POST.get(f'option_d_{i}','').strip()
                correct_answer = request.POST.get(f'correct_answer_{i}','').strip()
                
                if question:  # Ensure there's a question
                    mcq_questions.append({
                        'question': question,
                        'options': {
                            'A': option_a,
                            'B': option_b,
                            'C': option_c,
                            'D': option_d
                        },
                        'correct_answer': correct_answer
                    })

                    # Save to the database
                    MCQQuestion.objects.create(
                        exam=exam,
                        question=question,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        correct_answer=correct_answer,
                    )

            # Process True/False Questions
            for i in range(1, tf_count + 1):
                question = request.POST.get(f'tf-question_{i}','').strip()  # Adjust as necessary
                correct_answer = request.POST.get(f'tf-correct-answer_{i}','').strip()
                
                if question:  # Check to ensure we have a question
                    tf_questions.append({
                        'question': question,
                        'correct_answer': correct_answer
                    })

                    # Save to the database
                    TrueFalseQuestion.objects.create(
                        exam=exam,
                        question=question,
                        correct_answer=(correct_answer == 'True')  # Convert to boolean
                    )

            exam.question_created = True
            exam.save()
            # After saving, you can redirect or return a response
            return redirect('create-questions', id=exam.id)
        
        elif exam_type == 'MCQ':
            # Handle MCQ-specific logic
            mcq_count = exam.number_of_questions # Count of MCQs
            
            for i in range(1, mcq_count + 1):
                question = request.POST.get(f'question_{i}','').strip()
                option_a = request.POST.get(f'option_a_{i}','').strip()
                option_b = request.POST.get(f'option_b_{i}','').strip()
                option_c = request.POST.get(f'option_c_{i}','').strip()
                option_d = request.POST.get(f'option_d_{i}','').strip()
                correct_answer = request.POST.get(f'correct_answer_{i}','').strip()
                
                if question:  # Ensure there's a question
                    # Save to the database
                    MCQQuestion.objects.create(
                        exam=exam,
                        question=question,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        correct_answer=correct_answer,
                    )
            exam.question_created = True
            exam.save()
            return redirect('create-questions', id=exam.id)
        
        elif exam_type == 'TF':
            # Handle True/False specific logic
            tf_count = exam.number_of_questions  # Count of True/False questions
            
            for i in range(1, tf_count + 1):
                question = request.POST.get(f'tf-question_{i}', '').strip()  # Get the full question text
                correct_answer = request.POST.get(f'tf-correct-answer_{i}', '').strip()
                
                if question:  # Check to ensure we have a question
                    # Save to the database
                    TrueFalseQuestion.objects.create(
                        exam=exam,
                        question=question.strip(),  # Ensure leading/trailing whitespace is removed
                        correct_answer=(correct_answer == 'True')  # Convert to boolean
                    )
            exam.question_created = True
            exam.save()
            return redirect('create-questions', id=exam.id)


        
        elif exam_type == 'SA':
            # Handle Short Answer logic
            sa_count = exam.number_of_questions  # Count of Short Answer questions
            
            for i in range(1, sa_count + 1):
                question = request.POST.get(f'sa-question_{i}', '').strip()
                correct_answer = request.POST.get(f'sa-correct-answer_{i}', '').strip()
                
                if question:  # Ensure there's a question
                    # Save to the database
                    ShortAnswerQuestion.objects.create(
                        exam=exam,
                        question=question,
                        correct_answer=correct_answer,
                    )
            exam.question_created = True
            exam.save()
            return redirect('create-questions', id=exam.id)
    else:
        number_of_questions = exam.number_of_questions
        mcqs = MCQQuestion.objects.filter(exam=exam)
        tf = TrueFalseQuestion.objects.filter(exam=exam)
        sa = ShortAnswerQuestion.objects.filter(exam=exam)

        all_questions = []
        
        # Add question_type attribute to each question
        for question in mcqs:
            question.question_type = 'MCQ'
            all_questions.append(question)
        
        for question in tf:
            question.question_type = 'TrueFalse'
            all_questions.append(question)

        for question in sa:
            question.question_type = 'ShortAnswer'
            all_questions.append(question)
         
        context = {
            'exam': exam,
            'number_of_questions': number_of_questions,
            'all_questions': all_questions,
        }
        return render(request, 'create_questions.html', context)
    
def publish_exam(request,id):
    try:
        exam = Exam.objects.get(id=id)

        exam.visibility = 'publish'
        exam.save()
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return redirect(referer_url)
        else:
            return redirect('my-all-exam')
    except Exam.DoesNotExist:
        return HttpResponseBadRequest("Exam not found.")


def private_exam(request,id):
    try:
        exam = Exam.objects.get(id=id)

        exam.visibility = 'private'
        exam.save()
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return redirect(referer_url)
        else:
            return redirect('my-all-exam') 
    except Exam.DoesNotExist:
        return HttpResponseBadRequest("Exam not found.")
    
def delete_exam(request, id):
    # Check if the request method is POST to confirm deletion
    exam = get_object_or_404(Exam, id=id)  # Retrieve the exam or return a 404 if not found
    exam.delete()  # Delete the exam
    return redirect('my-all-exams')  # Redirect to the exams list page (replace with your actual URL name)

def all_exams(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    all_exams = Exam.objects.filter(visibility='publish').exclude(user=user)
    print(all_exams)
    context = {
        'all_exams': all_exams,
    }
    return render(request, 'all_exam.html', context)
def view_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    total_enrollment = Enrollment.objects.filter(exam=exam).distinct().count()
    finish_exam = Enrollment.objects.filter(exam=exam, is_completed=True).count()
    
    if total_enrollment > 0:
        complation_rate = (finish_exam / total_enrollment) * 100
    else:
        complation_rate = 0

    context = {
        'exam': exam,
        'total_enrollment': total_enrollment,
        'complation_rate': complation_rate,
    }
    return render(request, 'view_exam.html', context)

    
def get_question(request, exam_id, index):
    mcq_questions = MCQQuestion.objects.filter(exam_id=exam_id)
    tf_questions = TrueFalseQuestion.objects.filter(exam_id=exam_id)
    sa_questions = ShortAnswerQuestion.objects.filter(exam_id=exam_id)

    total_questions = mcq_questions.count() + tf_questions.count() + sa_questions.count()
    
    if index < mcq_questions.count():
        question = mcq_questions[index]
        question_data = {
            'question': question.question,
            'type': 'MCQ',
            'options': {
                'a': question.option_a,
                'b': question.option_b,
                'c': question.option_c,
                'd': question.option_d,
            },
        }
    elif index < mcq_questions.count() + tf_questions.count():
        question = tf_questions[index - mcq_questions.count()]
        question_data = {
            'question': question.question,
            'type': 'TrueFalse',
        }
    else:
        question = sa_questions[index - mcq_questions.count() - tf_questions.count()]
        question_data = {
            'question': question.question,
            'type': 'ShortAnswer',
        }

    return JsonResponse({
        'question': question_data['question'],
        'type': question_data['type'],
        'options': question_data.get('options', {}),
        'id': question.id,
        'isLastQuestion': index >= total_questions - 1
    })

def enroll_exam(request, id):
    exam = get_object_or_404(Exam, id=id)

    mcq = MCQQuestion.objects.filter(exam=exam)
    tf = TrueFalseQuestion.objects.filter(exam=exam)
    sa = ShortAnswerQuestion.objects.filter(exam=exam)

    all_questions = []
    total_questions = mcq.count() + tf.count() + sa.count()

    for question in mcq:
        all_questions.append({
            'question': question.question,
            'type': 'MCQ',
            'options': {
                'a': question.option_a,
                'b': question.option_b,
                'c': question.option_c,
                'd': question.option_d,
            },
            'correct_answer': question.correct_answer,
        })

    for question in tf:
        all_questions.append({
            'question': question.question,
            'type': 'TrueFalse',
            'correct_answer': question.correct_answer,
        })  

    for question in sa:
        all_questions.append({
            'question': question.question,
            'type': 'ShortAnswer',
            'correct_answer': question.correct_answer,
        })
    user = CustomUser.objects.get(id=request.session['user_id'])
    try:
        enroll = Enrollment.objects.get(user=user, exam=exam)
        enroll.attempted += 1
        enroll.save()
    except Enrollment.DoesNotExist:
        Enrollment.objects.create(user=user, exam=exam, attempted=1)

    context = {
        'exam': exam,
        'all_questions': all_questions,
        'total_questions': total_questions,
        'exam_time': exam.exam_time,
        'time_setting': exam.time_setting,
    }
    return render(request, 'start_exam.html', context)

def submit_answers(request, exam_id):
    if request.method == 'POST':
        print("Request received to submit answers.")  # Debug print
        try:
            answers = request.POST.get('answers')
            print(f"Answers received: {answers}")  # Debug print
            
            if not answers:
                return JsonResponse({'error': 'No answers provided'}, status=400)

            answers_dict = json.loads(answers)  # Convert JSON string to dictionary
            print(f"Parsed Answers: {answers_dict}")  # Debug print

            # Fetching correct answers from database
            correct_answers = {}
            mcq_questions = MCQQuestion.objects.filter(exam_id=exam_id)
            tf_questions = TrueFalseQuestion.objects.filter(exam_id=exam_id)
            sa_questions = ShortAnswerQuestion.objects.filter(exam_id=exam_id)

            for question in mcq_questions:
                correct_answers[question.id] = question.correct_answer
            
            for question in tf_questions:
                correct_answers[question.id] = question.correct_answer
            
            for question in sa_questions:
                correct_answers[question.id] = question.correct_answer

            score = 0

            # Check answers against correct answers
            for question_id, user_answer in answers_dict.items():
                correct_answer = correct_answers.get(int(question_id))  # Ensure key is int
                print(f"Checking Question ID: {question_id}, User Answer: {user_answer}, Correct Answer: {correct_answer}")

                if str(user_answer) == str(correct_answer):  # Compare as strings
                    score += 1

            # Save ExamResult instance with the calculated score
            user = CustomUser.objects.get(id=request.session['user_id'])
            exam = Exam.objects.get(id=exam_id)
            enroll = Enrollment.objects.get(user=user, exam=exam)
            enroll.is_completed = True
            enroll.save()
            result = ExamResult(
                exam_id=exam_id, 
                user=user, 
                answers=answers_dict, 
                score=score,
                attempt_no = enroll.attempted,
                status = 'completed'
                )
            result.save()  # Save result to database

            return JsonResponse({'result_id': result.id})  # Return the result ID
        except json.JSONDecodeError as json_error:
            print(f"JSONDecodeError: {str(json_error)}")  # Debug print
            return JsonResponse({'error': 'Invalid JSON format: {}'.format(str(json_error))}, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug print
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)




def results_view(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)  # Fetch the result based on ID
    return render(request, 'results.html', {'result': result})  # Pass the result to your template

def enrolled_exams(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    results = ExamResult.objects.filter(user=user)
    return render(request, 'enrolled_exams.html', {'results': results})