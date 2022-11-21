from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Community
from .forms import CommunitiesSearchForm

from .tasks import check_for_update_data_from_vk

import logging

logger = logging.getLogger(__name__)

COMMUNITIES_PER_PAGE = 30
COMMUNITIES_LIMIT = 5 * COMMUNITIES_PER_PAGE


@require_GET
def communities_view(request):
    check_for_update_data_from_vk()
    context = {
        'title': 'Result',
    }
    form = CommunitiesSearchForm(request.GET)
    if form.is_valid():
        communities = Community.profile_objects.select(
            form.cleaned_data['countries'],
            form.cleaned_data['age_ranges'],
            form.cleaned_data['sexes'],
            form.cleaned_data['min_members'], form.cleaned_data['max_members'],
            form.cleaned_data['min_sex_perc'], form.cleaned_data['max_sex_perc'],
            form.cleaned_data['min_audience'], form.cleaned_data['max_audience'],
            form.cleaned_data['min_audience_perc'], form.cleaned_data['max_audience_perc'],
            form.cleaned_data['ordering'],
            form.cleaned_data['inverted']
        )[:COMMUNITIES_LIMIT]
        paginator = Paginator(communities, COMMUNITIES_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        try:
            communities= page_obj
        except PageNotAnInteger:
            communities = paginator.get_page(1)
        except EmptyPage:
            communities = paginator.get_page(paginator.num_pages)
    else:
        communities = []
    context['form'] = form
    context['communities'] = communities

    return render(request, 'communities.html', context)
