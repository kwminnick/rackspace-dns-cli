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
Record interface
"""

from dnsclient import base

class Record(base.Resource):
    """
    A record.
    """
    
    HUMAN_ID = False
    NAME_ATTR = 'name'
    
    def __repr__(self):
        return "<Record: %s" % self.label
    
    def delete(self):
        self.manager.delete(self)

class RecordManager(base.ManagerWithFind):
    """
    Manage :class:`Record` resources.
    """
    
    resource_class = Record
        
    def list(self, domainId):
        """
        Get a list of all records for the domain.

        :rtype: list of :class:`Record`.
        """
        return self._list("/domains/%s/records" % base.getid(domainId), "records")
    
    def create(self, args, domainId):
        """
        Create a record in the dns system.  The following parameters are
        required type, name, data.
        
        :param type: str
        :param name: str
        :param ttl: int
        :param data: str
        :param priority: int
        :param comment: str
        
        :rtype: list of :class:`Record`
        """
        
        body = {
            "records" : [ {
                "name" : args.name,
                "comment" : args.comment,
                "ttl" : int(args.ttl),
                "type" : args.type,
                "data" : args.data,
                "priority" : args.priority                
            } ]
        }
        return self._create_async('/domains/%s/records' % base.getid(domainId), body, return_raw=False, response_key="")
