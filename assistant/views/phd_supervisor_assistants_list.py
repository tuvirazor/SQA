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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms import forms
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from assistant.business.users_access import user_is_phd_supervisor_and_procedure_is_open
from assistant.models import assistant_mandate, reviewer
from base.models import academic_year, entity_version


class AssistantsListView(LoginRequiredMixin, UserPassesTestMixin, ListView, FormMixin):
    context_object_name = 'phd_supervisor_assistants_list'
    template_name = 'phd_supervisor_assistants_list.html'
    form_class = forms.Form
    is_reviewer = False

    def test_func(self):
        return user_is_phd_supervisor_and_procedure_is_open(self.request.user)

    def get_login_url(self):
        return reverse('access_denied')

    def get_queryset(self):
        try:
            self.reviewer = reviewer.find_by_person(self.request.user.person)
            self.is_reviewer = True
        except ObjectDoesNotExist:
            self.is_reviewer = False
            self.reviewer = None
        return assistant_mandate.find_for_supervisor_for_academic_year(self.request.user.person,
                                                                       academic_year.current_academic_year())

    def get_context_data(self, **kwargs):
        context = super(AssistantsListView, self).get_context_data(**kwargs)
        context['year'] = academic_year.current_academic_year().year
        start_date = academic_year.current_academic_year().start_date
        context['is_reviewer'] = self.is_reviewer
        context['current_reviewer'] = self.reviewer
        if self.reviewer:
            entity = entity_version.get_last_version(self.reviewer.entity)
        else:
            entity = None
        context['entity'] = entity
        if self.is_reviewer:
            can_delegate = reviewer.can_delegate(reviewer.find_by_person(self.request.user.person))
            context['can_delegate'] = can_delegate
        else:
            context['can_delegate'] = False
        for mandate in context['object_list']:
            entities = []
            entities_id = mandate.mandateentity_set.all().order_by('id')
            for entity in entities_id:
                current_entityversion = entity_version.get_by_entity_and_date(entity.entity, start_date)[0]
                if current_entityversion is None:
                    current_entityversion = entity_version.get_last_version(entity.entity)
                entities.append(current_entityversion)
            mandate.entities = entities
        return context
