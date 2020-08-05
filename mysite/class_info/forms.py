from django import forms
from .models import Reply, SK, SY, HO, SG, KY, KO, BU, BK, KI, SO, SE, SP, JK, GE

field = (
            "clas", "semes", "prof", "ease", "aplus", "fulfil",
            "comme", "reply", "contributor", "like", "date"
)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ("re_comme", "contributor", "like", "date")


class SKForm(forms.ModelForm):
    class Meta:
        model = SK
        fields = field


class SYForm(forms.ModelForm):
    class Meta:
        model = SY
        fields = field


class HOForm(forms.ModelForm):
    class Meta:
        model = HO
        fields = field


class SGForm(forms.ModelForm):
    class Meta:
        model = SG
        fields = field


class KYForm(forms.ModelForm):
    class Meta:
        model = KY
        fields = field


class KOForm(forms.ModelForm):
    class Meta:
        model = KO
        fields = field


class BUForm(forms.ModelForm):
    class Meta:
        model = BU
        fields = field


class BKForm(forms.ModelForm):
    class Meta:
        model = BK
        fields = field


class KIForm(forms.ModelForm):
    class Meta:
        model = KI
        fields = field


class SOForm(forms.ModelForm):
    class Meta:
        model = SO
        fields = field


class SEForm(forms.ModelForm):
    class Meta:
        model = SE
        fields = field


class SPForm(forms.ModelForm):
    class Meta:
        model = SP
        fields = field


class JKForm(forms.ModelForm):
    class Meta:
        model = JK
        fields = field


class GEForm(forms.ModelForm):
    class Meta:
        model = GE
        fields = field