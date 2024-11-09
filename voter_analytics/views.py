from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

# Create your views here.
class VotersListView(ListView):
    '''View to show a list of voters '''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100 # show 50 results per page

    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the results to a small number of records'''

        # default query set is all of the records:
        qs = super().get_queryset()

        # handle search form/URL parameters:
        if 'party' in self.request.GET:

            party = self.request.GET['party']
            # filter results by party
            qs = qs.filter(party__icontains=party)

        if 'min_dob' in self.request.GET:

            min_dob = int(self.request.GET['min_dob'])
            # filter results by >= min dob
            qs = qs.filter(dob__year__gte=min_dob)

        if 'max_dob' in self.request.GET:

            max_dob = int(self.request.GET['max_dob'])
            # filter results by <= max dob
            qs = qs.filter(dob__year__lte=max_dob)
        
        if 'voter_score' in self.request.GET:

            voter_score = self.request.GET['voter_score']
            # filter results by voter score
            qs = qs.filter(voter_score=voter_score)
        
        if 'v20state' in self.request.GET:

            voted = self.request.GET['v20state'] # always TRUE
            # filter results by whether they voted for this election
            qs = qs.filter(v20state=voted)
        
        if 'v21town' in self.request.GET:

            voted = self.request.GET['v21town'] # always TRUE
            # filter results by whether they voted for this election
            qs = qs.filter(v21town=voted)

        if 'v20primary' in self.request.GET:

            voted = self.request.GET['v20primary'] # always TRUE
            # filter results by whether they voted for this election
            qs = qs.filter(v20primary=voted)
        
        if 'v22general' in self.request.GET:

            voted = self.request.GET['v22general'] # always TRUE
            # filter results by whether they voted for this election
            qs = qs.filter(v22general=voted)
        
        if 'v23town' in self.request.GET:

            voted = self.request.GET['v23town'] # always TRUE
            # filter results by whether they voted for this election
            qs = qs.filter(v23town=voted)

        return qs

class VoterDetailView(DetailView):
    '''Display a single Voter on it's own page.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = "v"