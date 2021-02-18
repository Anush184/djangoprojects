from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import CreateTaskForm
from django.contrib import messages


def homepage(request):
    return render(request, 'to_do/homepage.html')


def home(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'to_do/home.html', context)


def new_task(request):
    form = CreateTaskForm()
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The task is created successfully!")
            return redirect('home')
        else:
            messages.warning(request, "The task is not created!")

    return render(request, 'to_do/new_task.html', {'form': form})


def task_update(request, pk):
    task = Task.objects.get(id=pk)
    form = CreateTaskForm(instance=task)
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Update was  done successfully!")
            return redirect('home')
        else:
            messages.warning(request, "Update was failed!")
    context = {'form': form}
    return render(request, 'to_do/task_update.html', context)


def task_view(request, pk):
    special_task = get_object_or_404(Task, pk=pk)
    return render(request, 'to_do/task_view.html', {'task': special_task})


def task_delete(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Task was deleted.")
        return redirect('home')
    # task_to_delete = get_object_or_404(Task, pk=pk)
    # task_to_delete.delete()
    # messages.success(request, "Task was deleted.")
    # return redirect("home")
    context = {'item': item}

    return render(request, 'to_do/task_delete.html', context)




