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
        url = '/domains/%s/records' % base.getid(domainId)
        
        if args.type == "PTR":
            url = '/rdns'
            body = {
                "recordsList" : {
                    "records" : [ {
                                   "name" : args.name,
                                   "comment" : args.comment,
                                   "ttl" : int(args.ttl),
                                   "type" : args.type,
                                   "data" : args.data               
                                   } ]
                    },
                "link" : {
                    "content" : "",
                    "href" : args.server_href,
                    "rel" : "cloudServersOpenStack"
                }
            }      
        
        return self._create_async(url, body, return_raw=False, response_key="")

    def modify(self, args, domainId):
        """
        Modify a record in the dns system.  The following parameters are
        required recordId and name.
        
        :param record_id: str
        :param domain: str
        :param name: str
        :param ttl: int
        :param data: str
        :param priority: int
        :param comment: str
        
        :rtype: list of :class:`Record`
        """
        
        body = {
            "name" : args.name,
            "comment" : args.comment,
            "ttl" : int(args.ttl),
            "data" : args.data,
            "priority" : args.priority                
        }
        url = '/domains/%s/records/%s' % (base.getid(domainId), base.getid(args.record_id))
        
        if hasattr(args, 'type'):
            if args.type == "PTR":
                url = '/rdns'
                body = {
                        "recordsList" : {
                                "records" : [ {
                                   "name" : args.name,
                                   "id" : args.record_id,
                                   "comment" : args.comment,
                                   "ttl" : int(args.ttl),
                                   "type" : args.type,
                                   "data" : args.data               
                                   } ]
                        },
                        "link" : {
                                  "content" : "",
                                  "href" : args.server_href,
                                  "rel" : "cloudServersOpenStack"
                        }
                }      

        return self._update(url, body, return_raw=False, response_key="")

    def delete(self, domainId, recordId):
        """
        Delete a specific record.

        :param domainId: The ID of the :class:`Domain` to delete.
        :param recordId: The ID of the :class:`Record` to delete.
        """
        self._delete("/domains/%s/records/%s" % (base.getid(domainId), base.getid(recordId)))
        
    def rdns_list(self, href):     
        """
        List all PTR records configured for the specified Cloud device.

        :param href: The href of the device to get .
        :rtype: :class:`Record`
        """
        return self._list("/rdns/cloudServersOpenStack?href=%s" % href, "records") 

    def rdns_delete(self, href, ip):
        """
        Remove one or all PTR records associated with a Rackspace Cloud device. 
        Use the optional ip query parameter to specify a specific record to delete. 
        Omitting this parameter removes all PTR records associated with the specified device.

        :param href: The ID of the device to delete.
        :param ip: The ip of the specific record to delete.
        """
        self._delete("/rdns/cloudServersOpenStack?href=%s&ip=%s" % (href, ip))
