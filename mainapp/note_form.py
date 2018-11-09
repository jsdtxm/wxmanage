from django import forms
from mainapp.models import Team

class Note_form(forms.Form):
    source_type={
        ("journal", "期刊" ),
        ("rich", "硕博" ),
        ("meeting", "会议" ),
        ("newspaper", "报纸" ),
        ("yearbook", "年鉴" ),
        ("patent", "专利" ),
        ("stand", "标准" ),
        ("achievements", "成果" ),
        ("other", "其他" ),
    }
    upfile = forms.FileField()
    title = forms.CharField(
        label='标题',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"在此处键入标题..."})
    )
    authors = forms.CharField(
        label='作者',
        max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"在此处键入作者..."})
    )
    source =  forms.CharField(
        label='来源',
        max_length=256,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"在此处键入文献来源..."})
    )
    source_select = forms.ChoiceField(
        choices=source_type,
        widget=forms.widgets.Select(attrs={'class': 'form-control'})
    )
    institution = forms.CharField(
        label='机构',
        max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"在此处键入机构名称..."})
    )
    sore_year = forms.IntegerField(
        label='发表年度',
        max_value=2200,
        min_value=1800,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"2018..."})
    )
    abstract = forms.CharField(
        label='摘要',
        widget=forms.Textarea(attrs={'class': 'form-control','placeholder':"在此处键入摘要...","cols":"40","rows":"6"})
    )
    keywords = forms.CharField(
        label='关键词',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"在此处键入关键词..."})
    )
    doi = forms.CharField(
        label='doi',
        max_length=256,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"在此处键入数字对象唯一标识符..."})
    )
    team_choice=forms.ChoiceField(
        choices=Team.objects.all().values_list("id","name"),
        widget=forms.widgets.Select(attrs={'class': 'form-control'}),
    )