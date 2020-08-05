from django.db import models


class Reply(models.Model):
    re_comme = models.TextField(null=True, verbose_name="")
    contributor = models.TextField(null=True, verbose_name="投稿者")
    like = models.IntegerField(null=True, default=0)
    date = models.TextField(null=True)

    def __str__(self):
        return self.re_comme + " / " + self.contributor


sem = (
    ("通年", "通年"),
    ("春夏", "春夏"),
    ("春クオーター", "春クオーター"),
    ("夏クォーター", "夏クォーター"),
    ("秋冬", "秋冬"),
    ("秋クォータ", "秋クォータ"),
    ("冬クォーター", "冬クォーター")
)
star = (
    ("★ 5", "★ 5"),
    ("★ 4", "★ 4"),
    ("★ 3", "★ 3"),
    ("★ 2", "★ 2"),
    ("★ 1", "★ 1")
)

class Define(models.Model):
    clas = models.CharField(max_length=25, verbose_name="科目")
    semes = models.TextField(choices=sem, null=True, verbose_name="学期")
    prof = models.CharField(max_length=25, default="", verbose_name="先生")
    ease = models.TextField(choices=star, null=True, verbose_name="楽単度")
    aplus = models.TextField(choices=star, null=True, verbose_name="評価A以上")
    fulfil = models.TextField(choices=star, null=True, verbose_name="内容")
    comme = models.TextField(null=True, verbose_name="")
    reply = models.TextField(null=True)
    contributor = models.TextField(null=True, verbose_name="投稿者")
    like = models.IntegerField(null=True, default=0)
    date = models.TextField(null=True)

    def __str__(self):
        return self.clas + " / " + self.contributor + " / " + self.comme

    class Meta:
        abstract = True


class SK(Define):
    pass


class SY(Define):
    pass


class HO(Define):
    pass


class SG(Define):
    pass


class KY(Define):
    pass


class KO(Define):
    pass


class BU(Define):
    pass


class BK(Define):
    pass


class KI(Define):
    pass


class SO(Define):
    pass


class SE(Define):
    pass


class SP(Define):
    pass


class JK(Define):
    pass


class GE(Define):
    pass