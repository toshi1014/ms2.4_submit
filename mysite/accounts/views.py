from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from .forms import UserCreateForm, LoginForm, MyPageForm
from django.contrib.auth.decorators import login_required
from class_info.models import Reply, SK, SY, HO, SG, KY, KO, BU, BK, KI, SO, SE, SP, JK, GE
from .models import MyPage
from django.http import HttpResponseRedirect
import pandas as pd
import class_info.views as class_views


class Index(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = User.objects.get(username = username)
            login(request, user)
            return redirect("mypage")
        form = UserCreateForm(data = request.POST)
        return render(request, "accounts/signup.html", {"form" : form})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, "accounts/index.html", {"form" : form})


class Signup(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data = request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect("init_mypage")
        return render(request, "accounts/signup.html", {"form" : form})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, "accounts/signup.html", {"form" : form})


class Logout(LoginRequiredMixin, LogoutView):
    template_name = "accounts/index.html"



faculs = [
    [SK, "sk"], [SY, "sy"], [HO, "ho"], [SG, "sg"], [KY, "ky"], [KO, "ko"],
    [BU, "bu"], [BK, "bk"], [KI, "ki"], [SO, "so"], [SE, "se"], [SP, "sp"],
    [JK, "jk"], [GE, "ge"]
    ]


def facul_db(facul):
    for fac in faculs:
        if fac[1] == facul:
            return fac[0]


@login_required()
def init_mypage(request):
    name = request.user.username
    defal = {"name": name, "fav_class": "hoge$#&#$", "like" : "hoge,", "re_like" : "hoge,"}
    if request.method == "POST":
        form = MyPageForm(request.POST, initial = defal)
        if form.is_valid():
            form.save()
            return redirect("mypage")
    else:
        form = MyPageForm(initial = defal)
    return render(request, "accounts/init_mypage.html", {"form" : form})


@login_required()
def reinit_mypage(request):
    name = request.user.username
    defal = {"name": name, "fav_class": "hoge$#&#$", "like" : "hoge,", "re_like" : "hoge,"}
    if request.method == "POST":
        form = MyPageForm(request.POST, initial = defal)
        if form.is_valid():
            form.save()
            return redirect("mypage")
    else:
        form = MyPageForm(initial = defal)
    return render(request, "accounts/reinit_mypage.html", {"form" : form})


def mypage_validation(name):
    try:
        return MyPage.objects.get(name = name)
    except:
        return 0


@login_required()
def mypage(request):
    fav_classes = MyPage.objects.filter(name = request.user.username).values("fav_class")
    fav_class = []
    for rclas in fav_classes:
        clas = rclas.get("fav_class")
    try:
        for c in clas.split("$#&#$")[1:-1]:
            clist = c.split("$@$")
            fav_class.append(clist)
    except:
        return redirect("reinit_mypage")

    res = {"fav_class" : fav_class}
    return render(request, "class_info/mypage.html", {"res" : res})


def comment_list(request, name):
    comments = []
    for facul in faculs:
        rcomments = facul[0].objects.filter(contributor = name)
        comment = []
        for rcomment in rcomments:
            if not rcomment.comme == "None":
                comment.append([rcomment.clas, rcomment.comme, rcomment.id])
        arg = class_views.facul_argument(facul[1])
        box = [len(comment), arg]
        box.append(comment)
        comments.append(box)

    res = {"name" : name, "comments" : comments}
    return render(request, "class_info/comment_list.html", {"res" : res})


@login_required()
def add_fav_class(request, clas, facul, sign):
    mypage = mypage_validation(request.user.username)
    if mypage == 0:
        return redirect("reinit_mypage")
    fav_class = mypage.fav_class
    if sign == 0:
        mypage.fav_class = fav_class + facul + "$@$" +clas + "$#&#$"
        mypage.save()
    else:
        rfav_class_list = str(fav_class).split("$#&#$")
        fav_class_list = []
        for v in rfav_class_list:
            if not v == (facul + "$@$" + clas):
                fav_class_list.append(v)
        mypage.fav_class = ("$#&#$").join(fav_class_list)
        mypage.save()
    return redirect("/class/class_info/" + facul + "/" + clas + "/")


@login_required()
def add_like(request, facul, pk, sign):
    mypage = mypage_validation(request.user.username)
    if mypage == 0:
        return redirect("init_mypage")
    like = mypage.like
    db = facul_db(facul)
    post = db.objects.filter(pk = pk)
    dblike = db.objects.get(pk = pk)
    for p in post:
        clas = p.clas
        date = str(p.date)
    path = "csv/class_info/" + facul.upper() + "/" + clas + ".csv"
    df = pd.read_csv(path)
    columns = [
        "index", "date", "semes", "prof", "ease", "aplus", "fulfil",
        "comme", "contributor", "gender", "grade", "like"
    ]
    df = df[columns]
    if sign == 0:
        mypage.like = like + str(pk) + ","
        mypage.save()
        sum_like = int(df[df["date"] == date]["like"])
        sum_like += 1
        idx = int(df.loc[df["date"] == date].index.values)
        df.loc[idx, "like"] = sum_like
        df.to_csv(path)
        dblike.like = sum_like
        dblike.save()
    else:
        rlike_list = str(like).split(",")
        like_list = []
        for v in rlike_list:
            if not v == str(pk):
                like_list.append(v)
        mypage.like = (",").join(like_list)
        mypage.save()
        sum_like = int(df[df["date"] == date]["like"])
        sum_like -= 1
        idx = int(df.loc[df["date"] == date].index.values)
        df.loc[idx, "like"] = sum_like
        df.to_csv(path)
        dblike.like = sum_like
        dblike.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def add_re_like(request, pk, sign):
    mypage = mypage_validation(request.user.username)
    if mypage == 0:
        return redirect("init_mypage")
    re_like = mypage.re_like
    if sign == 1:
        rre_like_pk = re_like.split(",")
        re_like_pk = []
        for re in rre_like_pk:
            if not re == str(pk):
                re_like_pk.append(re)
        mypage.re_like = (",").join(re_like_pk)
        mypage.save()
        reply = Reply.objects.get(id=pk)
        reply.like -= 1
        reply.save()
    else:
        mypage.re_like = re_like + str(pk) + ","
        mypage.save()
        reply = Reply.objects.get(id = pk)
        reply.like += 1
        reply.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))