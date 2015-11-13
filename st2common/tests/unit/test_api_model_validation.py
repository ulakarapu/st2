# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2

from st2common.models.api.base import BaseAPI

__all__ = [
    'APIModelValidationTestCase'
]


class MockAPIModel(BaseAPI):
    model = None
    schema = {
        'title': 'MockAPIModel',
        'description': 'Test',
        'type': 'object',
        'properties': {
            'id': {
                'description': 'The unique identifier for the action runner.',
                'type': ['string', 'null'],
                'default': None
            },
            'name': {
                'description': 'The name of the action runner.',
                'type': 'string',
                'required': True
            },
            'description': {
                'description': 'The description of the action runner.',
                'type': 'string'
            },
            'enabled': {
                'type': 'boolean',
                'default': True
            },
            'parameters': {
                'type': 'object'
            },
            'permission_grants': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'resource_uid': {
                            'type': 'string',
                            'description': 'UID of a resource to which this grant applies to.',
                            'required': False,
                            'default': 'unknown'
                        },
                        'enabled': {
                            'type': 'boolean',
                            'default': True
                        },
                        'description': {
                            'type': 'string',
                            'description': 'Description',
                            'required': False
                        }
                    }
                },
                'default': []
            }
        },
        'additionalProperties': False
    }


class APIModelValidationTestCase(unittest2.TestCase):
    def test_validate_default_values_are_set(self):
        # no "permission_grants" attribute
        mock_model_api = MockAPIModel(name='name')
        self.assertEqual(getattr(mock_model_api, 'id', 'notset'), 'notset')
        self.assertEqual(mock_model_api.name, 'name')
        self.assertEqual(getattr(mock_model_api, 'enabled', None), None)
        self.assertEqual(getattr(mock_model_api, 'permission_grants', None), None)

        mock_model_api_validated = mock_model_api.validate()

        # Validate it doesn't modify object in place
        self.assertEqual(getattr(mock_model_api, 'id', 'notset'), 'notset')
        self.assertEqual(mock_model_api.name, 'name')
        self.assertEqual(getattr(mock_model_api, 'enabled', None), None)

        # Verify cleaned object
        self.assertEqual(mock_model_api_validated.id, None)
        self.assertEqual(mock_model_api_validated.name, 'name')
        self.assertEqual(mock_model_api_validated.enabled, True)
        self.assertEqual(mock_model_api_validated.permission_grants, [])

        # "permission_grants" attribute present, but child missing
        mock_model_api = MockAPIModel(name='name', enabled=False,
                                      permission_grants=[{}, {'description': 'test'}])
        self.assertEqual(mock_model_api.name, 'name')
        self.assertEqual(mock_model_api.enabled, False)
        self.assertEqual(mock_model_api.permission_grants, [{}, {'description': 'test'}])

        mock_model_api_validated = mock_model_api.validate()

        # Validate it doesn't modify object in place
        self.assertEqual(mock_model_api.name, 'name')
        self.assertEqual(mock_model_api.enabled, False)
        self.assertEqual(mock_model_api.permission_grants, [{}, {'description': 'test'}])

        # Verify cleaned object
        self.assertEqual(mock_model_api_validated.id, None)
        self.assertEqual(mock_model_api_validated.name, 'name')
        self.assertEqual(mock_model_api_validated.enabled, False)
        self.assertEqual(mock_model_api_validated.permission_grants,
                         [{'resource_uid': 'unknown', 'enabled': True},
                          {'resource_uid': 'unknown', 'enabled': True, 'description': 'test'}])