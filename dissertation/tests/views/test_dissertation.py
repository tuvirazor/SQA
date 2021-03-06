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

import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from base.tests.factories.academic_year import AcademicYearFactory
from base.tests.factories.offer_year import OfferYearFactory
from base.tests.factories.person import PersonFactory
from base.tests.factories.offer import OfferFactory
from base.tests.factories.student import StudentFactory
from dissertation.tests.factories.adviser import AdviserManagerFactory, AdviserTeacherFactory
from dissertation.tests.factories.dissertation import DissertationFactory
from dissertation.tests.factories.faculty_adviser import FacultyAdviserFactory
from dissertation.tests.factories.offer_proposition import OfferPropositionFactory
from dissertation.tests.factories.proposition_dissertation import PropositionDissertationFactory
from dissertation.tests.factories.proposition_offer import PropositionOfferFactory
from dissertation.models import adviser
from dissertation.models import dissertation_role
from dissertation.tests.models.test_faculty_adviser import create_faculty_adviser
from dissertation.views.dissertation import adviser_can_manage

ERROR_405_BAD_REQUEST=405
ERROR_404_PAGE_NO_FOUND = 404
HTTP_OK = 200
ERROR_403_NOT_AUTORIZED=403
MAXIMUM_IN_REQUEST=50


class DissertationViewTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.manager = AdviserManagerFactory()
        a_person_teacher = PersonFactory.create(first_name='Pierre', last_name='Dupont')
        self.teacher = AdviserTeacherFactory(person=a_person_teacher)
        a_person_teacher2 = PersonFactory.create(first_name='Marco', last_name='Millet')
        self.teacher2 = AdviserTeacherFactory(person=a_person_teacher2)
        a_person_student = PersonFactory.create(last_name="Durant", user=None)
        student = StudentFactory.create(person=a_person_student)
        self.offer1 = OfferFactory(title="test_offer1")
        self.offer2 = OfferFactory(title="test_offer2")
        self.academic_year1 = AcademicYearFactory()
        self.academic_year2 = AcademicYearFactory(year=self.academic_year1.year-1)
        self.offer_year_start1 = OfferYearFactory(acronym="test_offer1", offer=self.offer1,
                                             academic_year=self.academic_year1)
        offer_year_start2 = OfferYearFactory(academic_year=self.academic_year2, acronym="test_offer2", offer=self.offer1)
        self.offer_proposition1 = OfferPropositionFactory(offer=self.offer1)
        self.offer_proposition2 = OfferPropositionFactory(offer=self.offer2)
        FacultyAdviserFactory(adviser=self.manager, offer=self.offer1)
        self.manager2 = AdviserManagerFactory()
        FacultyAdviserFactory(adviser=self.manager, offer=self.offer2)
        roles = ['PROMOTEUR', 'CO_PROMOTEUR', 'READER', 'PROMOTEUR', 'ACCOMPANIST', 'PRESIDENT']
        status = ['DRAFT', 'COM_SUBMIT', 'EVA_SUBMIT', 'TO_RECEIVE', 'DIR_SUBMIT', 'DIR_SUBMIT']
        self.dissertations_list = list()
        for x in range(0, 6):
            proposition_dissertation = PropositionDissertationFactory(author=self.teacher,
                                                                      creator=a_person_teacher,
                                                                      title='Proposition {}'.format(x)
                                                                      )
            PropositionOfferFactory(proposition_dissertation=proposition_dissertation,
                                    offer_proposition=self.offer_proposition1)

            self.dissertations_list.append(DissertationFactory(author=student,
                                title='Dissertation {}'.format(x),
                                offer_year_start=self.offer_year_start1,
                                proposition_dissertation=proposition_dissertation,
                                status=status[x],
                                active=True,
                                dissertation_role__adviser=self.teacher,
                                dissertation_role__status=roles[x]
                                ))
        self.dissertation_1 = DissertationFactory\
            (author=student,
            title='Dissertation 2017',
            offer_year_start=self.offer_year_start1,
            proposition_dissertation=proposition_dissertation,
            status='COM_SUBMIT',
            active=True,
            dissertation_role__adviser=self.teacher2,
            dissertation_role__status='PROMOTEUR')

    def test_get_dissertations_list_for_teacher(self):
        self.client.force_login(self.teacher.person.user)
        url = reverse('dissertations_list')
        response = self.client.get(url)
        self.assertEqual(response.context[-1]['adviser_list_dissertations'].count(), 1)  # only 1 because 1st is DRAFT
        self.assertEqual(response.context[-1]['adviser_list_dissertations_copro'].count(), 1)
        self.assertEqual(response.context[-1]['adviser_list_dissertations_reader'].count(), 1)
        self.assertEqual(response.context[-1]['adviser_list_dissertations_accompanist'].count(), 1)
        self.assertEqual(response.context[-1]['adviser_list_dissertations_president'].count(), 1)

    def test_get_dissertations_list_for_manager(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_list')
        response = self.client.get(url)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)
        self.assertCountEqual(response.context[-1]['dissertations'],[self.dissertation_1]+self.dissertations_list)

    def test_search_dissertations_for_manager_1(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "no result search"})
        self.assertEqual(response.status_code, 200)


    def test_search_dissertations_for_manager_2(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Dissertation 2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 2)
        self.assertCountEqual(
            response.context[-1]['dissertations'],
            [self.dissertation_1, self.dissertations_list[2]]
        )

    def test_search_dissertations_for_manager_3(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Proposition 3"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 1)
        self.assertCountEqual(
            response.context[-1]['dissertations'],
            [self.dissertations_list[3]]
        )

    def test_search_dissertations_for_manager_4(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Dissertation"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)

    def test_search_dissertations_for_manager_5(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Dissertation",
                                              "offer_prop_search": self.offer_proposition1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)

    def test_search_dissertations_for_manager_6(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Dissertation",
                                              "offer_prop_search": self.offer_proposition2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 0)

    def test_search_dissertations_for_manager_7(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"academic_year": self.academic_year1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)

    def test_search_dissertations_for_manager_8(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"academic_year": self.academic_year2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 0)

    def test_search_dissertations_for_manager_9(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"status_search": "COM_SUBMIT"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 2)

    def test_search_dissertations_for_manager_10(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "test_offer"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)

    def test_search_dissertations_for_manager_11(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Durant"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)

    def test_search_dissertations_for_manager_12(self):
        self.client.force_login(self.manager.person.user)
        url = reverse('manager_dissertations_search')
        response = self.client.get(url, data={"search": "Dupont"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['dissertations'].count(), 7)

    def test_adviser_can_manage_dissertation(self):
        manager = AdviserManagerFactory()
        manager2 = AdviserManagerFactory()
        a_person_teacher = PersonFactory.create(first_name='Pierre', last_name='Dupont')
        a_person_teacher2 = PersonFactory.create(first_name='Marco', last_name='Millet')
        teacher = AdviserTeacherFactory(person=a_person_teacher)
        teacher2 = AdviserTeacherFactory(person=a_person_teacher2)
        a_person_student = PersonFactory.create(last_name="Durant", user=None)
        student = StudentFactory.create(person=a_person_student)
        offer_year_start = OfferYearFactory(academic_year=self.academic_year1, acronym="test_offer2")
        offer_year_start2 = OfferYearFactory(acronym="test_offer3", academic_year=offer_year_start.academic_year)
        offer = offer_year_start.offer
        offer2 = offer_year_start2.offer
        FacultyAdviserFactory(adviser=manager, offer=offer)
        create_faculty_adviser(manager, offer)
        create_faculty_adviser(manager2, offer2)
        proposition_dissertation = PropositionDissertationFactory(author=teacher,
                                                                  creator=a_person_teacher,
                                                                  title='Proposition1')
        dissertation = DissertationFactory(author=student,
                                           title='Dissertation 2017',
                                           offer_year_start=offer_year_start,
                                           proposition_dissertation=proposition_dissertation,
                                           status='DIR_SUBMIT',
                                           active=True,
                                           dissertation_role__adviser=teacher,
                                           dissertation_role__status='PROMOTEUR')
        self.assertEqual(adviser_can_manage(dissertation, manager), True)
        self.assertEqual(adviser_can_manage(dissertation, manager2), False)
        self.assertEqual(adviser_can_manage(dissertation, teacher), False)

    def test_get_all_advisers(self):
        res = adviser.find_all_advisers()
        self.assertEqual(res.count(), 4)

    def test_find_by_last_name_or_email(self):
        res = adviser.find_advisers_last_name_email('Dupont', MAXIMUM_IN_REQUEST)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].person.last_name, 'Dupont')
        res = adviser.find_advisers_last_name_email(None, MAXIMUM_IN_REQUEST)
        self.assertEqual(len(res), 0)

    def test_get_adviser_list_json(self):
        self.client.force_login(self.manager.person.user)
        response = self.client.get('/dissertation/find_adviser_list/', {'term': 'Dupont'})
        self.assertEqual(response.status_code, HTTP_OK)
        data_json = response.json()
        self.assertNotEqual(len(data_json), 0)
        for data in data_json:
            self.assertEqual(data['last_name'], 'Dupont')

    def test_manager_dissert_jury_new_by_ajax1(self):
        self.client.force_login(self.manager.person.user)
        dissert_role_count = dissertation_role.count_by_dissertation(self.dissertation_1)
        response = self.client.post('/dissertation/manager_dissertations_jury_new_ajax/',
                                    {'pk_dissertation': str(self.dissertation_1.id)})
        self.assertEqual(response.status_code, ERROR_405_BAD_REQUEST)
        response = self.client.get('/dissertation/manager_dissertations_jury_new_ajax/', {
            'pk_dissertation': str(self.dissertation_1.id)})
        self.assertEqual(response.status_code, ERROR_405_BAD_REQUEST)
        response = self.client.post('/dissertation/manager_dissertations_jury_new_ajax/',
                                    {'pk_dissertation': str(self.dissertation_1.id), 'status_choice': 'READER'})
        self.assertEqual(response.status_code, ERROR_405_BAD_REQUEST)
        response = self.client.post('/dissertation/manager_dissertations_jury_new_ajax/',
                                    {'pk_dissertation': str(self.dissertation_1.id),
                                     'status_choice': 'READER',
                                     'adviser_pk': str(self.teacher.id)})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(dissert_role_count + 1, dissertation_role.count_by_dissertation(self.dissertation_1))

    def test_manager_dissert_jury_del_by_ajax(self):
        self.client.force_login(self.manager.person.user)
        response = self.client.post('/dissertation/manager_dissertations_jury_new_ajax/',
                                    {'pk_dissertation': str(self.dissertation_1.id),
                                     'status_choice': 'READER',
                                     'adviser_pk': str(self.teacher.id)})
        self.assertEqual(response.status_code, HTTP_OK)
        liste_dissert_roles = dissertation_role.search_by_dissertation_and_role(self.dissertation_1, 'READER')
        self.assertNotEqual(len(liste_dissert_roles),0)
        for element in liste_dissert_roles:
            dissert_role_count = dissertation_role.count_by_dissertation(self.dissertation_1)
            url = "/dissertation/manager_dissertations_role_delete_by_ajax/{role}"
            response2 = self.client.get(url.format(role=str(element.id)))
            self.assertEqual(response2.status_code, HTTP_OK)
            self.assertEqual(dissertation_role.count_by_dissertation(self.dissertation_1), dissert_role_count-1)

    def test_manager_dissert_wait_comm_jsonlist(self):
        self.client.force_login(self.manager.person.user)
        response = self.client.post('/dissertation/manager_dissertations_wait_comm_json_list', )
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(len(response_data), 2)

    def test_manager_dissert_jury_security_ajax(self):
        self.client.force_login(self.manager2.person.user)
        response = self.client.post('/dissertation/manager_dissertations_jury_new_ajax/',
                                    {'pk_dissertation': str(self.dissertation_1.id),
                                     'status_choice': 'READER',
                                     'adviser_pk': str(self.teacher.id)})
        self.assertEqual(response.status_code, ERROR_403_NOT_AUTORIZED)
        liste_dissert_roles = dissertation_role.search_by_dissertation_and_role(self.dissertation_1, 'READER')
        for element in liste_dissert_roles:
            url = "/dissertation/manager_dissertations_role_delete_by_ajax/{role}"
            response = self.client.get(url.format(role=str(element.id)))
            self.assertEqual(response.status_code, ERROR_403_NOT_AUTORIZED)
