from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task

# ১. ইউজার রেজিস্ট্রেশন
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo_app/register.html', {'form': form})

# ২. টাস্ক লিস্ট দেখা এবং নতুন টাস্ক যোগ করা
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect('task_list')
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

# ৩. টাস্ক কমপ্লিট বা ইনকমপ্লিট মার্ক করা
@login_required
def toggle_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.complete = not task.complete
    task.save()
    return redirect('task_list')

# ৪. টাস্ক ডিলিট করা
@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return redirect('task_list')

# ৫. টাস্ক এডিট বা আপডেট করা
@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            task.title = new_title
            task.save()
        return redirect('task_list')
    return render(request, 'todo_app/update_task.html', {'task': task})
