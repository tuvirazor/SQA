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
from base.models import proposal_folder, proposal_learning_unit


def create_learning_unit_proposal(person, folder_entity, folder_id, learning_unit_year, state_proposal,
                                  type_proposal, initial_data):
    folder, created = proposal_folder.ProposalFolder.objects.get_or_create(entity=folder_entity, folder_id=folder_id)

    proposal_learning_unit.ProposalLearningUnit.objects.create(folder=folder, learning_unit_year=learning_unit_year,
                                                               type=type_proposal, state=state_proposal,
                                                               initial_data=initial_data, author=person)
