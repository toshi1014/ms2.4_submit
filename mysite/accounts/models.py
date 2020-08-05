from django.db import models


class MyPage(models.Model):

    gen = (
        ("male", "male"),
        ("female", "female")
    )

    gra = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4")
    )

    name = models.TextField(null=True)
    gender = models.TextField(choices = gen, null = True)
    grade = models.TextField(choices = gra, null = True)
    fav_class = models.TextField(null = True)
    like = models.TextField(null = True)
    re_like = models.TextField(null=True)

    def __str__(self):
        return self.name