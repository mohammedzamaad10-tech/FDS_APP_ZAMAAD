from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg
from django.http import HttpResponse
import csv
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
from collections import defaultdict

from .models import StudySession
from .forms import StudySessionForm, SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'tracker/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Get user's study sessions
    sessions = StudySession.objects.filter(user=request.user).order_by('-date_time')
    
    # Calculate total study hours per subject
    subject_hours = sessions.values('subject').annotate(
        total_hours=Sum('duration'),
        avg_productivity=Avg('productivity_rating')
    ).order_by('-total_hours')
    
    # Generate charts
    charts = generate_charts(request.user)
    
    # Generate insights
    insights = generate_insights(request.user)
    
    context = {
        'subject_hours': subject_hours,
        'charts': charts,
        'insights': insights,
        'total_sessions': sessions.count(),
        'total_hours': sessions.aggregate(Sum('duration'))['duration__sum'] or 0,
        'sessions': sessions,  # Pass sessions to the template for chart data
    }
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def add_session(request):
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, "Study session added successfully!")
            return redirect('dashboard')
    else:
        form = StudySessionForm()
    
    return render(request, 'tracker/add_session.html', {'form': form})

@login_required
def session_list(request):
    sessions = StudySession.objects.filter(user=request.user)
    return render(request, 'tracker/session_list.html', {'sessions': sessions})

@login_required
def edit_session(request, session_id):
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    
    if request.method == 'POST':
        form = StudySessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Study session updated successfully!")
            return redirect('session_list')
    else:
        form = StudySessionForm(instance=session)
    
    return render(request, 'tracker/edit_session.html', {'form': form})

@login_required
def delete_session(request, session_id):
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    
    if request.method == 'POST':
        session.delete()
        messages.success(request, "Study session deleted successfully!")
        return redirect('session_list')
    
    return render(request, 'tracker/delete_session.html', {'session': session})

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="study_sessions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Subject', 'Date & Time', 'Duration (hours)', 'Productivity Rating'])
    
    sessions = StudySession.objects.filter(user=request.user)
    for session in sessions:
        writer.writerow([
            session.subject,
            session.date_time,
            session.duration,
            session.productivity_rating
        ])
    
    return response

@login_required
def predict_productivity(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        day_of_week = int(request.POST.get('day_of_week'))
        
        # Get user's sessions for this subject and day of week
        sessions = StudySession.objects.filter(
            user=request.user,
            subject=subject,
            date_time__week_day=day_of_week
        )
        
        if sessions.exists():
            avg_productivity = sessions.aggregate(Avg('productivity_rating'))['productivity_rating__avg']
            prediction = round(avg_productivity, 1)
        else:
            prediction = "No data available for prediction"
        
        return render(request, 'tracker/predict.html', {
            'subject': subject,
            'day_of_week': day_of_week,
            'prediction': prediction
        })
    
    # Get unique subjects for the current user
    subjects = StudySession.objects.filter(user=request.user).values_list('subject', flat=True).distinct()
    
    return render(request, 'tracker/predict.html', {'subjects': subjects})

def generate_charts(user):
    sessions = StudySession.objects.filter(user=user)
    
    if not sessions:
        return {}
    
    # Convert to DataFrame for easier manipulation
    data = []
    for session in sessions:
        data.append({
            'subject': session.subject,
            'date_time': session.date_time,
            'duration': session.duration,
            'productivity_rating': session.productivity_rating,
            'day_of_week': session.date_time.strftime('%A'),
            'hour_of_day': session.date_time.hour
        })
    
    df = pd.DataFrame(data)
    
    charts = {}
    
    # Bar chart of hours per subject
    if not df.empty:
        subject_hours = df.groupby('subject')['duration'].sum().reset_index()
        fig = px.bar(subject_hours, x='subject', y='duration', 
                    title='Total Hours by Subject',
                    labels={'duration': 'Hours', 'subject': 'Subject'})
        charts['hours_by_subject'] = plot(fig, output_type='div')
        
        # Line chart of study hours over time
        df['date'] = df['date_time'].dt.date
        daily_hours = df.groupby('date')['duration'].sum().reset_index()
        fig = px.line(daily_hours, x='date', y='duration',
                    title='Study Hours Over Time',
                    labels={'duration': 'Hours', 'date': 'Date'})
        charts['hours_over_time'] = plot(fig, output_type='div')
        
        # Heatmap of study activity
        pivot = df.pivot_table(
            index='day_of_week', 
            columns=df['date_time'].dt.strftime('%U').astype(int),  # Week number
            values='duration', 
            aggfunc='sum'
        ).fillna(0)
        
        fig = px.imshow(pivot, 
                        labels=dict(x="Week of Year", y="Day of Week", color="Hours"),
                        title="Study Activity Heatmap")
        charts['activity_heatmap'] = plot(fig, output_type='div')
    
    return charts

def generate_insights(user):
    sessions = StudySession.objects.filter(user=user)
    insights = []
    
    if not sessions:
        return ["Start logging your study sessions to see insights!"]
    
    # Convert to DataFrame for analysis
    data = []
    for session in sessions:
        data.append({
            'subject': session.subject,
            'date_time': session.date_time,
            'duration': session.duration,
            'productivity_rating': session.productivity_rating,
            'day_of_week': session.date_time.strftime('%A'),
            'hour_of_day': session.date_time.hour
        })
    
    df = pd.DataFrame(data)
    
    # Most studied subject
    if not df.empty:
        subject_hours = df.groupby('subject')['duration'].sum()
        if not subject_hours.empty:
            most_studied = subject_hours.idxmax()
            insights.append(f"You study {most_studied} the most.")
        
        # Best day for productivity
        day_productivity = df.groupby('day_of_week')['productivity_rating'].mean()
        if not day_productivity.empty:
            best_day = day_productivity.idxmax()
            insights.append(f"Your highest productivity is on {best_day}s.")
        
        # Best time of day
        df['time_category'] = pd.cut(
            df['hour_of_day'],
            bins=[0, 6, 12, 18, 24],
            labels=['Night', 'Morning', 'Afternoon', 'Evening']
        )
        
        subject_time = df.groupby(['subject', 'time_category']).size().reset_index(name='count')
        for subject in df['subject'].unique():
            subject_df = subject_time[subject_time['subject'] == subject]
            if not subject_df.empty:
                best_time = subject_df.loc[subject_df['count'].idxmax(), 'time_category']
                insights.append(f"You study {subject} most often in the {best_time.lower()}.")
        
        # Long sessions and productivity
        df['long_session'] = df['duration'] >= 2
        long_prod = df[df['long_session']]['productivity_rating'].mean()
        short_prod = df[~df['long_session']]['productivity_rating'].mean()
        
        if not (pd.isna(long_prod) or pd.isna(short_prod)):
            if long_prod > short_prod:
                insights.append(f"Consistent 2+ hours study sessions increase your average productivity score.")
            else:
                insights.append(f"Shorter study sessions seem to be more productive for you.")
    
    return insights
