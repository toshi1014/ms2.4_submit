from django.shortcuts import render, get_object_or_404, redirect
from .models import Reply, SK, SY, HO, SG, KY, KO, BU, BK, KI, SO, SE, SP, JK, GE
from accounts.models import MyPage
from .forms import ReplyForm, SKForm, SYForm, HOForm, SGForm, KYForm, BUForm, BKForm, \
    KOForm, KIForm, SOForm, SEForm, SPForm, JKForm, GEForm
from django.db.models import Q
import pandas as pd
import os.path
from django.utils import timezone
from django.utils.timezone import localtime
from django.http import HttpResponseRedirect


faculs = [
    [SK, "sk", "政経", "PSE", SKForm], [SY, "sy", "商", "SOC", SYForm], [HO, "ho", "法", "LAW", HOForm],
    [SG, "sg", "社学", "SSS", SGForm], [KY, "ky", "教育", "EDU", KYForm], [KO, "ko", "国教", "SILS", KOForm],
    [BU, "bu", "文", "HSS", BUForm], [BK, "bk", "文化構想", "CMS", BKForm],
    [KI, "ki", "基幹", "FSE", KIForm], [SO, "so", "創造", "CSE", SOForm], [SE, "se", "先進", "ASE", SEForm],
    [SP, "sp", "スポ科", "SPS", SPForm], [JK, "jk", "人間科学部", "HUM", JKForm],
    [GE, "ge", "GEC", GEForm]
]


def facul_argument(facul):
    for fac in faculs:
        if fac[1] == facul:
            return fac


def faculty_list(request):
    return render(request, "class_info/faculty_list.html", {})


def top_search(request, prof):
    pro = prof
    if not pro == "normal_search":
        query = pro
    else:
        query = request.GET.get("query")
    if query:
        counter = 0
        result_box = []
        for facul in faculs:
            rbox = []
            classes = facul[0].objects.filter(clas__icontains = query).values("clas").distinct()
            rprofs = facul[0].objects.filter(prof__icontains = query).values("prof").distinct()
            profs = facul[0].objects.filter(prof__icontains=  rprofs).values("clas").distinct()
            for clas in classes:
                rbox.append(clas)
            for proff in profs:
                if proff not in rbox:
                    rbox.append(proff)
            count = len(rbox)
            counter += count
            box = []
            gpath = "csv/class_info/" + facul[1].upper() + "/" + facul[1] + "_list.csv"
            gdf = pd.read_csv(gpath)
            for c in rbox:
                info_box = []
                cla = c.get("clas")
                df = gdf[gdf["clas"] == cla]
                info = percentage(df)
                for v in info:
                    origin = v[0]
                    w = v[0].split(" - ")
                    w.append(origin)
                    v[0] = w
                    info_box.append(v)
                box.append(info_box)
            arg = facul_argument(facul[1])
            box = [box]
            box.insert(0, [[count], arg])
            result_box.append(box)
    else:
        return redirect("faculty_list")

    res = {"query": query, "counter": counter, "results": result_box}
    return render(request, "class_info/top_result.html", {"res" : res})


def counter(df, gender, grade):
    Gender = df.loc[0, "gender"].strip("'[]").split(",")
    Grade = df.loc[0, "grade"].strip("'[]").split(",")

    if gender == "male":
        Gender[0] = int(Gender[0]) + 1
    elif gender == "female":
        Gender[1] = int(Gender[1]) + 1
    if grade == "1":
        Grade[0] = int(Grade[0]) + 1
    elif grade == "2":
        Grade[1] = int(Grade[1]) + 1
    elif grade == "3":
        Grade[2] = int(Grade[2]) + 1
    elif grade == "4":
        Grade[3] = int(Grade[3]) + 1
    a = []
    for v in [Gender, Grade]:
        a.append((",").join(map(str, v)))

    return a[0], a[1]


def make_csv(request, contributor, post, facul):
    cla = post.clas
    semes = post.semes
    prof = post.prof
    ease = post.ease[-1]
    aplus = post.aplus[-1]
    fulfil = post.fulfil[-1]
    date = str(post.date)[:19]
    comme = post.comme

    if contributor == "unknown":
        gender = 0
        grade = 0
    else:
        user = MyPage.objects.get(name = contributor)
        gender = user.gender
        grade = user.grade

    gpath = "csv/class_info/" + facul + "/" + facul.lower() + "_list.csv"
    path = "csv/class_info/" + facul + "/" + cla + ".csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = df[[
            "index", "date", "semes", "prof", "ease", "aplus", "fulfil",
            "comme", "contributor", "gender", "grade", "like"
        ]]

        Dsum = int(df.loc[0, "index"].split("-")[0])
        Sum = int(df.loc[0, "index"].split("-")[1])
        if not ease == "e":
            Sum += 1
            Dsum += 1
            Ease = float(df.loc[0, "ease"])
            Ease = str(((Ease * (Dsum - 1) + float(ease)) / Dsum))[:3]
            Aplus = float(df.loc[0, "aplus"])
            Aplus = str((Aplus * (Dsum - 1) + float(aplus)) / Dsum)[:3]
            Fulfil = float(df.loc[0, "fulfil"])
            Fulfil = str((Fulfil * (Dsum - 1) + float(fulfil)) / Dsum)[:3]
        else:
            Sum += 1
            Ease = df.loc[0, "ease"]
            Aplus = df.loc[0, "aplus"]
            Fulfil = df.loc[0, "fulfil"]
        Index = str(Dsum) + "-" + str(Sum)
        cnt = counter(df, gender, grade)

        df.loc[0] = [
            Index, 0, 0, 0, Ease, Aplus, Fulfil, 0, 0, cnt[0], cnt[1], 0
        ]
        df.loc[Sum] = [
            Sum, date, semes, prof, ease, aplus, fulfil,
            comme, contributor, gender, grade, 0
        ]
        df.to_csv(path)

        gdf = pd.read_csv(gpath)
        gdf = gdf[[
            "sum", "clas", "latest", "semes", "prof", "ease", "aplus", "fulfil",
            "syllabus", "gender", "grade"
        ]]
        Sum = int(gdf[gdf["clas"] == cla]["sum"])
        Sum += 1
        syllabus = gdf[gdf["clas"] == cla]["syllabus"]
        gdf[gdf["clas"] == cla] = [
            Sum, cla, date, semes, prof, Ease, Aplus, Fulfil, syllabus, cnt[0], cnt[1]
        ]
        gdf.to_csv(gpath)

    else:
        data = {
            "index": ["1-1"], "date" : [0], "semes": [0], "prof": [0], "ease": [0],
            "aplus": [0], "fulfil" : [0],"comme" : ["0"], "contributor" : ["0"],
            "gender" : ["0, 0"], "grade" : ["0, 0, 0, 0"], "like" : ["0"]
        }
        df = pd.DataFrame(data, columns = [
            "index", "date", "semes", "prof", "ease", "aplus", "fulfil",
            "comme", "contributor", "gender", "grade", "like"
        ])
        cnt = counter(df, gender, grade)
        df.loc[0] = [
            "1-1", 0, 0, 0, ease, aplus, fulfil, 0, 0, cnt[0], cnt[1], 0
        ]
        df.loc[1] = [
            1, date, semes, prof, ease, aplus, fulfil,
            comme, contributor, gender, grade, 0
        ]
        df.to_csv(path)

        gdf = pd.read_csv(gpath)
        gdf = gdf[[
            "sum", "clas", "latest", "semes", "prof", "ease", "aplus",
            "fulfil", "syllabus", "gender", "grade"
        ]]
        Sum = int(gdf.loc[0, "sum"])
        Sum += 1
        gdf.loc[0, "sum"] = Sum
        gdf.loc[Sum] = [
            1, cla, date, semes, prof, ease, aplus, fulfil,
            "SyllabusComingSoon", cnt[0], cnt[1]
        ]
        gdf.to_csv(gpath)


def percentage(df):
    classes = []
    for v in df.itertuples(name = None):
        box = []
        for n in [11, 12]:
            try:
                u = int(v[n].replace(" ", "")[0])
                d = int(v[n].replace(" ", "")[2])
                s = (u + d) / 100
                try:
                    a = str(u / s).split(".")[0] + "%-" + str(d / s).split(".")[0] + "%"
                except:
                    a = "0%-0%"
            except:
                pass
            try:
                t = int(v[n].replace(" ", "")[4])
                c = int(v[n].replace(" ", "")[6])
                s = (u + d + t + c) / 100
                try:
                    a = str(u / s).split(".")[0] + "%-" + str(d / s).split(".")[0] + "%-" + str(t / s).split(".")[0] + "%-" + str(c / s).split(".")[0] + "%"
                except:
                    a = "0%-0%-0%-0%"
            except:
                pass

            box.append(a)

        classes.append(
            [v[3], [v[7]], [v[8]], [v[9]], [box[0]], [box[1]]]
        )
    return classes


def facul_list(request, facul):
    Facul = facul[1].upper()
    gpath = "csv/class_info/" + Facul + "/" + facul[1] + "_list.csv"
    if not os.path.exists(gpath):
        data = {
            "sum": [0], "clas" : [0], "latest" : [0], "semes": [0], "prof": [0],
            "ease": [0], "aplus": [0], "fulfil" : [0], "syllabus" : [0],
            "gender" : ["0, 0"], "grade" : ["0, 0, 0, 0"]
        }
        gdf = pd.DataFrame(data, columns = [
            "sum", "clas", "latest", "semes", "prof", "ease", "aplus", "fulfil",
            "syllabus", "gender", "grade"
        ])
        gdf.to_csv(gpath)

    classes = []
    df = pd.read_csv(gpath, header = 1)
    info = percentage(df)
    for v in info:
        origin = v[0]
        w = v[0].split(" - ")
        w.append(origin)
        v[0] = w
        classes.append(v)

    html = "class_info/list.html"
    arg= facul_argument(facul[1])
    return render(request, html, {"classes" : classes, "facul_argument" : arg})


def class_list(request, clas, facul, modelform):
    Facul = facul[1].upper()
    path = "csv/class_info/" + Facul + "/" + facul[1] + "_list.csv"
    rdf = pd.read_csv(path)
    df = rdf[rdf["clas"] == clas]
    info = [0]
    rinfo = percentage(df)
    for r in rinfo:
        for v in r:
            v = v[0]
            info.append(v)
    info = info[2:]
    rposts = facul[0].objects.filter(clas = clas).order_by("id").reverse()

    try:
        mypage = MyPage.objects.get(name = request.user.username)
        like = mypage.like
        like_list = str(like).split(",")
        posts = []
        for p in rposts:
            pid = p.id
            lsign = 0
            replied = get_object_or_404(facul[0], pk = pid)
            rep = replied.reply
            rep_pk = rep.split(",")[1:-1]
            re = len(rep_pk)
            if re == 0:
                re = ""
            if str(pid) in like_list:
                lsign = 1
            if not p.comme == "None":
                posts.append([lsign, pid, p.contributor, p.comme, p.like, re])
    except:
        posts = []
        for p in rposts:
            pid = p.id
            lsign = 0
            replied = get_object_or_404(facul[0], pk=pid)
            rep = replied.reply
            rep_pk = rep.split(",")[1:-1]
            re = len(rep_pk)
            if re == 0:
                re = ""
            posts.append([lsign, pid, p.contributor, p.comme, p.like, re])


    pclas = clas.split("-")[0].strip(" ")
    prof = clas.split("-")[1].strip(" ")
    semes = clas.split("-")[2].strip(" ")
    date = str(localtime(timezone.now()))[:19]
    cps = [clas, pclas, prof, semes]
    contributor = request.user.username
    if not contributor:
        contributor = "unknown"
    defal1 = {
        "clas": clas, "prof": prof, "semes": semes,
        "reply" : "hoge,", "contributor": contributor,
        "date" : date, "comme" : "None"
    }
    defal2 = {
        "clas": clas, "prof": prof, "semes": semes,
        "reply" : "hoge,", "contributor": contributor, "date": date,
        "ease" : "★ 5", "aplus" : "★ 5", "fulfil" : "★ 5",
    }
    if request.method == "POST":
        form1 = modelform(request.POST, initial = defal1)
        form2 = modelform(request.POST, initial = defal2)

        if "form1" in request.POST:
            if form1.is_valid():
                post = form1.save(commit = False)
                post.save()
                make_csv(request, contributor, post, Facul)
                return redirect("detail", facul = facul[1], clas = post.clas, pk = post.pk)

        elif "form2" in request.POST:
            if form2.is_valid():
                post = form2.save(commit = False)
                post.ease = "None"
                post.aplus = "None"
                post.fulfil = "None"
                post.save()
                make_csv(request, contributor, post, Facul)
                return redirect("detail", facul = facul[1], clas=post.clas, pk=post.pk)
    else:
        form1 = modelform(initial = defal1)
        form2 = modelform(initial = defal2)

    sign = 0
    try:
        fav_class = mypage.fav_class
        fav_class_list = str(fav_class).split("$#&#$")
        if (facul[1] + "$@$" + clas) in fav_class_list:
            sign = 1
    except:
        pass

    class_data = {"info" : info, "sign" : sign, "cps" : cps}
    html = "class_info/class.html"
    arg = facul_argument(facul[1])
    return render(request, html, {
        "class_data" : class_data, "posts": posts, "form1": form1,
        "form2" : form2, "facul_argument": arg
    })


def class_detail(request, clas, pk, db, facul):
    detail = get_object_or_404(db, pk = pk)
    contributor = detail.contributor
    try:
        user = MyPage.objects.get(name = contributor)
        gender = user.gender
        grade = user.grade
        User = [gender, grade]
    except:
        User = []
    return render(request, "class_info/detail.html", {"detail" : detail, "facul" : facul, "user" : User})


def class_search(request, facul, modelform):
    clas = request.GET.get("clas")
    prof = request.GET.get("prof")

    if clas and prof:
        classes = []
        rclasses = facul[0].objects.filter(Q(clas__icontains = clas) & Q(prof__icontains = prof)).values("clas")
        for v in rclasses:
            if not v in classes:
                classes.append(v)
    elif clas:
        classes = facul[0].objects.filter(clas__icontains = clas).values("clas").distinct()
    elif prof:
        rprofs = facul[0].objects.filter(prof__icontains = prof).values("prof").distinct()
        classes = facul[0].objects.filter(prof__icontains =  rprofs).values("clas").distinct()
    else:
        return redirect("list", facul = facul[1])

    Facul = facul[1].upper()
    gpath = "csv/class_info/" + Facul + "/" + facul[1] + "_list.csv"
    gdf = pd.read_csv(gpath)
    sclasses = []
    for c in classes:
        c = list(c.values())
        for v in c:
            df = gdf[gdf["clas"] == v]
            info = percentage(df)
            for v in info:
                origin = v[0]
                w = v[0].split(" - ")
                w.append(origin)
                v[0] = w
                sclasses.append(v)

    contributor = request.user.username
    if not contributor:
        contributor = "unknown"
    date = str(localtime(timezone.now()))[:19]
    defal = {"reply" : "hoge,", "contributor": contributor, "date" : date}
    if request.method == "POST":
        form = modelform(request.POST, initial=defal)
        if form.is_valid():
            post = form.save(commit = False)
            post.clas = post.clas + " - " + post.prof + " - " + post.semes
            post.save()
            make_csv(request, contributor, post, Facul)
            return redirect("detail", facul = facul[1], clas = post.clas, pk = post.pk)
    else:
        form = modelform(initial = defal)
    query = [clas, prof]
    count = len(sclasses)
    result = {"query" :query, "count" : count, "classes" : sclasses, "form" : form}
    html = "class_info/result.html"
    arg = facul_argument(facul[1])
    return render(request, html, {"result" : result, "facul_argument" : arg})


def class_ranking(request, facul):
    Facul = facul[1].upper()
    gpath = "csv/class_info/" + Facul + "/" + facul[1] + "_list.csv"
    gdf = pd.read_csv(gpath)

    def no_data_yet(rlist, i):
        list = []
        for l in rlist:
            list.append(l)
        if i == 1:
            list = list[1:]
        else:
            list = list[:-1]
        while len(list) < 5:
            list.append(["NoDataYet", "NoDataYet"])
        return list

    ranks = [
        ["ease", "楽単", "難単", 7], ["aplus", "A以上", "B以下", 8],          ##  change name
        ["fulfil", "充実", "虚実", 9]
    ]
    ranking = []

    for rank in ranks:
        for i in range(2):
            box = []
            if i == 1:
                df = gdf.sort_values(rank[0]).head(5)
            else:
                df = gdf.sort_values(rank[0], ascending = False).head(5)
            for v in df.itertuples(name = None):
                box.append([v[3], v[rank[3]]])
            box = no_data_yet(box, i)
            box = [box]
            box.insert(0, rank[i + 1])
            ranking.append(box)

    html = "class_info/ranking.html"
    arg = facul_argument(facul[1])
    return render(request, html, {"ranking" : ranking, "facul_argument" : arg})





def reply(request, facul, clas, pk):
    db = facul_argument(facul)[0]
    replied = get_object_or_404(db, pk = pk)
    rep = replied.reply
    rep_pk = rep.split(",")[1:-1]
    rep_sum = len(rep_pk)
    rep_list = []

    contributor = request.user.username

    for id in rep_pk[::-1]:
        re = Reply.objects.filter(pk = id)[0]
        pid = re.id
        sign = 0
        try:
            mypage = MyPage.objects.get(name = contributor)
            re_like = mypage.re_like
            re_like_pk = re_like.split(",")[1:-1]
            if id in re_like_pk:
                sign = 1
        except:
            pass
        rep_list.append([pid, sign, re.re_comme, re.contributor, re.like, re.date[:11]])

    if not contributor:
        contributor = "unknown"
    date = str(localtime(timezone.now()))[:19]
    defal = {"contributor": contributor, "date": date}
    if request.method == "POST":
        form = ReplyForm(request.POST, initial = defal)
        if form.is_valid():
            post = form.save(commit = False)
            post.save()
            pid = post.id
            replied.reply = rep + str(pid) + ","
            replied.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ReplyForm(initial = defal)
    res = {
        "clas" : clas, "replied" : replied, "form" : form,
        "rep_sum" : rep_sum, "rep_list" : rep_list}
    return render(request, "class_info/reply.html", {"res" : res})



def lists(request, facul):
    arg = facul_argument(facul)[:2]
    return facul_list(request, arg)


def ranking(request, facul):
    arg = facul_argument(facul)[:2]
    return class_ranking(request, arg)


def search(request, facul):
    lis = facul_argument(facul)
    arg = lis[:2]
    modelform = lis[-1]
    return class_search(request, arg, modelform)


def clas(request, facul, clas):
    lis = facul_argument(facul)
    arg = lis[:2]
    modelform = lis[-1]
    return class_list(request, clas, arg, modelform)


def detail(request, facul, clas, pk):
    db = facul_argument(facul)[0]
    return class_detail(request, clas, pk, db, facul)