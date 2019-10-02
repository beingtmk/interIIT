# Importing necessary functions
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.edit import DeleteView
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,ListView,DetailView
from django.db import models
from django.contrib.auth import authenticate, login, logout

from django_tables2 import RequestConfig
from .tables import *

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from itertools import groupby

from django.forms import formset_factory

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.db.models import Count
from django_tables2.export.export import TableExport
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
from django.apps import apps
from django.db.models.functions import TruncDate

# For Emailing
import requests
from django.template.loader import render_to_string

match_type1 = ['athletics','weight_lifting','swimming' ]
match_type2 = ['badminton', 'basketball', 'cricket', 'football', 'hockey', 'squash', 'tennis', 'table_tennis', 'volleyball']

model_type1 ={
    'athletics': Athletics,
    'weight_lifting': WeightLifting,
    'swimming': Swimming,
}

model_type2 = {
    'badminton':Badminton,
    'basketball':Basketball,
    'cricket':Cricket,
    'football':Football,
    'hockey':Hockey,
    'squash':Squash,
    'tennis':Tennis,
    'table_tennis':TableTennis,
    'volleyball':Volleyball,
    'water_polo':WaterPolo,
}

playermatches = [PlayerAthletics,PlayerWeightLifting,PlayerSwimming]

def Send(to,subject,file,data={},sender="noreply@interiit.com",name="Inter IIT Sport Meet 2018",cc=[],bcc=[]):

    content = render_to_string(file,data)
    return requests.post(
        "https://api.mailgun.net/v3/interiit.com/messages",
        auth=("api", "3d4d20f017c53969b3a93edfca5b2ed1-bd350f28-f551fa7d"),
        data={"from": name+" <"+sender+">",
            "to": to,
            "cc": cc,
            "bcc": bcc,
            "subject": subject,
            "h:Reply-To": "rohan.aggarwal@iitg.ac.in",
            "html": content})

## index for the website
class IndexView(generic.ListView):
    template_name = 'Schedule/index.html'
    context_object_name = 'latest_sport_list'

    def get_queryset(self):
        return Event.objects.values_list('sport', flat=True).order_by('sport').distinct


## index of the Schedule app
class ScheduleIndexView(generic.ListView):
    template_name = 'Schedule/schedule_index.html'
    context_object_name = 'latest_sport_list'

    def get_queryset(self):
        return Event.objects.values_list('sport', flat=True).order_by('sport').distinct


## ADMIN Permission Check

def is_admin(user_id):
    print(user_id)
    profile = Profile.objects.filter(user=user_id)[0]
    if profile.user_type == 'ADMIN':
        return True
    else:
        print('not authorised')
        return False
######################### --------- Player and Staff Portal Views ------------------ #####################

## Registration Views :
class StaffCreateView(CreateView):
    Model = Staff
    template_name = 'Schedule/generic/forms/registration/staff_registration_form.html'
    form_class = StaffCreate
    success_url = reverse_lazy('reaching')

## Registration Wizard :
class RegistrationWizard(SessionWizardView):

    trivia = Trivia.objects.all()
    questions_count = trivia.count()
    print(questions_count)
    error = 0

    TriviaFormSet = formset_factory(TriviaForm, extra=questions_count)
    form_list = [PlayerCreate, TriviaFormSet, ConfirmationForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'SportsMeet'))

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/registration/registration_form.html",
                    "1": "Schedule/generic/forms/registration/trivia_form.html",
                    "2": "Schedule/generic/forms/registration/confirmation.html",
                    }

        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(RegistrationWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.current == '0':
            if self.error == 1:
                context['error'] = '* Registered Events are more that allowed Number *'
            elif self.error == 2:
                context['error'] = '* Some of the events your registered are not available for your gender *'

        elif self.steps.current == '1':
            context['trivia'] = Trivia.objects.all()

        elif self.steps.current == '2':
            context['data'] = self.get_cleaned_data_for_step('0')
            context['trivia'] = Trivia.objects.all()
            context['answers'] = self.get_cleaned_data_for_step('1')


        return context

    def done(self, form_list, form_dict, **kwargs):

        # Validating Data
        player_data = form_dict['0']

        events = player_data.cleaned_data['event']
        category = player_data.cleaned_data['category']
        print(events)

        restrictions_relay = 2
        restrictions_other = 3

        count_relay = {}
        count_other = {}

        sports = [  'athletics',
                    'badminton',
                    'basketball',
                    'cricket',
                    'football',
                    'hockey',
                    'squash',
                    'tennis',
                    'table_tennis',
                    'volleyball',
                    'weight_lifting',
                    'water_polo',
                    'swimming',
                    ]

        for index, sport in enumerate(sports):
            count_relay[sport] = 0
            count_other[sport] = 0


        for event in events:
            if(event.is_men and category=='MEN'):
                pass
            elif(event.is_women and category=='WOMEN'):
                pass
            else:
                self.error = 2
                return self.render_goto_step('0')

            if(event.is_relay):
                count_relay[event.sport] += 1
            else:
                count_other[event.sport] += 1

        for index, sport in enumerate(sports):
            if(count_relay[sport] > restrictions_relay or count_other[sport] > restrictions_other):
                self.error = 1
                return self.render_goto_step('0')

        # Send(to,subject,file,data={},sender="noreply@interiit.com",name="Inter IIT Sport Meet 2018",cc=[],bcc=[])


        # Saving Data
        player = form_dict['0'].save()
        form_1 = form_dict['1']

        for idx,form in enumerate(form_1):
            try:
                answer = form.cleaned_data['answer']
            except KeyError:
                answer = ''
            trivia = Trivia.objects.all()[idx]
            Answer(player=player, answer=answer, trivia=trivia).save()
            # print(player.id)

        resp = Send(player.email, "Registration Successful", "Schedule/registration_mail.html",data={'heading':'Registration Successful','name':player.name,'events':events,"approved":player.approved_status})
        return redirect('reaching')
        # return HttpResponse(str(resp.content))

## Registration Views :
class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    template_name = 'Schedule/generic/forms/registration/update_form.html'
    form_class = PlayerCreate
    success_url = reverse_lazy('player_list_staff', kwargs = {'sport' : 'athletics'})

    def form_valid(self, form):

        events = form.cleaned_data['event']
        category = form.cleaned_data['category']
        print(events)


        restrictions_relay = 2
        restrictions_other = 3

        count_relay = {}
        count_other = {}

        sports = [  'athletics',
                    'badminton',
                    'basketball',
                    'cricket',
                    'football',
                    'hockey',
                    'squash',
                    'tennis',
                    'table_tennis',
                    'volleyball',
                    'weight_lifting',
                    'water_polo',
                    'swimming',
                    ]

        for index, sport in enumerate(sports):
            count_relay[sport] = 0
            count_other[sport] = 0

        for event in events:
            if(event.is_men and category=='MEN'):
                pass
            elif(event.is_women and category=='WOMEN'):
                pass
            else:
                form.add_error(None, "Your Gender is not allowed to register for the selected event")
                return super().form_invalid(form)

            if(event.is_relay):
                count_relay[event.sport] += 1
            else:
                count_other[event.sport] += 1

        for index, sport in enumerate(sports):
            if(count_relay[sport] > restrictions_relay or count_other[sport] > restrictions_other):
                form.add_error(None, "Registered events count is more than allowed")
                return super().form_invalid(form)

        approved_status = Player.objects.filter(id=int(self.kwargs['pk'])).first().approved_status
        resp = Send(str(form.cleaned_data['email']), "Registration Details Updated", "Schedule/registration_mail.html",data={'heading':'Registration Details Updated','name':str(form.cleaned_data['name']),'events':events,"approved":approved_status})
        return super().form_valid(form)

# Player DeleteView
class PlayerDeleteView(LoginRequiredMixin, DeleteView):
    model = Player
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('index')

from dal import autocomplete

class EventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Event.objects.all().exclude(sport__in = ['swimming', 'water_polo'])

        if self.q:
            qs = qs.filter(sport__icontains=self.q) | qs.filter(event__icontains=self.q)
        return qs

# Player List
@login_required
def PlayerListView(request):

    # Admin Check
    user = request.user
    if not is_admin(user.id):
        return redirect('unauthorised')

    queryset = Player.objects.all().exclude(event__sport__in = ['swimming', 'water_polo'])
    table = PlayerTable(queryset)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'Schedule/registration/player_list_table.html', {'table': table})

# Player List
@login_required
def StaffListView(request):

    # Admin Check
    user = request.user
    if not is_admin(user.id):
        return redirect('unauthorised')

    queryset = Staff.objects.all().exclude(sport__in = ['swimming', 'water_polo'])
    table = StaffTable(queryset)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))


    return render(request, 'Schedule/registration/staff_list_table.html', {'table': table})

# Player Search
@login_required
def player_filter(request):

    # Admin Check
    user = request.user
    if not is_admin(user.id):
        return redirect('unauthorised')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerFilter(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            sports = form.cleaned_data['sport']
            team = form.cleaned_data['team']

            print(sports)

            # Get queryset
            players = Player.objects.filter( event__sport__in = sports, team=team).distinct()
            events = Event.objects.filter( sport__in = sports,)


            # Count for different fields
            print(len(players))

            fieldname = 'food'
            count_food = players.values(fieldname).order_by(fieldname).annotate(count=Count(fieldname))

            fieldname = 'category'
            count_category = players.values(fieldname).order_by(fieldname).annotate(count=Count(fieldname))

            fieldname = 'blood_group'
            count_blood = players.values(fieldname).order_by(fieldname).annotate(count=Count(fieldname))

            context = {'players':players,
                'events': events,
                'count_food' : count_food,
                'count_blood' : count_blood,
                'count_category' : count_category,
                'sports' : 'sports',
                'team' : 'team'
                }

            return render(request, 'Schedule/generic/sports/players.html', context)
        else:
            return HttpResponse('Error!')
            # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerFilter()
        return render(request, 'Schedule/generic/forms/player_filter.html', {'form':form})

## Forms for college Staff

# list of sports
class SportView(generic.ListView):
    template_name = 'Schedule/registration/sport_list.html'
    context_object_name = 'latest_sport_list'

    def get_queryset(self):
        return Event.objects.values_list('sport', flat=True).distinct

# list of players
class Players_Sports(LoginRequiredMixin, generic.ListView):
    context_object_name = 'data'
    template_name = 'Schedule/registration/player_list.html'

    def get_queryset(self):
        current_user = self.request.user
        staff_iit = Profile.objects.get(user=current_user).college
        # self.kwargs['sport'] = self.kwargs['sport'].replace('_', ' ')
        sports = Event.objects.filter(sport=self.kwargs['sport'])
        player_list = Player.objects.filter(team=staff_iit, event__in=sports).distinct().order_by('approved_status')
        return { 'players': player_list, 'sport': self.kwargs['sport'].replace(' ', '_') }


@login_required
def approve_toggle(request, pk):
    current_user = request.user
    staff_profile = Profile.objects.get(user=current_user)

    player = Player.objects.get(pk=pk)

    if(player.team == staff_profile.college or staff_profile.user_type == 'ADMIN'):
        # Toggle
        player.approved_status = not player.approved_status
        player.save()
        resp = Send(player.email, "Approval Updated", "Schedule/registration_mail.html",data={'heading':'Approval Updated','name':player.name,'events':player.event.all,"approved":player.approved_status})
        # Send("Approval Updated", "noreply@interiit.com", "HEXA", "apurva9@iitg.ac.in", "<h1>Important Text Message</h1>", "Important Testing Email", True)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'Schedule/generic/unauthorised.html')


## Player Profile
class PlayerProfile(DetailView):
    model = Player
    context_object_name = "player"
    template_name = 'Schedule/player_profile.html'

def playerview(request,pk):
    player = Player.objects.filter(id=pk).first()
    images = player.images.all()
    gold = 0
    silver = 0
    bronze = 0
    for x in playermatches:
        gold += x.objects.filter(player=player,medal="GOLD").count()
        silver += x.objects.filter(player=player,medal="SILVER").count()
        bronze += x.objects.filter(player=player,medal="BRONZE").count()

    match = []
    for _match in match_type2:
        all_players = Player.objects.filter(event__sport__contains = _match)
        if player in all_players:
            query = model_type2[_match].objects.filter(team1=player.team)|WaterPolo.objects.filter(team2=player.team).order_by('-date', '-time', '-event__event')
            match.append(query)

    try:
        answers = Answer.objects.filter(player=player).all()
    except Answer.DoesNotExist:
        answers = None

    matches = {"matches":match,"all_players":all_players}
    return render(request,'Schedule/player_profile.html',{"player":player,"answers":answers,"images":images,"gold":gold,"silver":silver,"bronze":bronze,"matches":matches})

## Player Search
def search(request):

    iits = Team.objects.values_list('college', flat=True).order_by('college')
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct

    if request.method == "GET":

        players = Player.objects.filter(approved_status=True).order_by("pk")
        page = request.GET.get('page', 1)

        paginator = Paginator(players, 20)
        try:
            players = paginator.page(page)
        except PageNotAnInteger:
            players = paginator.page(1)
        except EmptyPage:
            players = paginator.page(paginator.num_pages)

        context = {
                    'players': players,
                    'iits' : iits,
                    'sports' : sports,
                }

        return render(request, 'Schedule/players.html', context)

    else:
        name = request.POST.get('name')
        iit = request.POST.get('iit')
        sport = request.POST.get('sport')

        print(sport)
        print(iit)
        print(name)
        if iit == None and sport == None:
            if name == None:
                players = Player.objects.all()
            else:
                players = Player.objects.filter(name__icontains = name, approved_status=True).distinct
        elif iit == "ALL IIT's" and sport == "All Sports":
            print("1")
            players = Player.objects.filter(name__icontains = name, approved_status=True).distinct
        elif iit == "ALL IIT's" :
            print("2")
            players = Player.objects.filter(name__icontains = name, event__sport__contains = sport, approved_status=True).distinct
        elif sport == "All Sports":
            print("3")
            players = Player.objects.filter(name__icontains = name, team__college__icontains = iit, approved_status=True).distinct
        else :
            print("4")
            players = Player.objects.filter(name__icontains = name, team__college__icontains = iit, event__sport__contains = sport, approved_status=True).distinct
        context = {
                    'players': players,
                    'iits' : iits,
                    'sports' : sports,
                }
        return render(request, 'Schedule/players.html', context)

############################ --------- End Player Portal Views ------------------ #################


##############################################################################################
############################ --------- Match Views ------------------ #######################

############################ --------- Athletics------------------ #######################

# Schedule page
class AthleticsView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Athletics.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = AthleticsScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time','-event__event', '-category'), "sport": "athletics",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Athletics
class AthleticsScoreCreate(CreateView):
    model = AthleticsScore
    fields = '__all__'
    success_url = reverse_lazy('athletics')

#Form to update an entry for Athletics
class AthleticsScoreTableUpdate(UpdateView):
    model = AthleticsScore
    fields = '__all__'
    success_url = reverse_lazy('athletics')


# Points table
class AthleticsScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/athletics/athletics_score.html'
    queryset = AthleticsScore.objects.all()

    def get_queryset(self):
        return AthleticsScore.objects.all().order_by('-points')

## Form: Adding Match
class AthleticsWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [AthleticsCreate, PlayerAdd]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):
        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')

            return {
                'queryset' : Player.objects.filter(event=event, category=category, approved_status=True),
            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        # requests.post(url, data={djangoID})

        players = form_1.cleaned_data['players']

        for player in players:
            PlayerAthletics(player=Player.objects.get(pk=player.pk),
                            athletics = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class AthleticsDeleteView(LoginRequiredMixin, DeleteView):
    model = Athletics
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('athletics')

# Form: Updating Match Info
class AthleticsUpdate(LoginRequiredMixin, UpdateView):
    model = Athletics
    template_name = 'Schedule/sports/athletics/forms/athletics_update_form.html'
    # success_url = reverse_lazy('index')

    form_class = AthleticsUpdate

    def get_form_kwargs(self):

        kwargs = super(AthleticsUpdate, self).get_form_kwargs()
        kwargs['sport'] = "athletics"
        return kwargs

    def get_success_url(self):
        return reverse('playeradd_athletics', kwargs={'pk':self.kwargs['pk']})

def PlayerAthleticsDelete(request,pk):
    p = PlayerAthletics.objects.get(pk=pk)
    p.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/match/sports'))


def playeradd_athletics(request, pk):
        # if this is a POST request we need to process the form data
    match = Athletics.objects.get(pk=pk)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = playerAdd(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            pass
        players = form.cleaned_data['players']
        for player in players:
            PlayerAthletics(player=Player.objects.get(pk=player.pk),
                            athletics = match,
                            ).save()


            return redirect('index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerAdd(queryset = Player.objects.filter(event=match.event, category=match.category, approved_status=True))
        return render(request, 'Schedule/sports/athletics/forms/playerathletics_form.html', {'form': form})

## Form: Adding Match
# class AthleticsUpdateWizard(SessionWizardView):
#     form_list = [AthleticsCreate, PlayerAdd]
#
#     def get_template_names(self):
#         TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
#                     "1": "Schedule/generic/forms/match_players.html"}
#
#         return [TEMPLATES[self.steps.current]]
#
#     def get_form_kwargs(self, step):
#
#         if(step =='0'):
#             print('hi')
#
#             pk = self.kwargs['pk']
#             print(pk)
#             match = Athletics.objects.filter(pk__in=[pk,])[0]
#             print(type(match))
#             self.initial_dict = match.__dict__
#             return {}
#         elif (step == '1'):
#
#             prev_data = self.storage.get_step_data('0')
#
#             event = prev_data.get('0-event')
#             category = prev_data.get('0-category')
#
#             return {
#                 'queryset' : Player.objects.filter(event=event, category=category, approved_status=True),
#             }
#
#     def done(self, form_list, form_dict, **kwargs):
#         match = form_dict['0'].save()
#         form_1 = form_dict['1']
#
#         # requests.post(url, data={djangoID})
#
#         players = form_1.cleaned_data['players']
#
#         for player in players:
#             PlayerAthletics(player=Player.objects.get(pk=player.pk),
#                             athletics = match,
#                             ).save()
#
#         return redirect('index')

# Form: Updating Player Info
class PlayerAthleticsUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerAthletics
    template_name = 'Schedule/sports/athletics/forms/playerathletics_update_form.html'
    fields = ['player', 'athletics', 'time', 'medal']
    success_url = reverse_lazy('index')

############################ --------- End Athletics------------------ #######################



############################ --------- Badminton------------------ #######################

# Schedule page
class BadmintonView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Badminton.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = BadmintonScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "badminton",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }
# Points table
class BadmintonScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/badminton/badminton_score.html'
    queryset = BadmintonScore.objects.all()

    def get_queryset(self):
        return BadmintonScore.objects.all().order_by('-points')

#Form to create an entry for Badminton
class BadmintonScoreCreate(CreateView):
    model = BadmintonScore
    fields = '__all__'
    success_url = reverse_lazy('badminton')

#Form to update an entry for Badminton
class BadmintonScoreTableUpdate(UpdateView):
    model = BadmintonScore
    fields = '__all__'
    success_url = reverse_lazy('badminton')

# Form: Adding Match
class BadmintonWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [BadmintonCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']


        for player in players_team1:
            PlayerBadminton(player=Player.objects.get(pk=player.pk),
                            badminton = match,
                            ).save()

        for player in players_team2:
            PlayerBadminton(player=Player.objects.get(pk=player.pk),
                            badminton = match,
                            ).save()

        return redirect('index')


# Form: Deleting Matches
class BadmintonDeleteView(LoginRequiredMixin, DeleteView):
    model = Badminton
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('badminton')

# Form: Updating Match Info
class BadmintonUpdate(LoginRequiredMixin, UpdateView):
    model = Badminton
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'game_level', 'score_detail']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/badminton/forms/badminton_update_form.html'


# Form: Updating Player Info
class PlayerBadmintonUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerBadminton
    template_name = 'Schedule/sports/badminton/forms/playerbadminton_update_form.html'
    fields = ['player', 'badminton', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Badminton------------------ #######################



############################ --------- Basketball ------------------ #######################

# Schedule page
class BasketballView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Basketball.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = BasketballScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "basketball",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }
# Points table
class BasketballScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/basketball/basketball_score.html'
    queryset = BasketballScore.objects.all()

    def get_queryset(self):
        return BasketballScore.objects.all().order_by('-points')

#Form to create an entry for Basketball
class BasketballScoreCreate(CreateView):
    model = Basketball
    fields = '__all__'
    success_url = reverse_lazy('basketball')

#Form to update an entry for Basketball
class BasketballScoreTableUpdate(UpdateView):
    model = Basketball
    fields = '__all__'
    success_url = reverse_lazy('basketball')


# Form: Adding Match
class BasketballWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [BasketballCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }


    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']


        for player in players_team1:
            PlayerBasketball(player=Player.objects.get(pk=player.pk),
                            basketball = match,
                            ).save()

        for player in players_team2:
            PlayerBasketball(player=Player.objects.get(pk=player.pk),
                            basketball = match,
                            ).save()

        return redirect('index')


# Form: Deleting Matches
class BasketballDeleteView(LoginRequiredMixin, DeleteView):
    model = Basketball
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('basketball')

# Form: Updating Match Info
class BasketballUpdate(UpdateView):
    model = Basketball
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'score_detail', 'game_level', 'score_detail']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/basketball/forms/basketball_update_form.html'



# Form: Updating Player Info
class PlayerBasketballUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerBasketball
    template_name = 'Schedule/sports/basketball/forms/playerbasketball_update_form.html'
    fields = ['player', 'basketball', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Basketball ------------------ #######################



############################ --------- Cricket ------------------ #######################

# Schedule page
class CricketView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Cricket.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = CricketScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "cricket",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Cricket
class CricketScoreCreate(CreateView):
    model = CricketScore
    fields = '__all__'
    success_url = reverse_lazy('cricket')

#Form to update an entry for Cricket
class CricketScoreTableUpdate(UpdateView):
    model = CricketScore
    fields = '__all__'
    success_url = reverse_lazy('cricket')

# Points table
class CricketScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/cricket/cricket_score.html'
    queryset = CricketScore.objects.all()

    def get_queryset(self):
        return CricketScore.objects.all().order_by('-points')

# Form: Adding Match
class CricketWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [CricketCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')

            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']


        for player in players_team1:
            PlayerCricket(player=Player.objects.get(pk=player.pk),
                            cricket = match,
                            ).save()
        for player in players_team2:
            PlayerCricket(player=Player.objects.get(pk=player.pk),
                            cricket = match,
                            ).save()


        return redirect('index')

# Form: Deleting Matches
class CricketDeleteView(LoginRequiredMixin, DeleteView):
    model = Cricket
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('cricket')

# Form: Updating Match Info
class CricketUpdate(UpdateView):
    model = Cricket
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'wicket_team1', 'wicket_team2', 'over_team1', 'over_team2', 'team1', 'team2', 'score_detail', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/cricket/forms/cricket_update_form.html'


# Form: Updating Player Info
class PlayerCricketUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerCricket
    template_name = 'Schedule/sports/cricket/forms/playercricket_update_form.html'
    fields = ['player', 'cricket', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Cricket ------------------ #######################



############################ --------- Football ------------------ #######################

# Schedule page
class FootballView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Football.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = FootballScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "football",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }


#Form to create an entry for Football
class FootballScoreCreate(CreateView):
    model = FootballScore
    fields = '__all__'
    success_url = reverse_lazy('football')

#Form to update an entry for Football
class FootballScoreTableUpdate(UpdateView):
    model = FootballScore
    fields = '__all__'
    success_url = reverse_lazy('football')

# Points table
class FootballScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/football/football_score.html'
    queryset = FootballScore.objects.all()

    def get_queryset(self):
        return FootballScore.objects.all().order_by('-points')

# Form: Adding Match
class FootballWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [FootballCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }
    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            PlayerFootball(player=Player.objects.get(pk=player.pk),
                            football = match,
                            ).save()

        for player in players_team2:
            PlayerFootball(player=Player.objects.get(pk=player.pk),
                            football = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class FootballDeleteView(LoginRequiredMixin, DeleteView):
    model = Football
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('football')

# Form: Updating Match Info
class FootballUpdate(UpdateView):
    model = Football
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/football/forms/football_update_form.html'


# Form: Updating Player Info
class PlayerFootballUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerFootball
    template_name = 'Schedule/sports/football/forms/playerfootball_update_form.html'
    fields = ['player', 'football', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Football ------------------ #######################



############################ --------- Hockey ------------------ #######################

# Schedule page
class HockeyView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Hockey.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = HockeyScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "hockey",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Hockey
class HockeyScoreCreate(CreateView):
    model = HockeyScore
    fields = '__all__'
    success_url = reverse_lazy('hockey')

#Form to update an entry for Hockey
class HockeyScoreTableUpdate(UpdateView):
    model = HockeyScore
    fields = '__all__'
    success_url = reverse_lazy('hockey')


# Points table
class HockeyScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/hockey/hockey_score.html'
    queryset = HockeyScore.objects.all()

    def get_queryset(self):
        return HockeyScore.objects.all().order_by('-points')

# Form: Adding Match
class HockeyWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [HockeyCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }
    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            HockeyPlayer(player=Player.objects.get(pk=player.pk),
                            hockey = match,
                            ).save()

        for player in players_team2:
            HockeyPlayer(player=Player.objects.get(pk=player.pk),
                            hockey = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class HockeyDeleteView(LoginRequiredMixin, DeleteView):
    model = Hockey
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('hockey')

# Form: Updating Match Info
class HockeyUpdate(LoginRequiredMixin, UpdateView):
    model = Hockey
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/hockey/forms/hockey_update_form.html'

# Form: Updating Player Info
class PlayerHockeyUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerHockey
    template_name = 'Schedule/sports/hockey/forms/playerhockey_update_form.html'
    fields = ['player', 'hockey', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Hockey ------------------ #######################



############################ --------- Squash ------------------ #######################

# Schedule page
class SquashView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Squash.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = SquashScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "squash",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Squash
class SquashScoreCreate(CreateView):
    model = SquashScore
    fields = '__all__'
    success_url = reverse_lazy('squash')

#Form to update an entry for Squash
class SquashScoreTableUpdate(UpdateView):
    model = SquashScore
    fields = '__all__'
    success_url = reverse_lazy('squash')

# Points table
class SquashScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/squash/squash_score.html'
    queryset = SquashScore.objects.all()

    def get_queryset(self):
        return SquashScore.objects.all().order_by('-points')

# Form: Adding Match
class SquashWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [SquashCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            PlayerSquash(player=Player.objects.get(pk=player.pk),
                            squash = match,
                            ).save()

        for player in players_team2:
            PlayerSquash(player=Player.objects.get(pk=player.pk),
                            squash = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class SquashDeleteView(LoginRequiredMixin, DeleteView):
    model = Squash
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('squash')

# Form: Updating Match Info
class SquashUpdate(LoginRequiredMixin, UpdateView):
    model = Squash
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'score_detail', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/squash/forms/squash_update_form.html'


# Form: Updating Player Info
class PlayerSquashUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerSquash
    template_name = 'Schedule/sports/squash/forms/playersquash_update_form.html'
    fields = ['player', 'squash', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Squash ------------------ #######################



############################ --------- Tennis ------------------ #######################

# Schedule page
class TennisView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Tennis.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = TennisScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "tennis",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Tennis
class TennisScoreCreate(CreateView):
    model = TennisScore
    fields = '__all__'
    success_url = reverse_lazy('tennis')

#Form to update an entry for Tennis
class TennisScoreTableUpdate(UpdateView):
    model = TennisScore
    fields = '__all__'
    success_url = reverse_lazy('tennis')

# Points table
class TennisScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/tennis/tennis_score.html'
    queryset = TennisScore.objects.all()

    def get_queryset(self):
        return TennisScore.objects.all().order_by('-points')

# Form: Adding Match
class TennisWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [TennisCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            PlayerTennis(player=Player.objects.get(pk=player.pk),
                            tennis = match,
                            ).save()

        for player in players_team2:
            PlayerTennis(player=Player.objects.get(pk=player.pk),
                            tennis = match,
                            ).save()



        return redirect('index')

# Form: Deleting Matches
class TennisDeleteView(LoginRequiredMixin, DeleteView):
    model = Tennis
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('tennis')

# Form: Updating Match Info
class TennisUpdate(LoginRequiredMixin, UpdateView):
    model = Tennis
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'score_detail', 'game_level']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/tennis/forms/tennis_update_form.html'

# Form: Updating Player Info
class PlayerTennisUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerTennis
    template_name = 'Schedule/sports/tennis/forms/playertennis_update_form.html'
    fields = ['player', 'tennis', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Tennis ------------------ #######################



############################ --------- Table Tennis ------------------ #######################

# Schedule page
class TableTennisView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = TableTennis.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = TableTennisScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "table tennis",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Table Tennis
class TableTennisScoreCreate(CreateView):
    model = TableTennisScore
    fields = '__all__'
    success_url = reverse_lazy('table_tennis')

#Form to update an entry for Table Tennis
class TableTennisScoreTableUpdate(UpdateView):
    model = TableTennisScore
    fields = '__all__'
    success_url = reverse_lazy('table_tennis')

# Points table
class TableTennisScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/table_tennis/tabletennis_score.html'
    queryset = TableTennis.objects.all()

    def get_queryset(self):
        return TableTennisScore.objects.all().order_by('-points')

# Form: Adding Match
class TableTennisWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [TableTennisCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            PlayerTableTennis(player=Player.objects.get(pk=player.pk),
                            tabletennis = match,
                            ).save()

        for player in players_team2:
            PlayerTableTennis(player=Player.objects.get(pk=player.pk),
                            tabletennis = match,
                            ).save()



        return redirect('index')

# Form: Deleting Matches
class TableTennisDeleteView(LoginRequiredMixin, DeleteView):
    model = TableTennis
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('table_tennis')

# Form: Updating Match Info
class TableTennisUpdate(LoginRequiredMixin, UpdateView):
    model = TableTennis
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'score_detail', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/table_tennis/forms/tabletennis_update_form.html'

# Form: Updating Player Info
class PlayerTableTennisUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerTableTennis
    template_name = 'Schedule/sports/table_tennis/forms/playertabletennis_update_form.html'
    fields = ['player', 'tabletennis', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Table Tennis ------------------ #######################



############################ --------- Volleyball ------------------ #######################

# Schedule page
class VolleyballView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = Volleyball.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = VolleyballScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "volleyball",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Volleyball
class VolleyballScoreCreate(CreateView):
    model = VolleyballScore
    fields = '__all__'
    success_url = reverse_lazy('volleyball')

#Form to update an entry for Volleyball
class VolleyballScoreTableUpdate(UpdateView):
    model = VolleyballScore
    fields = '__all__'
    success_url = reverse_lazy('volleyball')

# Points table
class VolleyballScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/volleyball/volleyball_score.html'
    queryset = VolleyballScore.objects.all()

    def get_queryset(self):
        return VolleyballScore.objects.all().order_by('-points')

# Form: Adding Match
class VolleyballWizard(SessionWizardView):
    form_list = [VolleyballCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            PlayerVolleyball(player=Player.objects.get(pk=player.pk),
                            volleyball = match,
                            ).save()

        for player in players_team2:
            PlayerVolleyball(player=Player.objects.get(pk=player.pk),
                            volleyball = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class VolleyballDeleteView(LoginRequiredMixin, DeleteView):
    model = Volleyball
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('volleyball')

# Form: Updating Match Info
class VolleyballUpdate(UpdateView):
    model = Volleyball
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'score_detail', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/volleyball/forms/volleyball_update_form.html'

# Form: Updating Player Info
class PlayerVolleyballUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerVolleyball
    template_name = 'Schedule/sports/volleyball/forms/playervolleyball_update_form.html'
    fields = ['player', 'volleyball', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Volleyball ------------------ #######################



############################ --------- Weight Lifting ------------------ #######################

# Schedule page
class WeightLiftingView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = WeightLifting.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = WeightLiftingScore.objects.all()

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "Weight Lifting",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
          }

#Form to create an entry for Weight Lifting
class WeightLiftingScoreCreate(CreateView):
    model = WeightLiftingScore
    fields = '__all__'
    success_url = reverse_lazy('weight_lifting')

#Form to update an entry for Weight Lifting
class WeightLiftingScoreTableUpdate(UpdateView):
    model = WeightLiftingScore
    fields = '__all__'
    success_url = reverse_lazy('weight_lifting')


# Points table
class WeightLiftingScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/weight_lifting/weightlifting_score.html'
    queryset = WeightLiftingScore.objects.all()

    def get_queryset(self):
        return WeightLiftingScore.objects.all().order_by('-points')

# Form: Adding Match
class WeightLiftingWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [WeightLiftingCreate, PlayerAdd]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')

            return {
                'queryset' : Player.objects.filter(event=event, category=category, approved_status=True),
            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players = form_1.cleaned_data['players']

        for player in players:
            PlayerWeightLifting(player=Player.objects.get(pk=player.pk),
                            weightlifting = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class WeightLiftingDeleteView(LoginRequiredMixin, DeleteView):
    model = WeightLifting
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('weight_lifting')

# Form: Updating Match Info
class WeightLiftingUpdate(LoginRequiredMixin, UpdateView):
    model = WeightLifting
    fields = ('date', 'time', 'event', 'category', 'place', 'game_level', 'duration', 'game_status', 'score_detail')
    # success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/weight_lifting/forms/weightlifting_update_form.html'

    def get_success_url(self):
        print('1')
        return reverse('playeradd_weightlifting', kwargs={'pk':self.kwargs['pk']})

def playeradd_weightlifting(request, pk):
        # if this is a POST request we need to process the form data
    match = WeightLifting.objects.get(pk=pk)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerAdd(request.POST, queryset = Player.objects.filter(event=match.event, category=match.category, approved_status=True))
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            pass
        players = form.cleaned_data['players']
        for player in players:
            PlayerWieghtLifting(player=Player.objects.get(pk=player.pk),
                            weightlifting = match,
                            ).save()


        return redirect('index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerAdd(queryset = Player.objects.filter(event=match.event, category=match.category, approved_status=True))
        return render(request, 'Schedule/generic/forms/match_players_update_1.html', {'form': form})

# Form: Adding Player
class PlayerWeightLiftingCreateView(LoginRequiredMixin, CreateView):
    fields = ('player', 'weightlifting', 'time', 'medal')
    model = PlayerWeightLifting
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/weight_lifting/forms/playerweightlifting_form.html'

# Form: Updating Player Info
class PlayerWeightLiftingUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerWeightLifting
    fields = ['player', 'weightlifting', 'time', 'medal']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/weight_lifting/forms/playerweightlifting_update_form.html'


def PlayerWeightLiftingDelete(request,pk):
    p = PlayerWeightLifting.objects.get(pk=pk)
    p.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/match/sports'))

############################ --------- End Weight Lifting  ------------------ #######################



############################ --------- Water Polo ------------------ #######################

# Schedule page
class WaterPoloView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'
    queryset = WaterPolo.objects.all()
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = WaterPoloScore.objects.all().order_by('-points')
    all_players = Player.objects.filter(event__sport__contains = "water")

    def get_queryset(self):
        """Return the last five published matches."""
        return {"matches": self.queryset.order_by('-date', '-time', '-event__event'), "sport": "water polo",
                "sports" : self.sports,
                "scoretable" : self.scoretable,
                "all_players" : self.all_players,
          }
        
#Form to create an entry for Water Polo
class WaterPoloScoreCreate(CreateView):
    model = WaterPoloScore
    fields = '__all__'
    success_url = reverse_lazy('water_polo')

#Form to update an entry for Water Polo
class WaterPoloScoreTableUpdate(UpdateView):
    model = WaterPoloScore
    fields = '__all__'
    success_url = reverse_lazy('water_polo')

# Points table
class WaterPoloScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/water_polo/waterpolo_score.html'
    queryset = WaterPoloScore.objects.all()

    def get_queryset(self):
        return WaterPoloScore.objects.all().order_by('-points')

# Form: Adding Match
class WaterPoloWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [WaterPoloCreate, PlayerAddTeamWise]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')
            team1 = prev_data.get('0-team1')
            team2 = prev_data.get('0-team2')

            players_team1 = Player.objects.filter(event=event, category=category, team=team1, approved_status=True)
            players_team2 = Player.objects.filter(event=event, category=category, team=team2, approved_status=True)

            return {
                'players_team1' : Player.objects.filter(event=event, category=category, team=team1, approved_status=True),
                'players_team2' : Player.objects.filter(event=event, category=category, team=team2, approved_status=True),

            }
    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players_team1 = form_1.cleaned_data['players_team1']
        players_team2 = form_1.cleaned_data['players_team2']

        for player in players_team1:
            PlayerWaterPolo(player=Player.objects.get(pk=player.pk),
                            waterpolo = match,
                            ).save()

        for player in players_team2:
            PlayerWaterPolo(player=Player.objects.get(pk=player.pk),
                            waterpolo = match,
                            ).save()


        return redirect('index')

# Form: Deleting Matches
class WaterPoloDeleteView(LoginRequiredMixin, DeleteView):
    model = WaterPolo
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('water_polo')

# Form: Updating Match Info
class WaterPoloUpdate(LoginRequiredMixin, UpdateView):
    model = WaterPolo
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status', 'event', 'score_team1', 'score_team2', 'team1', 'team2', 'game_level']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/water_polo/forms/waterpolo_update_form.html'

# Form: Updating Player Info
class PlayerWaterPoloUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerWaterPolo
    template_name = 'Schedule/sports/water_polo/forms/playerwaterpolo_update_form.html'
    fields = ['player', 'waterpolo', 'score']
    success_url = reverse_lazy('index')

############################ --------- End Water Polo ------------------ #######################



############################ --------- Swimming ------------------ #######################

# Schedule page
class SwimmingView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/generic/sports/sport.html'

    def get_queryset(self):
        queryset = Swimming.objects.all()
        sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
        scoretable = SwimmingScore.objects.order_by('-points','-gold','-silver','-bronze').all()
        """Return the last five published matches."""
        return {"matches": queryset.order_by('-date', '-time', '-event__event'), "sport": "swimming",
                "sports" : sports,
                "scoretable" : scoretable,
          }

#Form to create an entry for Swimming
class SwimmingScoreCreate(CreateView):
    model = SwimmingScore
    fields = '__all__'
    success_url = reverse_lazy('swimming')

#Form to update an entry for Swimming
class SwimmingScoreTableUpdate(UpdateView):
    model = SwimmingScore
    fields = '__all__'
    success_url = reverse_lazy('swimming')

def SwimmingTestView(request):
    iits = Team.objects.values_list('college', flat=True).order_by('college')
    events = Event.objects.filter(sport='swimming').values_list('event', flat=True).order_by('event').distinct
    sports = Event.objects.values_list('sport', flat=True).order_by('sport').distinct
    scoretable = SwimmingScore.objects.all()


    if request.method == "GET":

        matches = Swimming.objects.all().order_by('-date', '-time', '-event__event')
        context = {
                    'matches': matches,
                    'alliits' : iits,
                    'allevents' : events,
                    "sports" : sports,
                    "scoretable" : scoretable
                }

        return render(request, 'Schedule/generic/sports/sport.html', context)

    else:
        iit = request.POST.get('iit')
        event = request.POST.get('event')

        matches = Swimming.objects.all().filter(event=event).order_by('-date', '-time', '-event__event')
        context = {
                    'matches': matches,
                    'alliits' : iits,
                    'allevents' : events,
                    "sports" : sports,
                    "scoretable" : scoretable
                }
        return render(request, 'Schedule/generic/sports/sport.html', context)


# Points table
class SwimmingScoreView(generic.ListView):
    context_object_name = 'matches'
    template_name = 'Schedule/sports/swimming/swimming_score.html'
    queryset = SwimmingScore.objects.all()

    def get_queryset(self):
        return SwimmingScore.objects.all().order_by('-points')

# Form: Adding Match
class SwimmingWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [SwimmingCreate, PlayerAdd]

    def get_template_names(self):
        TEMPLATES = {"0": "Schedule/generic/forms/match_form.html",
                    "1": "Schedule/generic/forms/match_players.html"}

        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):

        if(step =='0'):
            print('hi')
            return {}
        elif (step == '1'):

            prev_data = self.storage.get_step_data('0')

            event = prev_data.get('0-event')
            category = prev_data.get('0-category')

            return {
                'queryset' : Player.objects.filter(event=event, category=category, approved_status=True),
            }

    def done(self, form_list, form_dict, **kwargs):

        # Admin Check
        user = self.request.user
        if not is_admin(user.id):
            return redirect('unauthorised')

        match = form_dict['0'].save()
        form_1 = form_dict['1']

        players = form_1.cleaned_data['players']

        for player in players:
            PlayerSwimming(player=Player.objects.get(pk=player.pk),
                            swimming = match,
                            ).save()

        return redirect('index')

# Form: Deleting Matches
class SwimmingDeleteView(LoginRequiredMixin, DeleteView):
    model = Swimming
    template_name = 'Schedule/generic/delete_entry.html'
    success_url = reverse_lazy('swimmingsch')

# Form: Updating Match Info
class SwimmingUpdate(LoginRequiredMixin, UpdateView):
    model = Swimming
    fields = ['date', 'time', 'duration', 'category', 'place', 'game_status']
    # success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/swimming/forms/swimming_update_form.html'

    def get_success_url(self):
        return reverse('playeradd_swimming', kwargs={'pk':self.kwargs['pk']})

def playeradd_swimming(request, pk):
        # if this is a POST request we need to process the form data
    match = Swimming.objects.get(pk=pk)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerAdd(request.POST, queryset = Player.objects.filter(event=match.event, category=match.category, approved_status=True))
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            pass
        players = form.cleaned_data['players']
        for player in players:
            PlayerSwimming(player=Player.objects.get(pk=player.pk),
                            swimming = match,
                            ).save()


        return redirect('index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerAdd(queryset = Player.objects.filter(event=match.event, category=match.category, approved_status=True))
        return render(request, 'Schedule/generic/forms/match_players_update_1.html', {'form': form})

# Form: Adding Player
class PlayerSwimmingCreateView(LoginRequiredMixin, CreateView):
    fields = ('player', 'swimming', 'time', 'medal')
    model = PlayerSwimming
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/swimming/forms/playerswimming_form.html'

# Form: Updating Player Info
class PlayerSwimmingUpdate(LoginRequiredMixin, UpdateView):
    model = PlayerSwimming
    fields = ['player', 'swimming', 'time', 'medal']
    success_url = reverse_lazy('index')
    template_name = 'Schedule/sports/swimming/forms/playerswimming_update_form.html'

def PlayerSwimmingDelete(request,pk):
    p = PlayerSwimming.objects.get(pk=pk)
    p.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/match/sports'))


############################ --------- End Swimming ------------------ #####################

############################ --------- End Match Views ------------------ #####################
##############################################################################################

## Users Login and Logout

# Staff Creation
@login_required
def staff_register(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            college = form.cleaned_data.get('college')
            user_type = form.cleaned_data.get('user_type')

            Profile(user=user, college=college, user_type=user_type).save()
            my_group = Group.objects.get(name='college_staff')
            my_group.user_set.add(user)

            return redirect('staff_register')
    else:
        form = StaffForm()
    return render(request, 'Schedule/registration/staff_register.html', {'form': form})

# Login Staff
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('player_list_staff', sport='athletics')
            else:
                return render(request, 'Schedule/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Schedule/login.html', {'error_message': 'Invalid login'})
    return render(request, 'Schedule/login.html')

# Logout Staff
@login_required
def logout_user(request):
    logout(request)
    # Redirect to a success page.
    return redirect('index')


# Static pages

class AboutView(TemplateView):
    template_name="Schedule/static/about.html"

class InteriitView(TemplateView):
    template_name="Schedule/static/interiit.html"

class PlacesView(TemplateView):
    template_name="Schedule/static/places.html"

class GettingthereView(TemplateView):
    template_name="Schedule/static/reaching.html"

class MapView(TemplateView):
    template_name="Schedule/static/map.html"


# coming soon
def comingsoon(request):
    return render(request, 'Schedule/generic/comingsoon.html')

# csv handler for gallery
def csv_handler_gallery(request):
    # if request.method == "POST":
    #     csv_file = request.FILES["csv_file"]
    #     if not csv_file.name.endswith('.csv'):
    #         return HttpResponse('File is not CSV type')

    #     file_data = csv_file.read().decode("utf-8")
    #     lines = file_data.split("\n")

    #     for line in lines:
    #         fields = line.split(",")
    #         pk = int(fields[0])
    #         url = fields[1]

    #         player = Player.objects.get(pk=pk)

    #         try:
    #             album = Album.objects.get(player=player)
    #         except Scheduel.models.DoesNotExist:
    #             album = Album.objects.create(player=player, urls='[]')

    #         urls_string = album.urls
    #         jsonDec = json.decoder.JSONDecoder()
    #         urls_list = jsonDec.decode(urls_string)
    #         urls_list.append(url)
    #         urls_string_new = json.dumps(urls_list)
    #         album.urls = urls_string_new
    #         album.save()
    #     return HttpResponse('Done Updating')
    # else:
    #     return render(request, 'Schedule/generic/forms/csv_handler_gallery.html')
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('File is not CSV type')

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")

        for line in lines:
            fields = line.split(",")
            album = fields[0]
            url = fields[1]
            elem = Photo.objects.create(album=album,urls=url)
            elem.save()
        return HttpResponse('Done Updating')
    else:
        return render(request, 'Schedule/generic/forms/csv_handler_gallery.html')

# Photo list views

def gallery_name(request,album_name):

    albums = reversed(Photo.objects.order_by('-created_at').values('album').distinct().order_by())
    photos = Photo.objects.filter(album=album_name).all()
    # page = request.GET.get('page', 1)

    # paginator = Paginator(photos, 10)
    # try:
    #     photos = paginator.page(page)
    # except PageNotAnInteger:
    #     photos = paginator.page(1)
    # except EmptyPage:
    #     photos = paginator.page(paginator.num_pages)

    context = {'photos': photos,"albums":albums, "album_name":album_name}

    return render(request, 'Schedule/generic/photos.html', context)

def gallery(request):

    albums = list(reversed(Photo.objects.order_by('-created_at').values('album').distinct().order_by()))
    album_name = list(albums[0].values())[0]
    photos = Photo.objects.filter(album=album_name).all()
    # page = request.GET.get('page', 1)

    # paginator = Paginator(photos, 10)
    # try:
    #     photos = paginator.page(page)
    # except PageNotAnInteger:
    #     photos = paginator.page(1)
    # except EmptyPage:
    #     photos = paginator.page(paginator.num_pages)

    context = {'photos': photos,"albums":albums, "album_name":album_name}

    return render(request, 'Schedule/generic/photos.html', context)

def WaterPoloScoreUpdate(request):
    matches = WaterPolo.objects.all().order_by('date', 'time')
    playermatchlist = []
    players = Player.objects.filter(event__sport__contains = "water")
    for player in players:
        playermatchlist.append(str(player.team)+"    "+player.name)
    context = {'entries':playermatchlist}
    return render(request,'Schedule/test/waterpoloscoresupdate.html',context)


from .resources import PlayerResource

def player_export(request):
    profile = Profile.objects.get(user=request.user)
    team = profile.college

    queryset = Player.objects.filter(team=team, approved_status=True).exclude(event__sport__in = ['swimming', 'water_polo'])
    person_resource = PlayerResource()
    dataset = person_resource.export(queryset)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response
