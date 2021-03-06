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
from base.models import entity_container_year, proposal_learning_unit, entity
from base.models.academic_year import current_academic_year
from base.models.enums import learning_unit_year_subtypes, proposal_type, learning_container_year_types
from base.models.enums.entity_container_year_link_type import REQUIREMENT_ENTITY
from base.models.enums.learning_unit_year_subtypes import PARTIM
from base.models.enums.proposal_state import ProposalState
from base.models.enums.proposal_type import ProposalType
from base.models.learning_unit import is_old_learning_unit
from base.models.utils.person_entity_filter import filter_by_attached_entities

TYPES_PROPOSAL_NEEDED_TO_EDIT = (learning_container_year_types.COURSE,
                                 learning_container_year_types.DISSERTATION,
                                 learning_container_year_types.INTERNSHIP)
PROPOSAL_TYPE_ACCEPTED_FOR_UPDATE = (proposal_type.ProposalType.CREATION.name,
                                     proposal_type.ProposalType.MODIFICATION.name,
                                     proposal_type.ProposalType.TRANSFORMATION.name)
CANCELLABLE_PROPOSAL_TYPES = (ProposalType.MODIFICATION.name,
                              ProposalType.TRANSFORMATION.name,
                              ProposalType.TRANSFORMATION_AND_MODIFICATION.name)


def is_person_linked_to_entity_in_charge_of_learning_unit(a_person, a_learning_unit_year):
    entity_containers_year = entity_container_year.search(
        learning_container_year=a_learning_unit_year.learning_container_year,
        link_type=REQUIREMENT_ENTITY)

    return filter_by_attached_entities(a_person, entity_containers_year).exists()


def is_eligible_to_create_modification_proposal(learn_unit_year, person):
    if _learning_unit_year_is_past(learn_unit_year) or \
            learn_unit_year.subtype == learning_unit_year_subtypes.PARTIM:
        return False
    if learn_unit_year.learning_container_year and \
            learn_unit_year.learning_container_year.container_type not in TYPES_PROPOSAL_NEEDED_TO_EDIT:
        return False
    if _learning_unit_year_is_on_proposal(learn_unit_year):
        return False

    return person.is_linked_to_entity_in_charge_of_learning_unit_year(learn_unit_year)


def is_eligible_for_cancel_of_proposal(learning_unit_proposal, a_person):
    if not learning_unit_proposal or learning_unit_proposal.state != ProposalState.FACULTY.name:
        return False

    if learning_unit_proposal.type not in CANCELLABLE_PROPOSAL_TYPES:
        return False

    initial_entity_requirement_id = learning_unit_proposal.initial_data["entities"][REQUIREMENT_ENTITY]
    an_entity = entity.get_by_internal_id(initial_entity_requirement_id)
    if an_entity in a_person.entities:
        return True

    return a_person.is_linked_to_entity_in_charge_of_learning_unit_year(learning_unit_proposal.learning_unit_year)


def is_eligible_to_edit_proposal(proposal, a_person):
    if not proposal:
        return False

    is_person_linked_to_entity = a_person.is_linked_to_entity_in_charge_of_learning_unit_year(
        proposal.learning_unit_year)

    if a_person.is_faculty_manager():
        if (proposal.state != ProposalState.FACULTY.name or
                proposal.type not in PROPOSAL_TYPE_ACCEPTED_FOR_UPDATE or
                not is_person_linked_to_entity):
            return False

    return a_person.user.has_perm('base.can_edit_learning_unit_proposal')


def is_eligible_for_modification_end_date(learn_unit_year, a_person):
    if is_old_learning_unit(learn_unit_year.learning_unit):
        return False
    if proposal_learning_unit.find_by_learning_unit_year(learn_unit_year):
        return False
    if a_person.is_faculty_manager() and not _can_faculty_manager_modify_end_date(learn_unit_year):
        return False
    return a_person.is_linked_to_entity_in_charge_of_learning_unit_year(learn_unit_year)


def is_eligible_for_modification(learn_unit_year, person):
    if _learning_unit_year_is_past(learn_unit_year):
        return False
    if _learning_unit_year_is_on_proposal(learn_unit_year):
        return False
    return person.is_linked_to_entity_in_charge_of_learning_unit_year(learn_unit_year)


def _can_faculty_manager_modify_end_date(learning_unit_year):
    if learning_unit_year.learning_container_year:
        if learning_unit_year.subtype == PARTIM:
            return True
        return learning_unit_year.learning_container_year.container_type not in TYPES_PROPOSAL_NEEDED_TO_EDIT
    return False


def _learning_unit_year_is_past(learn_unit_year):
    current_year = current_academic_year().year
    return learn_unit_year.academic_year.year < current_year


def _learning_unit_year_is_on_proposal(learn_unit_year):
    proposal = proposal_learning_unit.find_by_learning_unit_year(learn_unit_year)
    return proposal is not None


def can_delete_learning_unit_year(learning_unit_year, person):
    if not person.is_linked_to_entity_in_charge_of_learning_unit_year(learning_unit_year):
        return False
    return _can_delete_learning_unit_year_according_type(learning_unit_year, person)


def _can_delete_learning_unit_year_according_type(learning_unit_year, person):
    if not person.is_central_manager() and person.is_faculty_manager():
        container_type = learning_unit_year.learning_container_year.container_type
        subtype = learning_unit_year.subtype

        return not (
                container_type == learning_container_year_types.COURSE and subtype == learning_unit_year_subtypes.FULL
        ) and container_type not in [learning_container_year_types.DISSERTATION,
                                     learning_container_year_types.INTERNSHIP]
    return True
