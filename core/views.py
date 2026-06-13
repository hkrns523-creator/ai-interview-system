from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (ResumeSerializer, InterviewResultSerializer,
                           QuestionSerializer, RoleSerializer)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Resume, InterviewResult, Question, Role, Skill
from .resume_parser import extract_resume_data,get_skill_gap,generate_suggestions
from .ai.scoring import evaluate_answer
from django.contrib.auth.decorators import login_required
from .ai_generator import generate_questions
import json
from django.http import JsonResponse
from .models import Role
from django.contrib import messages
from django.views.decorators.cache import never_cache


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

        missing_skills = get_skill_gap(
            predicted_role,
            skills
        )

        suggestions = generate_suggestions(
            score,
            skills,
            result['text']
        )

        resume.score = score

        resume.skills = ",".join(skills)

        resume.role = predicted_role

        resume.save()

        messages.success(request,"Resume analyzed successfully")

        context = {

            'score': score,

            'skills': skills,

            'predicted_role': predicted_role,

            'matched_roles': matched_roles,

            'recommended_roles': matched_roles,

            'missing_skills': missing_skills,

            'suggestions': suggestions,

            'skills_score': result.get('skills_score'),

            'semantic_score': result.get('semantic_score'),

            'project_score': result.get('project_score'),

            'completeness_score': result.get('completeness_score'), 
        }   

    return render(request,'upload_resume.html',context)

@never_cache
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

        correct_answer = current_question['answer']

        keywords = current_question['keywords']

        result = evaluate_answer(
            answer,
            correct_answer,
            keywords
        )

        score = result['final_score']

        feedback = result['feedback']

        interview_results = request.session.get(
            'interview_results',
            []
        )

        interview_results.append({

            'question': current_question['question'],

            'answer': answer,

            'score': score,

            'feedback': feedback,

            'semantic': result['semantic'],

            'keyword': result['keyword'],

            'grammar': result['grammar'],
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

            num_results = len(interview_results)

            avg_semantic = round(
                sum(r['semantic'] for r in interview_results) / num_results, 2
            )

            avg_keyword = round(
                sum(r['keyword'] for r in interview_results) / num_results, 2
            )

            avg_grammar = round(
                sum(r['grammar'] for r in interview_results) / num_results, 2
            )

            combined_feedback = []

            for r in interview_results:

                combined_feedback.extend(r.get('feedback', []))

            InterviewResult.objects.create(

                user=request.user,
                role=role,
                score=final_score,
                feedback=f"Interview completed with score {final_score}/10. " + " ".join(combined_feedback)

            )

            request.session['final_score'] = final_score

            #request.session['feedback'] = combined_feedback

            request.session['semantic'] = avg_semantic

            request.session['keyword'] = avg_keyword

            request.session['grammar'] = avg_grammar

            request.session['breakdown'] = interview_results

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

@never_cache
@login_required
def result_page(request):

    print("User authenticated:", request.user.is_authenticated)
    print("User:", request.user)
    print("Session keys:", list(request.session.keys()))

    final_score = request.session.get('final_score')

    if final_score is None:
        return redirect('interview')

    context = {

        'final_score': final_score,

        'semantic': request.session.get('semantic', 0),

        'keyword': request.session.get('keyword', 0),

        'grammar': request.session.get('grammar', 0),

        'breakdown': request.session.get('breakdown', []),

    }

    return render(request, 'result.html', context)

# ─ Resume API ─

@api_view(['GET'])
def api_resume_list(request):

    resumes = Resume.objects.select_related('user').all()
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_resume_detail(request, pk):

    try:
        resume = Resume.objects.select_related('user').get(pk=pk)

    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=404)
    serializer = ResumeSerializer(resume)
    return Response(serializer.data)


@api_view(['GET'])
def api_resume_score(request, pk):

    try:
        resume = Resume.objects.select_related('user').get(pk=pk)

    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=404)

    return Response({
        'candidate': resume.user.username,
        'role': resume.role,
        'ats_score': resume.score,
        'result': 'pass' if resume.score >= 70 else 'fail',
        'skills': resume.skills
    })


#  ─ Interview API ─

@api_view(['GET'])
def api_interview_list(request):

    results = InterviewResult.objects.select_related('user').all()
    serializer = InterviewResultSerializer(results, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def api_interview_by_role(request, role):

    results = InterviewResult.objects.select_related('user').filter(
        role__icontains=role
    )

    if not results.exists():
        return Response({'error': f'No results for role: {role}'}, status=404)

    serializer = InterviewResultSerializer(results, many=True)

    return Response({

        'role': role,
        'count': results.count(),
        'average_score': round(
            sum(r.score for r in results) / results.count(), 2
        ),
        'results': serializer.data

    })


# ─ Question API ─

@api_view(['GET'])
def api_question_list(request):

    questions = Question.objects.all()
    role = request.query_params.get('role')
    difficulty = request.query_params.get('difficulty')

    if role:
        questions = questions.filter(role__icontains=role)

    if difficulty:
        questions = questions.filter(difficulty__icontains=difficulty)

    serializer = QuestionSerializer(questions, many=True)

    return Response({

        'count': questions.count(),
        'questions': serializer.data

    })


# ─ Role API ─

@api_view(['GET'])
def api_role_list(request):

    roles = Role.objects.prefetch_related('skills').all()
    serializer = RoleSerializer(roles, many=True)

    return Response(serializer.data)
