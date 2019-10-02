from import_export import resources, fields
from import_export.widgets import ManyToManyWidget

from .models import Player, Event

class PlayerResource(resources.ModelResource):

    event = fields.Field(
        column_name='event',
        attribute='event',
        widget=ManyToManyWidget(Event, ',', 'code'))

    class Meta:
        model = Player
        fields = ['id', 'name', 'category', 'blood_group', 'mobile_no', 'email', 'food', 'nationality', 'event']
