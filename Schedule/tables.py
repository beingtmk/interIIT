# Schedule/tables.py
import django_tables2 as tables
from .models import Player, Staff
from django_tables2.utils import A
from django_tables2.export.views import ExportMixin

class PlayerTable(ExportMixin, tables.Table):
    # cp = tables.Column(accessor='get_photo',verbose_name='Photo')

    class Meta:
        model = Player
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'name', 'team', 'events', 'nationality', 'category', 'blood_group', 'mobile_no', 'email', 'photo', 'food', 'approved_status')

class StaffTable(ExportMixin, tables.Table):

    # profile = tables.LinkColumn(
    #   viewname = 'player_profile',
    #   args=[A('pk')],
    #   accessor=A('__str__')  # or whatever attribute of your instance you want to display
    # )

    class Meta:
        model = Staff
        template_name = 'django_tables2/bootstrap.html'
