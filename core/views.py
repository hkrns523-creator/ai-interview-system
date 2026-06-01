from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Resume, InterviewResult
from .resume_parser import extract_resume_data
from .ai.scoring import evaluate_answer
from django.contrib.auth.decorators import login_required
from .ai_generator import generate_questions
import json
from django.http import JsonResponse
from .skill_extractor import extract_skills
from .models import Role
from django.contrib import messages


@login_required
def home(request):
    return render(request,'home.html')

def register_view(request):

    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request,"Account created successfully")
        return redirect('login')

    if request.method == 'POST':
        messages.error(request,"Registration failed. Please check the details.")

    return render(request, 'register.html', {'form': form})

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request,"Login successful")
            return redirect('home')

        else:
            messages.error(request,"Invalid username or password")

    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def upload_resume(request):

    context = {}

    if request.method == 'POST':

        if 'resume' not in request.FILES:
            messages.error(request,"Please upload a resume file")
            return redirect('upload_resume')

        file = request.FILES['resume']

        if not file.name.endswith('.pdf'):
            messages.error(request,"Only PDF files are allowed")
            return redirect('upload_resume')

        resume = Resume.objects.create(
            user=request.user,
            file=file
        )


        result = extract_resume_data(resume.file.path)

        predicted_role = result['best_role']

        skills = result.get('skills', [])

        score = result['score']

        matched_roles = result['matched_roles']

        resume.score = score

        resume.skills = ",".join(skills)

        resume.save()

        messages.success(request,"Resume analyzed successfully")

        context = {

            'score': score,

            'skills': skills,

            'predicted_role': predicted_role,

            'matched_roles': matched_roles,

            'recommended_roles': matched_roles
        }

    return render(request,'upload_resume.html',context)

@login_required
def interview(request):

    role = request.session.get('role')

    questions = request.session.get(
        'questions',
        []
    )

    q_index = request.session.get(
        'q_index',
        0
    )

    total_score = request.session.get(
        'total_score',
        0
    )

    # Fetch all roles from database
    all_roles = Role.objects.prefetch_related('skills')

    # START INTERVIEW
    if request.method == 'POST' and 'start_interview' in request.POST:

        role = request.POST['role']

        previous_questions = request.session.get(
            'asked_questions',
            []
        )

        # Get selected role object
        selected_role = Role.objects.prefetch_related(
            'skills'
        ).get(name=role)

        # Get skills dynamically
        role_skills = [
            skill.name.lower()
            for skill in selected_role.skills.all()
        ]

        # AI-generated questions
        generated_questions = generate_questions(
            role,
            role_skills,
            previous_questions
        )

        request.session['questions'] = generated_questions

        request.session['role'] = role

        request.session['q_index'] = 0

        request.session['total_score'] = 0

        # Store asked questions
        all_previous = previous_questions + generated_questions

        request.session['asked_questions'] = all_previous

        questions = generated_questions

        q_index = 0

        messages.success(request,f"{role} interview started successfully")

    # SUBMIT ANSWER
    elif request.method == 'POST' and 'submit_answer' in request.POST:

        answer = request.POST.get('answer')

        if not answer.strip():

            return render(request, 'interview.html', {

                'question': questions[q_index],

                'role': role,

                'error': 'Answer is required'
            
            })

        current_question = questions[q_index]

        # Correct answer + keywords
        correct_answer = current_question['answer']

        keywords = current_question['keywords']

        # Advanced AI evaluation
        result = evaluate_answer(
            answer,
            correct_answer,
            keywords
        )

        score = result['final_score']

        feedback = result['feedback']

        # Store interview results temporarily

        interview_results = request.session.get(
            'interview_results',
            []
        )

        interview_results.append({

            'question': current_question['question'],

            'answer': answer,

            'score': score,

            'feedback': feedback

        })

        request.session['interview_results'] = interview_results

        total_score += score

        request.session['total_score'] = total_score

        q_index += 1

        request.session['q_index'] = q_index
        messages.success(request,"Answer submitted successfully")

        if q_index >= len(questions):

            final_score = round(
                total_score / len(questions),
                2
            )

            InterviewResult.objects.create(
            
                user=request.user,

                role=role,

                score=final_score,

                feedback=f"Interview completed with score {final_score}/10"

            )

            # STORE RESULT DATA IN SESSION

            request.session['final_score'] = final_score

            request.session['feedback'] = feedback

            request.session['semantic'] = result['semantic']

            request.session['keyword'] = result['keyword']

            request.session['grammar'] = result['grammar']

            # REMOVE INTERVIEW SESSION DATA

            request.session.pop('questions', None)

            request.session.pop('q_index', None)

            request.session.pop('total_score', None)

            request.session.pop('role', None)

            request.session.pop('interview_results', None)

            messages.success(request, "Interview completed successfully")

            return redirect('result_page')


    if role and q_index < len(questions):

        return render(request, 'interview.html', {

            'question': questions[q_index],

            'role': role,

            'q_index': q_index,

            'total_questions': len(questions)
        })

    # ROLE SELECTION
    return render(request, 'interview.html', {

        'roles': all_roles
    })

@login_required
def dashboard(request):

    results = InterviewResult.objects.filter(
        user=request.user).order_by('created_at')

    total_score = 0

    highest_score = 0

    for result in results:

        total_score += result.score

        if result.score > highest_score:
            highest_score = result.score

    return render(request, 'dashboard.html', {

        'results': results,

        'total_score': total_score,

        'highest_score': highest_score

    })
def result_page(request):

    context = {

        'final_score': request.session.get('final_score', 0),

        'feedback': request.session.get('feedback', ''),

        'semantic': request.session.get('semantic', 0),

        'keyword': request.session.get('keyword', 0),

        'grammar': request.session.get('grammar', 0)

    }

    return render(request, 'result.html', context)