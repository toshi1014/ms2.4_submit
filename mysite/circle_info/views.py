from django.shortcuts import render

def campus_list(request):
    return render(request, "circle_info/campus_list.html", {})