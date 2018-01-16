##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils import formats
from django.utils.translation import ugettext as _
from osis_common.utils.datetime import is_in_chronological_order
from base.signals.publisher import compute_scores_encodings_deadlines


class OfferYearCalendarAdmin(admin.ModelAdmin):
    list_display = ('academic_calendar', 'offer_year', 'start_date', 'end_date', 'changed', 'education_group_year')
    fieldsets = ((None, {'fields': ('offer_year', 'academic_calendar', 'start_date', 'end_date',
                                    'education_group_year')}),)
    raw_id_fields = ('offer_year', 'education_group_year')
    search_fields = ['offer_year__acronym']
    list_filter = ('academic_calendar__academic_year', 'academic_calendar__reference',)


class OfferYearCalendar(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed = models.DateTimeField(null=True, auto_now=True)
    academic_calendar = models.ForeignKey('AcademicCalendar')
    offer_year = models.ForeignKey('OfferYear')
    start_date = models.DateTimeField(blank=True, null=True, db_index=True)
    end_date = models.DateTimeField(blank=True, null=True, db_index=True)
    education_group_year = models.ForeignKey('EducationGroupYear', blank=True, null=True)

    class Meta:
        unique_together = ('academic_calendar', 'education_group_year')

    def clean(self):
        try:
            self.end_start_dates_validation()
        except AttributeError as e:
            raise ValidationError(e)

        if not hasattr(self, 'academic_calendar'):
            return None

        self._check_is_in_calendar_range(self.start_date)
        self._check_is_in_calendar_range(self.end_date)

    def _check_is_in_calendar_range(self, date):
        if date and not self.academic_calendar.start_date <= date.date() <= self.academic_calendar.end_date:
            info = {
                "date": formats.localize_input(date.date()),
                "start_date": formats.localize_input(self.academic_calendar.start_date),
                "end_date": formats.localize_input(self.academic_calendar.end_date),
            }
            raise ValidationError(_('%(date)s must be set within %(start_date)s and %(end_date)s'), params=info)

    def save(self, *args, **kwargs):
        self.end_start_dates_validation()
        super(OfferYearCalendar, self).save(*args, **kwargs)
        compute_scores_encodings_deadlines.send(sender=self.__class__, offer_year_calendar=self)

    def end_start_dates_validation(self):
        if self._dates_are_set() and not is_in_chronological_order(self.start_date, self.end_date):
            raise AttributeError(_('end_start_date_error'))

    def _dates_are_set(self):
        return bool(self.start_date and self.end_date)

    def __str__(self):
        return u"%s - %s" % (self.academic_calendar, self.offer_year)


def find_offer_year_events(offer_yr):
    return OfferYearCalendar.objects.filter(offer_year=offer_yr,
                                            start_date__isnull=False,
                                            end_date__isnull=False).order_by('start_date',
                                                                             'academic_calendar__title')


def find_by_id(offer_year_calendar_id):
    return OfferYearCalendar.objects.get(pk=offer_year_calendar_id)


def find_by_offer_year(offer_yr, academic_calendar_type=None):
    queryset = OfferYearCalendar.objects.filter(offer_year=offer_yr)
    if academic_calendar_type:
        queryset = queryset.filter(academic_calendar__reference=academic_calendar_type)
    return queryset


def find_latest_end_date_by_academic_calendar(academic_calendar_id):
    try:
        return OfferYearCalendar.objects.filter(academic_calendar_id=academic_calendar_id) \
            .filter(end_date__isnull=False) \
            .latest('end_date')
    except ObjectDoesNotExist:
        return None


def find_by_education_group_year(education_group_year):
    return OfferYearCalendar.objects.filter(education_group_year=education_group_year)


def get_by_education_group_year_and_academic_calendar(an_academic_calendar, an_education_group_year):
    try:
        return OfferYearCalendar.objects.get(academic_calendar=an_academic_calendar,
                                             education_group_year=an_education_group_year)
    except ObjectDoesNotExist:
        return None


def search(education_group_year_id=None, academic_calendar_reference=None, number_session=None, offer_year=None):

    queryset = OfferYearCalendar.objects

    if education_group_year_id is not None:
        queryset = queryset.filter(education_group_year=education_group_year_id)

    if academic_calendar_reference is not None:
        if isinstance(academic_calendar_reference, list):
            queryset = queryset.filter(academic_calendar__reference__in=academic_calendar_reference)
        else:
            queryset = queryset.filter(academic_calendar__reference=academic_calendar_reference)

    if number_session:
        queryset = queryset.filter(academic_calendar__sessionexamcalendar__number_session=number_session)

    if offer_year:
        queryset = queryset.filter(offer_year=offer_year)

    return queryset
