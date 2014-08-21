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

from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.admin.views.decorators import staff_member_required

from switch import esl

from pyfreebilling import __version__

@staff_member_required
def fs_status_view(request):
    fs_status = esl.getFsStatus()
    sofia_status = esl.getSofiaStatus().replace("\t", u'\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0')
    fs_calls = esl.getFsCalls()
    fs_bcalls = esl.getFsBCalls()

    return render_to_response('admin/fs_status.html', locals(),
        context_instance=RequestContext(request))