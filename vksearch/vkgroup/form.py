from django import forms

from .models import Community, AgeRange, Country, AudienceProfile


class CommunitiesSearchForm(forms.Form):
    countries = forms.ModelMultipleChoiceField(Country.objects.all(), required=False,
                                               widget=forms.CheckboxSelectMultiple())
    age_ranges = forms.ModelMultipleChoiceField(AgeRange.objects.all(), required=False,
                                                widget=forms.CheckboxSelectMultiple())
    sexes = forms.MultipleChoiceField(AudienceProfile.SEX_CHOICES, required=False,
                                      widget=forms.CheckboxSelectMultiple())

    min_sex_perc = forms.IntegerField(required=False, min_value=0, max_value=100, label='Min sex%')
    max_sex_perc = forms.IntegerField(required=False, min_value=0, max_value=100, label='Max sex%')

    min_members = forms.IntegerField(required=False, min_value=0, label='Min members')
    max_members = forms.IntegerField(required=False, min_value=0, label='Max members')

    min_audience = forms.IntegerField(required=False, min_value=0, label='Min audience')
    max_audience = forms.IntegerField(required=False, min_value=0, label='Max audience')

    min_audience_perc = forms.IntegerField(required=False, min_value=0, max_value=100, label='Min audience %')
    max_audience_perc = forms.IntegerField(required=False, min_value=0, max_value=100, label='Max audience %')


    ordering = forms.ChoiceField(Community.profile_objects.ORDERING_CHOICES)
    inverted = forms.BooleanField(required=False)


