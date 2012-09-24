# Copyright 2012 Kevin Minnick
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

"""
Domain interface
"""

from dnsclient import base

class Domain(base.Resource):
    """
    A domain.
    """
    
    HUMAN_ID = False
    NAME_ATTR = 'name'
    
    def __repr__(self):
        return "<Domain: %s" % self.label
    
    def delete(self):
        self.manager.delete(self)

class DomainManager(base.ManagerWithFind):
    """
    Manage :class:`Domain` resources.
    """
    
    resource_class = Domain
    
    def limits(self):
        """
        Get current limits.
        
        :rtype: :class:`rates`
        """
        return self._get("/limits", "")
    
    def list(self):
        """
        Get a list of all domains.

        :rtype: list of :class:`Domain`.
        """
        return self._list("/domains", "domains")
    
    def get(self, domain):
        """
        Get a specific domain.

        :param domain: The ID of the :class:`Domain` to get.
        :rtype: :class:`Domain`
        """
        return self._get("/domains/%s" % base.getid(domain), "domain")  
    
    def export(self, domain):
        """
        Export a specific domain.
        
        :param domain: The ID of the :class:`Domain` to get.
        :rtype: :class:`Domain`
        """
        return self._get_async("/domains/%s/export" % base.getid(domain), "")
    
    def delete(self, domain):
        """
        Delete a specific domain.

        :param domain: The ID of the :class:`Domain` to delete.
        """
        self._delete("/domains/%s" % base.getid(domain))
        
    def create(self, args):
        """
        Create a domain in the dns system.  The following parameters are
        optional, except for name and email_address.
        
        :param name: str
        :param email_address: str
        :param ttl: int
        :param comment: str
        
        :rtype: list of :class:`Domain`
        """
        
        body = {
            "domains" : [ {
                "name" : args.name,
                "comment" : args.comment,
                "ttl" : int(args.ttl),
                "emailAddress" : args.email_address                
            } ]
        }
        return self._create_async('/domains', body, return_raw=False, response_key="")
