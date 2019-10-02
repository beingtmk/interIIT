from django import forms
from dal import autocomplete
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import (
    #Global Models
    Match,
    Event,
    Player , Staff,
    Team,

    #Others
    Badminton, BadmintonScore,
    Basketball, BasketballScore,
    Cricket, CricketScore,
    Football, FootballScore,
    Hockey, HockeyScore,
    Squash, SquashScore,
    Tennis, TennisScore,
    TableTennis, TableTennisScore,
    Volleyball, VolleyballScore,
    WaterPolo, WaterPoloScore,
    Athletics, AthleticsScore, PlayerAthletics,
    WeightLifting, WeightLiftingScore, PlayerWeightLifting,
    Swimming, SwimmingScore, PlayerSwimming,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget, Select2Widget



### Player Registration:

class PlayerCreate(forms.ModelForm):

    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=Select2Widget,)

    class Meta:
        model = Player
        fields = ('name', 'team', 'category', 'nationality','event', 'mobile_no', 'email', 'photo', 'blood_group', 'food')
        widgets = {
            'event': autocomplete.ModelSelect2Multiple(url='event-autocomplete'),
        }

        help_texts = {
            'mobile_no': 'Ex : +918830285891 (+91 is important!)',
            'event': 'Type a Sport or a Event you want to participate in...',
            'photo': 'Please upload a clear photo, as it will be used to tag any of your photos in the AI Gallery ...',

        }

class StaffCreate(forms.ModelForm):

    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=Select2Widget,)
    # sport = forms.ModelChoiceField(queryset=Event.objects.values_list('sport', flat=True).order_by('sport').distinct, widget=Select2Widget,)

    class Meta:
        model = Staff

        fields = '__all__'

        help_texts = {
            'mobile_no': 'Ex : +918830285891 (+91 is important!)',
            'arrival_transport_id' : 'Note : Train/Flight Number',
            'departure_transport_id' : 'Note : Train/Flight Number',
	    'sport':'Note : Leave empty if not applicable',
        }

class TriviaForm(forms.Form):
    answer = forms.CharField()


### To Add: two step form in match update

class PlayerAdd(forms.Form):

    players = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        super(PlayerAdd, self).__init__(*args, **kwargs)
        self.fields["players"] = forms.ModelMultipleChoiceField(queryset=queryset, widget=forms.CheckboxSelectMultiple())
        self.fields["players"].required = False

class PlayerAddTeamWise(forms.Form):

    players_team1 = forms.ModelMultipleChoiceField(queryset=None)
    players_team2 = forms.ModelMultipleChoiceField(queryset=None)
    def __init__(self, *args, **kwargs):
        players_team1 = kwargs.pop('players_team1')
        players_team2 = kwargs.pop('players_team2')
        super(PlayerAddTeamWise, self).__init__(*args, **kwargs)
        self.fields["players_team1"] = forms.ModelMultipleChoiceField(queryset=players_team1, widget=forms.CheckboxSelectMultiple())
        self.fields["players_team2"] = forms.ModelMultipleChoiceField(queryset=players_team2, widget=forms.CheckboxSelectMultiple())
        self.fields["players_team1"].required = False
        self.fields["players_team2"].required = False


class AthleticsCreate(forms.ModelForm):
    class Meta:
       model = Athletics
       fields = ('date', 'time', 'event', 'category', 'place', 'game_level')

    def __init__(self, *args, **kwargs):
       super(AthleticsCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='athletics')

class AthleticsUpdate(forms.ModelForm):
    class Meta:
       model = Athletics
       fields = ('date', 'time', 'event', 'category', 'place', 'game_level', 'duration', 'game_status', 'score_detail')

    def __init__(self, *args, **kwargs):
       sport = kwargs.pop('sport')
       super(AthleticsUpdate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport=sport)

class BadmintonCreate(forms.ModelForm):
    class Meta:
       model = Badminton
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(BadmintonCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='badminton')

class BasketballCreate(forms.ModelForm):
    class Meta:
       model = Basketball
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(BasketballCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='basketball')

class CricketCreate(forms.ModelForm):
    class Meta:
       model = Cricket
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(CricketCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='cricket')

class FootballCreate(forms.ModelForm):
    class Meta:
       model = Football
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(FootballCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='football')

class HockeyCreate(forms.ModelForm):
    class Meta:
       model = Hockey
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(HockeyCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='hockey')

class SquashCreate(forms.ModelForm):
    class Meta:
       model = Squash
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(SquashCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='squash')

class TennisCreate(forms.ModelForm):
    class Meta:
       model = Tennis
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(TennisCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='tennis')

class TableTennisCreate(forms.ModelForm):
    class Meta:
       model = TableTennis
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(TableTennisCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='table_tennis')

class VolleyballCreate(forms.ModelForm):
    class Meta:
       model = Volleyball
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       sport = kwargs.pop('sport')
       super(VolleyballCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='volleyball')

class WaterPoloCreate(forms.ModelForm):
    class Meta:
       model = WaterPolo
       fields = ('date', 'time', 'event', 'category', 'place', 'team1', 'team2', 'game_level',)

    def __init__(self, *args, **kwargs):
       super(WaterPoloCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='water_polo')


class WeightLiftingCreate(forms.ModelForm):
    class Meta:
       model = WeightLifting
       fields = ('date', 'time', 'event', 'category', 'place', 'game_level')

    def __init__(self, *args, **kwargs):
       super(WeightLiftingCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='weight_lifting')

class SwimmingCreate(forms.ModelForm):
    class Meta:
       model = Swimming
       fields = ('date', 'time', 'event', 'category', 'place',  'game_level')

    def __init__(self, *args, **kwargs):
       super(SwimmingCreate, self).__init__(*args, **kwargs)
       self.fields['event'].queryset = Event.objects.filter(sport='swimming')

class Search(forms.ModelForm):
    player = forms.CharField(max_length=100)

    class Meta:
        model = Player
        fields = ('name',)


class StaffForm(UserCreationForm):
    user_choices =  [
    ('STAFF','STAFF'),
    ('ADMIN','ADMIN'),
    ]

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    college = forms.ModelChoiceField(queryset = Team.objects.all())
    user_type = forms.ChoiceField(choices = user_choices)

    class Meta:
        model = User
        fields = ('username', 'college', 'user_type', 'email', 'password1',)

# Confirmation Form

class ConfirmationForm(forms.Form):
    confirm = forms.BooleanField(initial=False)

    class Meta:
        fields = '__all__'

class PlayerFilter(forms.Form):
    CATEGORY_CHOICES = (
        ('MEN', 'MEN'),
        ('WOMEN', 'WOMEN'),
    )

    SPORT_CHOICES = (
        ('athletics', 'Athletics'),
        ('badminton', 'Badminton'),
        ('basketball', 'Basketball'),
        ('cricket', 'Cricket'),
        ('football', 'Football'),
        ('hockey', 'Hockey'),
        ('squash', 'Squash'),
        ('tennis', 'Tennis'),
        ('table_tennis', 'Table Tennis'),
        ('volleyball', 'Volleyball'),
        ('weight_lifting', 'Weight Lifting'),
        ('water_polo', 'Water Polo'),
        ('swimming', 'Swimming'),
    )

    sport = forms.MultipleChoiceField(choices=SPORT_CHOICES, widget=Select2MultipleWidget, )

    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=Select2Widget,)

    class Meta:
        fields = '__all__'
