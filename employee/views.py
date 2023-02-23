from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from .models import Department, Role, Employee
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request, 'employee/index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = { "emps": emps}
    return render(request, 'employee/all_emp.html', context)

def add_emp(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        salary = int(request.POST["salary"])
        bonus = int(request.POST["bonus"])
        role = int(request.POST["role"])
        department = int(request.POST["department"])
        phone = int(request.POST["phone"])
        joining_date = request.POST["joining_date"]
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, role_id=role, department_id=department, phone=phone, joining_date=joining_date)
        new_emp.save()
        return redirect("all_emp")

    elif request.method == "GET":
        return render (request, "employee/add_emp.html")
    else:
        return HttpResponse("An error has occurred; please try again.")

def remove_emp(request, pk):
    emps = get_object_or_404(Employee, id=pk)
    context = {"emps": emps}
    if request.method == "POST":
        emps.delete()
        return redirect("home")
    
    #If the method is not POST, the page will render "confirm_delete.html" to delete the data.
    else:
        return render(request, "employee/confirm_delete.html", context)
    

def filter_emp(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        department = request.POST["department"]
        role = request.POST["role"]
        emps = Employee.objects.all()
        if first_name:
            emps =  emps.filter(Q(first_name__icontains = first_name))
        if last_name:
            emps =  emps.filter(Q(last_name__icontains = last_name))
        if department:
            emps =  emps.filter(Q(department__name__icontains = department))
        if role:
            emps =  emps.filter(Q(role__name__icontains = role))

        context = { "emps": emps }
        return render(request, 'employee/all_emp.html', context)
    
    elif request.method == "GET":
        return render(request, "employee/filter_emp.html")
    else:
        return HttpResponse("An error Occurred")
