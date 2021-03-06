##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2018 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def show_success_learning_unit_year_creation_message(request, learning_unit_year_created, translation_key):
    link = reverse("learning_unit", kwargs={'learning_unit_year_id': learning_unit_year_created.id})
    success_msg = _(translation_key) % {'link': link, 'acronym': learning_unit_year_created.acronym,
                                        'academic_year': learning_unit_year_created.academic_year}
    messages.add_message(request, messages.SUCCESS, success_msg, extra_tags='safe')
