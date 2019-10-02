# Generated by Django 2.0.7 on 2018-12-06 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='athleticsscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='badmintonscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basketballscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cricketscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='footballscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hockeyscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='squashscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='swimmingscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tabletennisscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tennisscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volleyballscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waterpoloscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weightliftingscore',
            name='pool',
            field=models.CharField(choices=[('Heat 1', 'Heat 1'), ('SemiFinal 1', 'SemiFinal 1'), ('SemiFinal 2', 'SemiFinal 1'), ('Finals', 'Finals'), ('Round 1', 'Round 1'), ('Quarter Final', 'Quarter Final'), ('Semi Final', 'Semi Final'), ('Final', 'Final'), ('Pool A', 'Pool A'), ('Pool B', 'PoolB'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group C', 'Group C'), ('Group D', 'Group D'), ('TTF', 'TTF')], default='Pool A', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staff',
            name='sport',
            field=models.CharField(blank=True, choices=[('athletics', 'Athletics'), ('badminton', 'Badminton'), ('basketball', 'Basketball'), ('cricket', 'Cricket'), ('football', 'Football'), ('hockey', 'Hockey'), ('squash', 'Squash'), ('tennis', 'Tennis'), ('table_tennis', 'Table Tennis'), ('volleyball', 'Volleyball'), ('weight_lifting', 'Weight Lifting'), ('water_polo', 'Water Polo'), ('swimming', 'Swimming')], max_length=20),
        ),
        migrations.AlterField(
            model_name='staff',
            name='type',
            field=models.CharField(choices=[('coach', 'COACH'), ('sports_officer', 'SPORTS OFFICER'), ('pti', 'PTI'), ('supporting_staff', 'SUPPORTING STAFF'), ('faculty_advisor', 'FACULTY ADVISOR')], max_length=20),
        ),
    ]
