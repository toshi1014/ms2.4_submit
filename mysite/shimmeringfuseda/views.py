from django.shortcuts import render, redirect
from django.http import HttpResponse
from maintenance_mode.core import set_maintenance_mode
import pandas as pd
import csv, glob
import class_info.views as class_views


def sf_top(request):
    return render(request, "shimmeringfuseda/sf_top.html", {})


def sf_login(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        family_name = request.POST["family_name"]
        if first_name == "spongebob" and family_name == "squarepants":
            global KEY
            KEY = "KEY"
            return redirect("sf_control", key = KEY)
        else:
            pass
    return render(request, "shimmeringfuseda/sf_top.html", {})


def sf_logout(request):
    global KEY
    del KEY
    return render(request, "shimmeringfuseda/sf_top.html", {})


def sf_control(request, key):
    if not key == KEY:
        exit()
    return render(request, "shimmeringfuseda/sf_control.html", {"key" : key})


def sf_facul_list(request, key, facul):
    Facul = facul.upper()
    path = "csv/class_info/" + Facul + "/*.csv"
    list_name = "csv/class_info/" + Facul + "\\" + facul + "_list.csv"
    csv_files = [list_name.split("/")[-1]]
    for file in glob.glob(path):
        if not file == list_name:
            f = file.split("/")[-1]
            csv_files.append(f)
    html = "shimmeringfuseda/sf_list.html"
    arg = class_views.facul_argument(facul)
    res = {"csv_files": csv_files, "key": key, "facul_argument" : arg}
    return render(request, html, {"res" : res})


def sf_download(request, key, file):
    if not key == KEY:
        exit()

    none = ""
    ffile = "csv/class_info/" + file
    response = HttpResponse(none, content_type='text/csv')
    rdf = pd.read_csv(ffile)

    if file[-8:-4] == "list":
        columns = [
            "sum", "clas", "latest", "semes", "prof", "ease", "aplus", "fulfil",
            "syllabus", "gender", "grade"
            ]
    else:
        columns = [
            "index", "date", "semes", "prof", "ease", "aplus", "fulfil",
            "comme", "contributor", "gender", "grade", "like"
        ]

    df = rdf[columns]
    columns.insert(0, "")
    writer = csv.writer(response)
    writer.writerow(columns)
    for v in df.itertuples():
        writer.writerow(v)
    response["Content-Disposition"] = "filename=" + str(ffile)
    return response


def sf_add_syllabus(request, key, facul):
    if request.method == "POST":
        rsyllabus = request.POST["syllabus"]
        if rsyllabus:
            syllabus = list(rsyllabus.split(","))
            Facul = facul.upper()
            path = "csv/class_info/" + Facul + "/" + facul + "_list.csv"
            columns = [
                "sum", "clas", "latest", "semes", "prof", "ease", "aplus", "fulfil",
                "syllabus", "gender", "grade"
            ]
            rdf = pd.read_csv(path)
            df = rdf[columns]
            df["syllabus"].iloc[1:] = syllabus
            df.to_csv(path)

            none = ""
            rconf_df = pd.read_csv(path)
            conf_df = rconf_df[columns]
            response = HttpResponse(none, content_type='text/csv')
            columns.insert(0, "")
            writer = csv.writer(response)
            writer.writerow(columns)
            for v in conf_df.itertuples():
                writer.writerow(v)
            response["Content-Disposition"] = "filename=" + str(path)
            return response
        else:
            pass
    arg = class_views.facul_argument(facul)
    return render(request, "shimmeringfuseda/sf_edit.html", {"key": key, "facul_argument" : arg})


def sf_maintenance(request, key):
    if not key == KEY:
        exit()
    path = "mysite/maintenance_mode_state.txt"
    f = open(path, "r")
    state = f.read()
    f.close()
    res = {"key" : key, "state" : state}
    return render(request, "shimmeringfuseda/sf_maintenance.html", {"res" : res})


def sf_maintenance_mode(request, key, state):
    if not key == KEY:
        exit()
    if request.method == "POST":
        if state == "0":
            set_maintenance_mode(True)
        else:
            set_maintenance_mode(False)
    return redirect("sf_maintenace", key = key)


def sf_list(request, key, facul):
    if not key == KEY:
        exit()
    return sf_facul_list(request, key, facul)


def sf_edit(request, key, facul):
    if not key == KEY:
        exit()
    arg = class_views.facul_argument(facul)
    return render(request, "shimmeringfuseda/sf_edit.html", {"key" : key, "facul_argument" : arg})


def sf_syllabus(request, key, facul):
    if not key == KEY:
        exit()
    return sf_add_syllabus(request, key, facul)