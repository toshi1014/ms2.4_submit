from django.shortcuts import render
from django.http import HttpResponseRedirect


def top(request):
    return render(request, "top.html", {})


def redirect_accounts(request):
    return HttpResponseRedirect("index/")


def redirect_class_info(request):
    return HttpResponseRedirect("class_info/")


def redirect_seminar_info(request):
    return HttpResponseRedirect("seminar_info/")


def redirect_circle_info(request):
    return HttpResponseRedirect("circle_info/")


def redirect_shimmeringfuseda(request):
    return HttpResponseRedirect("dubious/")