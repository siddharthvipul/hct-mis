# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestGrievanceApproveDataChangeMutation::test_approve_update_individual 1'] = {
    'data': {
        'approveIndividualDataChange': {
            'grievanceTicket': {
                'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTphY2Q1N2FhMS1lZmQ4LTRjODEtYWMxOS1iOGNhYmViZTgwODk=',
                'individualDataUpdateTicketDetails': {
                    'individualData': {
                        'birth_date': {
                            'approve_status': False,
                            'value': '1980-02-01'
                        },
                        'documents': [
                            {
                                'approve_status': True,
                                'value': {
                                    'country': 'POL',
                                    'number': '999-888-777',
                                    'type': 'NATIONAL_ID'
                                }
                            }
                        ],
                        'documents_to_remove': [
                            {
                                'approve_status': True,
                                'value': 'RG9jdW1lbnROb2RlOmRmMWNlNmU4LTI4NjQtNGMzZi04MDNkLTE5ZWM2ZjRjNDdmMw=='
                            },
                            {
                                'approve_status': False,
                                'value': 'RG9jdW1lbnROb2RlOjhhZDVlM2I4LTRjNGQtNGMxMC04NzU2LTExOGQ4NjA5NWRkMA=='
                            }
                        ],
                        'family_name': {
                            'approve_status': True,
                            'value': 'Example'
                        },
                        'flex_fields': {
                        },
                        'full_name': {
                            'approve_status': True,
                            'value': 'Test Example'
                        },
                        'given_name': {
                            'approve_status': True,
                            'value': 'Test'
                        },
                        'marital_status': {
                            'approve_status': False,
                            'value': 'SINGLE'
                        },
                        'sex': {
                            'approve_status': False,
                            'value': 'MALE'
                        }
                    }
                }
            }
        }
    }
}
