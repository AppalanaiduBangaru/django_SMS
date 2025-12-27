from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.shortcuts import render
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

students = Student.objects.all()
paginator = Paginator(students, 10)  


@login_required
def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'query': query
    })
    
    



def home(request):
    return render(request, 'home.html')


def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {'form': form})

def student_update(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {'form': form})

def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})
