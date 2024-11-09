from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

# Create your views here.
class VotersListView(ListView):
    '''View to show a list of voters '''

    template_name = 'voter_analytics/results.html'
    model = Voter
    context_object_name = 'results'
    paginate_by = 50 # show 50 results per page

    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the results to a small number of records'''

        # default query set is all of the records:
        qs = super().get_queryset()
        # return qs[:25] # limit to 25 records
        
        # handle search form/URL parameters:
        if 'party' in self.request.GET:

            party = self.request.GET['party']
            # filter results by party
            qs = Voter.objects.filter(party__icontains=party)

        return qs