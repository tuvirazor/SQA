##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
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
from django import forms
from base import models as mdl
from django.core.exceptions import ValidationError
from base.enums import learning_unit_year_status
from base.enums import learning_unit_year_types
from base.enums import learning_units_errors

class LearningUnitYearForm(forms.Form):

    academic_year=forms.CharField(max_length=10, required=False)
    acronym = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}),max_length=20, required=False)
    keyword = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}),max_length=20, required=False)
    type = forms.CharField(
        widget=forms.Select(choices=learning_unit_year_types.LEARNING_UNIT_YEAR_TYPES),
        required=False
    )
    status=forms.CharField(
        widget=forms.Select(choices=learning_unit_year_status.LEARNING_UNIT_YEAR_STATUS),
        required=False
    )

    def clean(self):
        #Cleaning data, normalizing values coming from the user
        clean_data = self.cleaned_data
        academic_year = lambda : '' if self.cleaned_data.get('academic_year')=='0' else self.cleaned_data.get('academic_year')
        status = lambda : '' if self.cleaned_data.get('status')=="NONE" else self.cleaned_data.get('status')
        type = lambda : '' if self.cleaned_data.get('type')=="NONE" else self.cleaned_data.get('type')
        acronym = clean_data.get('acronym').upper()
        keyword = clean_data.get('keyword')
        #Save final values in cleaned_data for other use
        self.cleaned_data['academic_year'] = academic_year()
        self.cleaned_data['status'] = status()
        self.cleaned_data['type'] = type()
        self.cleaned_data['acronym'] = acronym
        minimal_inputs_not_satisfied = lambda : True if (not self.cleaned_data.get('acronym')
                                                         and not self.cleaned_data.get('keyword')
                                                         and not self.cleaned_data.get('type')
                                                         and not self.cleaned_data.get('status')) else False
        if minimal_inputs_not_satisfied():
            raise ValidationError(learning_units_errors.INVALID_SEARCH)
        elif not academic_year():
            check_when_academic_year_is_all(acronym)
        return clean_data

    def set_academic_years_all(self):
        academic_years_all = True if not self.cleaned_data.get('academic_year') else False
        return academic_years_all

    def get_learning_units(self):
        clean_data = self.cleaned_data
        academic_year = clean_data.get('academic_year')
        acronym = clean_data.get('acronym')
        keyword = clean_data.get('keyword')
        status = clean_data.get('status')
        type = clean_data.get('type')

        if not academic_year and acronym and not keyword and not type and not status:
            learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
        else:
            learning_units = mdl.learning_unit_year.search(academic_year_id=academic_year,acronym=acronym,title=keyword,type=type,status=status)
        return learning_units

    def get_academic_year(self):
        academic_year = 0 if not self.cleaned_data.get('academic_year') else self.cleaned_data.get('academic_year')
        return academic_year

def check_when_academic_year_is_all(acronym):
    if (acronym):
        check_learning_units_with_acronym(acronym)
    elif (not acronym):
        raise ValidationError(learning_units_errors.ACADEMIC_YEAR_REQUIRED)

def check_learning_units_with_acronym(acronym):
        learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
        if not learning_units:
           raise ValidationError(learning_units_errors.ACADEMIC_YEAR_WITH_ACRONYM)