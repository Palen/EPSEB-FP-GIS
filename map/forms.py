# -*- coding: utf-8 -*-
from django.contrib.gis import forms
from models import JobType, Teacher, CHOICES_SRID, Region, City, Province


class JobForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    s_first_name = forms.CharField(required=False)
    s_last_name = forms.CharField(required=False)
    title = forms.CharField()
    url = forms.URLField()
    desc = forms.CharField(widget=forms.Textarea(attrs={'cols': 25, 'rows': 5}))
    teachers = forms.ModelMultipleChoiceField(queryset=Teacher.objects.all(), required=True)
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    srid = forms.ChoiceField(choices=CHOICES_SRID)
    latitude = forms.DecimalField(label="Latitude (y)", help_text='It can be in Geographic or UTM', max_digits=10)
    longitude = forms.DecimalField(label='Longitude(x)', help_text='It can be in Geographic or UTM', max_digits=10)
    date = forms.CharField(help_text="Only year and month, with this structure 2014-01 ")
    image = forms.ImageField(required=False)

    teachers.help_text = 'Pressing cntrl you can select more than one'




class FilterForm(forms.Form):
    region_name = forms.ModelMultipleChoiceField(queryset=Region.objects.all(), required=False, label='Region', initial=None)
    province_name = forms.ModelMultipleChoiceField(queryset=Province.objects.all(), required=False, label='Province', initial=None)
    city_name = forms.ModelMultipleChoiceField(queryset=City.objects.all(), required=False, label='City', initial=None)
    region_name.empty_label = province_name.empty_label = city_name.empty_label = None







