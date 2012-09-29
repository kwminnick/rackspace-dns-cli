# Copyright (c) 2012 Kevin Minnick
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from dnsclient import client

from dnsclient.v1_0 import domains
from dnsclient.v1_0 import records

class Client(object):
    """
    Top-level object to access the Rackspace DNS API.

    Create an instance with your creds::

        >>> client = Client(USERNAME, PASSWORD, PROJECT_ID, AUTH_URL)

    Then call methods on its managers::

        >>> client.domains.list()
        ...
        >>> client.subdomains.list()
        ...

    """
    
    def __init__(self, username, password, project_id, auth_url=None,
                  insecure=False, no_cache=False, http_log_debug=False,
                  auth_system='keystone'):
        
        self.domains = domains.DomainManager(self)
        self.records = records.RecordManager(self)
        
        self.client = client.HTTPClient(username,
                                    password,
                                    project_id,
                                    auth_url,
                                    insecure=insecure,
                                    service_type='rax:dns',
                                    no_cache=no_cache,
                                    http_log_debug=http_log_debug)
        
    def authenticate(self):
        """
        Authenticate against the server.

        Normally this is called automatically when you first access the API,
        but you can call this method to force authentication right now.

        Returns on success; raises :exc:`exceptions.Unauthorized` if the
        credentials are wrong.
        """
        self.client.authenticate()
