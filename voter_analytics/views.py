from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.functions import ExtractYear
from django.db.models import Count
from .models import Voter
import plotly
from plotly import offline
import plotly.graph_objects as go

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

class GraphListView(ListView):
    '''Display a voters graphs on it's own page.'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = "v"

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

    # implement some methods... 
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # get the superclass version of context
        context = super().get_context_data(**kwargs)

        # gets filtered query set
        qs = self.get_queryset()

        # get the counts for each year, and order it by the year
        # note: this is a dictionary
        year_counts = qs.annotate(year=ExtractYear('dob')).values('year').annotate(count=Count('id')).order_by('year')

        # get total count
        total = 0
        # separate data into x and y lists
        x = [str(item['year']) for item in year_counts]  
        y = []
        for item in year_counts:
            total += item['count']
            y += [item['count']]

        # create the bar chart
        fig = go.Figure(data=[go.Bar(x=x, y=y)])
        fig.update_layout(title=f'Voter distribution by Year of Birth (n={total})',
                          xaxis_title='Year of DOB',
                          yaxis_title='Count of Voters')

        # generate HTML div for the plot and add it to context
        bar_div = offline.plot(fig, 
                               auto_open=False, 
                               output_type='div')
        context['bar_div'] = bar_div

        # get labels and values for pie chart
        party_counts = qs.values('party').annotate(count=Count('id')).order_by('party')

        # separate into labels and values
        labels = [str(item['party']) for item in party_counts]
        values = [item['count'] for item in party_counts]

        # create pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title=f'Voter distribution by Party Affiliation (n={total})')
        
        pie_div = offline.plot(fig,
                                auto_open=False,
                                output_type='div')
        
        # add the pie chart to the context
        context['pie_div'] = pie_div

        # get labels and counts for histogram
        labels = ['v20state']
        labels += ['v21town']
        labels += ['v20primary']
        labels += ['v22general']
        labels += ['v23town']

        counts = [0,0,0,0,0]
        counts[0] = qs.filter(v20state="TRUE").count()
        counts[1] = qs.filter(v21town="TRUE").count()
        counts[2] = qs.filter(v20primary="TRUE").count()
        counts[3] = qs.filter(v22general="TRUE").count()
        counts[4] = qs.filter(v23town="TRUE").count()

        # create second bar chart
        fig = go.Figure(data=[go.Bar(x=labels, y=counts)])
        fig.update_layout(title=f'Vote Count by Election (n={total})',
                          xaxis_title='Vote Count',
                          yaxis_title='Election')
        
        bar2_div = offline.plot(fig,
                                auto_open=False,
                                output_type='div')
        
        # add the pie chart to the context
        context['bar2_div'] = bar2_div

        return context