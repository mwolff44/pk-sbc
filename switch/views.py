# Create your tests here.
# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling. If not, see <http://www.gnu.org/licenses/>
# coding=UTF-8
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from datetime import datetime, timedelta
# import pygal
# from pygal.style import LightColorizedStyle
import psutil
import logging
import os
import platform
import psutil
import socket
import time

from switch import esl
from switch import psdash

from pyfreebilling import __version__


@staff_member_required
def fs_status_view(request):
    try:
        fs_status = esl.getFsStatus()
    except IOError:
        messages.error(request, """FS does not respond !""")
    try:
        sofia_status = esl.getSofiaStatus().replace("\t", u'\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0')
    except IOError:
        messages.error(request, """FS does not respond !""")
    try:
        fs_calls = esl.getFsCalls()
    except IOError:
        messages.error(request, """FS does not respond !""")
    try:
        fs_bcalls = esl.getFsBCalls()
    except IOError:
        messages.error(request, """FS does not respond !""")

    return render_to_response('admin/fs_status.html', locals(),
        context_instance=RequestContext(request))

@staff_member_required
def fs_registry_view(request):
    try:
        fs_status = esl.getFsRegistration()
    except IOError:
        messages.error(request, """FS does not respond !""")

    return render_to_response('admin/fs_status.html', locals(),
        context_instance=RequestContext(request))

@staff_member_required
def fs_bcalls_view(request):
    try:
        fs_status = esl.getFsBCalls()
    except IOError:
        messages.error(request, """FS does not respond !""")

    return render_to_response('admin/fs_status.html', locals(),
        context_instance=RequestContext(request))

# @staff_member_required
# def cpu_per(request):
#     cputimes = psutil.cpu_times_percent()
#     bar_chart = pygal.Bar(title=u'CPU % usage',print_values=True,pretty_print=True,print_zeroes=True)
#     bar_chart.add('user', cputimes.user)  # Add some values
#     bar_chart.add('system', cputimes.system)
#     bar_chart.add('idle', cputimes.idle)
#     return HttpResponse(bar_chart.render(), content_type="image/svg+xml")

@staff_member_required
def server_status_view(request):
    sysinfo = psdash.get_sysinfo()
    uptime = timedelta(seconds=sysinfo['uptime'])
    uptime = str(uptime).split('.')[0]
    memory = psdash.get_memory()
    mem_wo_c = memory['total'] - memory['available']
    netifs = psdash.get_network_interfaces().values()
    net_interfaces = netifs  #.sort(key=lambda x: x.get('bytes_sent'), reverse=True)
    os = sysinfo['os'].decode('utf-8')
    hostname = sysinfo['hostname'].decode('utf-8')
    uptime = uptime
    load_avg = sysinfo['load_avg']
    num_cpus = sysinfo['num_cpus']
    swap = psdash.get_swap_space()
    disks = psdash.get_disks()
    cpu = psdash.get_cpu()
    users = psdash.get_users()
    return render_to_response('admin/server_status.html', locals(),
        context_instance=RequestContext(request))