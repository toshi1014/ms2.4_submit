from django.shortcuts import render

def se_faculty_list(request):
    return render(request, "seminar_info/se_faculty_list.html", {})