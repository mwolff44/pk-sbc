# Generated by Django 2.1.5 on 2020-05-18 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyfb_kamailio', '0013_auto_20200514_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acccdr',
            name='company_id',
        ),
        migrations.AddField(
            model_name='acccdr',
            name='answered_time',
            field=models.DateTimeField(null=True, verbose_name='answered time'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='called_destination',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='called_did',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='caller_destination',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='did_destination',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='e164_called',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='e164_caller',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='kamailio_server',
            field=models.IntegerField(default=1, verbose_name='SIP server'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='leg_a_class',
            field=models.CharField(default='', help_text='on-net / off-net', max_length=128),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='leg_b_class',
            field=models.CharField(default='', help_text='on-net / off-net', max_length=128),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='media_server',
            field=models.IntegerField(null=True, verbose_name='Media server name'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='o_c_rate_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='o_c_rate_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='o_p_rate_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='o_p_rate_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='orig_customer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='orig_provider',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='sip_charge_info',
            field=models.CharField(help_text='Contents of the P-Charge-Info header for billing purpose.', max_length=100, null=True, verbose_name='charge info'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='sip_code',
            field=models.CharField(db_index=True, max_length=3, null=True, verbose_name='hangup SIP code'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='sip_reason',
            field=models.TextField(max_length=255, null=True, verbose_name='hangup SIP reason'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='sip_rtp_rxstat',
            field=models.CharField(max_length=30, null=True, verbose_name='sip rtp rx stat'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='sip_rtp_txstat',
            field=models.CharField(max_length=30, null=True, verbose_name='sip rtp tx stat'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='sip_user_agent',
            field=models.CharField(max_length=100, null=True, verbose_name='sip user agent'),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='t_c_rate_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='t_c_rate_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='t_p_rate_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='t_p_rate_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='term_customer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acccdr',
            name='term_provider',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='acccdr',
            name='callid',
            field=models.CharField(default='', max_length=128, verbose_name='a leg call-ID'),
        ),
        migrations.AlterField(
            model_name='acccdr',
            name='direction',
            field=models.CharField(default='', help_text='inbound / outbound', max_length=128),
        ),
    ]