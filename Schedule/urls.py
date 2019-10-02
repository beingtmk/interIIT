"""Schedule URL Configuration"""
##	link this view to some url in urls.py of the same app directory

from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [

    path('pages/comingsoon', views.comingsoon, name='comingsoon'),

    # path('', TemplateView.as_view(template_name="Schedule/index.html"), name='homepage'),
    path('', views.IndexView.as_view(), name='homepage'),
    # path('', views.comingsoon, name='homepage'),
    path('gallery/<str:album_name>/', views.gallery_name, name='gallery_name'),
    path('gallery/', views.gallery, name='gallery'),
    # path('gallery/', views.gallery, name='gallery'),
    # path('gallery/', views.comingsoon, name='gallery'),


    # Url to index page of Schedule app
    path('match/sports', views.ScheduleIndexView.as_view(), name='index'),
    # path('match/sports', views.comingsoon, name='index'),


    # Url to Registration of Player, staff
    path('staff/register/', views.StaffCreateView.as_view(),name='staffcreate'),

    path('player/register/', views.RegistrationWizard.as_view(), name='testplayercreate'),

    path('player/list/', views.PlayerListView, name='playerlist'),
    path('events-autocomplete/', views.EventAutocomplete.as_view(),name='event-autocomplete'),
    path('player/update/<int:pk>/', views.PlayerUpdateView.as_view(), name='playerupdate'),
    path('player/delete/<int:pk>/', views.PlayerDeleteView.as_view(), name='playerdelete'),

    path('player/filter/', views.player_filter, name='playerfilter'),
    path('staff/list/', views.StaffListView, name='stafflist'),


    # Forms for college admin
    path('registration/staff/sport_list', views.SportView.as_view(), name='sport_list'),
    path('registration/staff/player_list/<slug:sport>', views.Players_Sports.as_view(), name='player_list_staff'),
    path('registration/staff/toggle/<int:pk>', views.approve_toggle, name='player_approve_toggle'),

    # Urls to Schedule Page
    path('match/athletics/', views.AthleticsView.as_view(), name='athletics'),
    path('match/badminton/', views.BadmintonView.as_view(), name='badminton'),
    path('match/basketball/', views.BasketballView.as_view(), name='basketball'),
    path('match/cricket/', views.CricketView.as_view(), name='cricket'),
    path('match/football/', views.FootballView.as_view(), name='football'),
    path('match/hockey/', views.HockeyView.as_view(), name='hockey'),
    path('match/squash/', views.SquashView.as_view(), name='squash'),
    path('match/tennis/', views.TennisView.as_view(), name='tennis'),
    path('match/table_tennis/', views.TableTennisView.as_view(), name='table_tennis'),
    path('match/volleyball/', views.VolleyballView.as_view(), name='volleyball'),
    path('match/weight_lifting/', views.WeightLiftingView.as_view(), name='weight_lifting'),
    path('match/water_polo/', views.WaterPoloView.as_view(), name='water_polo'),
    path('match/swimming/', views.SwimmingView.as_view(), name='swimming'),
    path('match/swimmingsch/', views.SwimmingView.as_view(), name='swimmingsch'),
    path('match/swimming/test', views.SwimmingTestView, name='swimmingtest'),
    path('testview/waterpoloscoresupdate',views.WaterPoloScoreUpdate,name="testwaterpoloscores"),

    # Urls to form/table Schedule Page
    path('form/table/athletics/', staff_member_required(views.AthleticsScoreCreate.as_view()), name='athletics_form'),
    path('form/table/badminton/', staff_member_required(views.BadmintonScoreCreate.as_view()), name='badminton_form'),
    path('form/table/basketball/', staff_member_required(views.BasketballScoreCreate.as_view()), name='basketball_form'),
    path('form/table/cricket/', staff_member_required(views.CricketScoreCreate.as_view()), name='cricket_form'),
    path('form/table/football/', staff_member_required(views.FootballScoreCreate.as_view()), name='football_form'),
    path('form/table/hockey/', staff_member_required(views.HockeyScoreCreate.as_view()), name='hockey_form'),
    path('form/table/squash/', staff_member_required(views.SquashScoreCreate.as_view()), name='squash_form'),
    path('form/table/tennis/', staff_member_required(views.TennisScoreCreate.as_view()), name='tennis_form'),
    path('form/table/table_tennis/', staff_member_required(views.TableTennisScoreCreate.as_view()), name='table_tennis_form'),
    path('form/table/volleyball/', staff_member_required(views.VolleyballScoreCreate.as_view()), name='volleyball_form'),
    path('form/table/weight_lifting/', staff_member_required(views.WeightLiftingScoreCreate.as_view()), name='weight_lifting_form'),
    path('form/table/water_polo/', staff_member_required(views.WaterPoloScoreCreate.as_view()), name='water_polo_form'),
    path('form/table/swimming/', staff_member_required(views.SwimmingScoreCreate.as_view()), name='swimming_form'),
    path('form/table/swimmingsch/', staff_member_required(views.SwimmingScoreCreate.as_view()), name='swimmingsch_form'),
    # path('testview/waterpoloscoresupdate',staff_member_required(views.WaterPoloScoreUpdate,name="testwaterpoloscores"),

    # Urls to form/table Schedule Page
    path('update/table/athletics/<int:pk>/', staff_member_required(views.AthleticsScoreTableUpdate.as_view()), name='athletics_table_update'),
    path('update/table/badminton/<int:pk>/', staff_member_required(views.BadmintonScoreTableUpdate.as_view()), name='badminton_table_update'),
    path('update/table/basketball/<int:pk>/', staff_member_required(views.BasketballScoreTableUpdate.as_view()), name='basketball_table_update'),
    path('update/table/cricket/<int:pk>/', staff_member_required(views.CricketScoreTableUpdate.as_view()), name='cricket_table_update'),
    path('update/table/football/<int:pk>/', staff_member_required(views.FootballScoreTableUpdate.as_view()), name='football_table_update'),
    path('update/table/hockey/<int:pk>/', staff_member_required(views.HockeyScoreTableUpdate.as_view()), name='hockey_table_update'),
    path('update/table/squash/<int:pk>/', staff_member_required(views.SquashScoreTableUpdate.as_view()), name='squash_table_update'),
    path('update/table/tennis/<int:pk>/', staff_member_required(views.TennisScoreTableUpdate.as_view()), name='tennis_table_update'),
    path('update/table/table_tennis/<int:pk>/', staff_member_required(views.TableTennisScoreTableUpdate.as_view()), name='table_tennis_table_update'),
    path('update/table/volleyball/<int:pk>/', staff_member_required(views.VolleyballScoreTableUpdate.as_view()), name='volleyball_table_update'),
    path('update/table/weight_lifting/<int:pk>/', staff_member_required(views.WeightLiftingScoreTableUpdate.as_view()), name='weight_lifting_table_update'),
    path('update/table/water_polo/<int:pk>/', staff_member_required(views.WaterPoloScoreTableUpdate.as_view()), name='water_polo_table_update'),
    path('update/table/swimming/<int:pk>/', staff_member_required(views.SwimmingScoreTableUpdate.as_view()), name='swimming_table_update'),
    # path('update/table/swimmingsch/<int:pk>/', staff_member_required(views.SwimmingScoreTableUpdate.as_view()), name='swimmingsch_table_update'),


    # Urls to Adding Match
    path('create_athletics/',views.AthleticsWizard.as_view(),name='create_athletics'),
    path('create_badminton/',views.BadmintonWizard.as_view(),name='create_badminton'),
    path('create_basketball/',views.BasketballWizard.as_view(),name='create_basketball'),
    path('create_cricket/',views.CricketWizard.as_view(),name='create_cricket'),
    path('create_football/',views.FootballWizard.as_view(),name='create_football'),
    path('create_hockey/',views.HockeyWizard.as_view(),name='create_hockey'),
    path('create_squash/',views.SquashWizard.as_view(),name='create_squash'),
    path('create_tennis/',views.TennisWizard.as_view(),name='create_tennis'),
    path('create_tabletennis/',views.TableTennisWizard.as_view(),name='create_tabletennis'),
    path('create_volleyball/',views.VolleyballWizard.as_view(),name='create_volleyball'),
    path('create_weightlifting/',views.WeightLiftingWizard.as_view(),name='create_weightlifting'),
    path('create_waterpolo/',views.WaterPoloWizard.as_view(),name='create_waterpolo'),
    path('create_swimming/',views.SwimmingWizard.as_view(),name='create_swimming'),

    # Urls to Delete Match
    path('delete_athletics/<int:pk>/',views.AthleticsDeleteView.as_view(),name='athletics_delete'),
    path('delete_badminton/<int:pk>/',views.BadmintonDeleteView.as_view(),name='badminton_delete'),
    path('delete_basketball/<int:pk>/',views.BasketballDeleteView.as_view(),name='basketball_delete'),
    path('delete_cricket/<int:pk>/',views.CricketDeleteView.as_view(),name='cricket_delete'),
    path('delete_football/<int:pk>/',views.FootballDeleteView.as_view(),name='football_delete'),
    path('delete_hockey/<int:pk>/',views.HockeyDeleteView.as_view(),name='hockey_delete'),
    path('delete_squash/<int:pk>/',views.SquashDeleteView.as_view(),name='squash_delete'),
    path('delete_tennis/<int:pk>/',views.TennisDeleteView.as_view(),name='tennis_delete'),
    path('delete_tabletennis/<int:pk>/',views.TableTennisDeleteView.as_view(),name='tabletennis_delete'),
    path('delete_volleyball/<int:pk>/',views.VolleyballDeleteView.as_view(),name='volleyball_delete'),
    path('delete_weightlifting/<int:pk>/',views.WeightLiftingDeleteView.as_view(),name='weightlifting_delete'),
    path('delete_waterpolo/<int:pk>/',views.WaterPoloDeleteView.as_view(),name='waterpolo_delete'),
    path('delete_swimming/<int:pk>/',views.SwimmingDeleteView.as_view(),name='swimming_delete'),

    # Urls to Match update
    path('athletics_update/<int:pk>/', views.AthleticsUpdate.as_view(), name='athletics_update'),
    # path('athletics_update/<int:pk>/', views.AthleticsUpdateWizard.as_view(), name='athletics_update'),

    path('badminton_update/<int:pk>/', views.BadmintonUpdate.as_view(), name='badminton_update'),
    path('basketball_update/<int:pk>/', views.BasketballUpdate.as_view(), name='basketball_update'),
    path('cricket_update/<int:pk>/', views.CricketUpdate.as_view(), name='cricket_update'),
    path('football_update/<int:pk>/', views.FootballUpdate.as_view(), name='football_update'),
    path('hockey_update/<int:pk>/', views.HockeyUpdate.as_view(), name='hockey_update'),
    path('squash_update/<int:pk>/', views.SquashUpdate.as_view(), name='squash_update'),
    path('tennis_update/<int:pk>/', views.TennisUpdate.as_view(), name='tennis_update'),
    path('tabletennis_update/<int:pk>/', views.TableTennisUpdate.as_view(), name='tabletennis_update'),
    path('volleyball_update/<int:pk>/', views.VolleyballUpdate.as_view(), name='volleyball_update'),
    path('weightlifting_update/<int:pk>/', views.WeightLiftingUpdate.as_view(), name='weightlifting_update'),
    path('waterpolo_update/<int:pk>/', views.WaterPoloUpdate.as_view(), name='waterpolo_update'),
    path('swimming_update/<int:pk>/', views.SwimmingUpdate.as_view(), name='swimming_update'),
    path('weightlifting_update/<int:pk>/', views.WeightLiftingUpdate.as_view(), name='weightlifting_update'),

    # Urls to Points Table
    path('match/football_score/', views.FootballScoreView.as_view(), name='football_score'),
    path('match/badminton_score/', views.BadmintonScoreView.as_view(), name='badminton_score'),
    path('match/basketball_score/', views.BasketballScoreView.as_view(), name='basketball_score'),
    path('match/cricket_score/', views.CricketScoreView.as_view(), name='cricket_score'),
    path('match/hockey_score/', views.HockeyScoreView.as_view(), name='hockey_score'),
    path('match/squash_score/', views.SquashScoreView.as_view(), name='squash_score'),
    path('match/tennis_score/', views.TennisScoreView.as_view(), name='tennis_score'),
    path('match/tabletennis_score/', views.TableTennisScoreView.as_view(), name='tabletennis_score'),
    path('match/volleyball_score/', views.VolleyballScoreView.as_view(), name='volleyball_score'),
    path('match/waterpolo_score/', views.WaterPoloScoreView.as_view(), name='waterpolo_score'),
    path('match/athletics_score/', views.AthleticsScoreView.as_view(), name='athletics_score'),
    path('match/swimming_score/', views.SwimmingScoreView.as_view(), name='swimming_score'),
    path('match/weightlifting_score/', views.WeightLiftingScoreView.as_view(), name='weightlifting_score'),

    # Urls to Add Players
    #path('create_playerweightlifting/',views.PlayerWeightLiftingCreateView.as_view(),name='create_playerweightlifting'),
    #path('create_playerswimming/',views.PlayerSwimmingCreateView.as_view(),name='create_playerswimming'),
    #
    #Urls to Update Players
    path('playerathletics_update/<int:pk>/', views.PlayerAthleticsUpdate.as_view(), name='playerathletics_update'),
    path('playerathletics_delete/<int:pk>/', views.PlayerAthleticsDelete, name='playerathletics_delete'),
    path('playerswimming_update/<int:pk>/', views.PlayerSwimmingUpdate.as_view(), name='playerswimming_update'),
    path('playerswimming_delete/<int:pk>/', views.PlayerSwimmingDelete, name='playerswimming_delete'),
    path('playerweightlifting_update/<int:pk>/', views.PlayerWeightLiftingUpdate.as_view(), name='playerweightlifting_update'),
    path('playerweightlifting_delete/<int:pk>/', views.PlayerWeightLiftingDelete, name='playerweightlifting_delete'),
    path('playerfootball_update/<int:pk>/', views.PlayerFootballUpdate.as_view(), name='playerfootball_update'),
    path('playerbadminton_update/<int:pk>/', views.PlayerBadmintonUpdate.as_view(), name='playerbadminton_update'),
    path('playerbasketball_update/<int:pk>/', views.PlayerBasketballUpdate.as_view(), name='playerbasketball_update'),
    path('playercricket_update/<int:pk>/', views.PlayerCricketUpdate.as_view(), name='playercricket_update'),
    path('playerhockey_update/<int:pk>/', views.PlayerHockeyUpdate.as_view(), name='playerhockey_update'),
    path('playertennis_update/<int:pk>/', views.PlayerTennisUpdate.as_view(), name='playertennis_update'),
    path('playertabletennis_update/<int:pk>/', views.PlayerTableTennisUpdate.as_view(), name='playertabletennis_update'),
    path('playervolleyball_update/<int:pk>/', views.PlayerVolleyballUpdate.as_view(), name='playervolleyball_update'),
    path('playersquash_update/<int:pk>/', views.PlayerSquashUpdate.as_view(), name='playersquash_update'),
    path('playerwaterpolo_update/<int:pk>/', views.PlayerWaterPoloUpdate.as_view(), name='playerwaterpolo_update'),

    #user
    path('accounts/staff_register/', views.staff_register, name='staff_register'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),

    path('search/', views.comingsoon, name='search'),
    #path('search/', views.search, name='search'),
    #path('searchtest/', views.search, name='searchabc'),


    path('player_profile/<int:pk>/', views.playerview, name='player_profile'),


    #static fles
    path('pages/about/', views.AboutView.as_view(), name='about'),
    path('pages/interiit/', views.InteriitView.as_view(), name='interiit'),
    path('pages/places/', views.PlacesView.as_view(), name='places'),
    path('pages/reachingiitg/', views.GettingthereView.as_view(), name='reaching'),
    path('pages/map/', views.MapView.as_view(), name='map'),

    #csv handler for gallery
    path('forms/gallery_handler/', views.csv_handler_gallery, name='csv_handler_gallery'),
    # path('scripts/link_players/', views.link_players, name='link_players'),
    path('forms/playeradd_athletics/<int:pk>/', views.playeradd_athletics, name='playeradd_athletics'),
    path('forms/playeradd_swimming/<int:pk>/', views.playeradd_swimming, name='playeradd_swimming'),
    path('forms/playeradd_weightlifting/<int:pk>/', views.playeradd_weightlifting, name='playeradd_weightlifting'),

    path('export/player_export/', views.player_export, name='player_export'),

    path('unauthorised/', TemplateView.as_view(template_name="Schedule/generic/unauthorised.html"), name='unauthorised'),

]
