# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack LLC.
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

import json

from dnsclient import utils

def do_domain_list(cs, args):
    """Print a list of available domains."""
    domain_list = cs.domains.list()
    columns = ['ID', 'Name', 'emailAddress']
    utils.print_list(domain_list, columns)
    
@utils.arg('domain',
     metavar='<domain>',
     help="name of domain")
def do_domain_show(cs, args):
    """Show details about the given domain"""
    domainId = utils.find_resource(cs.domains, args.domain)
    domain = cs.domains.get(domainId)
    print json.dumps(domain._info, sort_keys=True, indent=4)

@utils.arg('domain',
           metavar='<domain>',
           help="name of domain")
def do_domain_export(cs, args):
    """Export details of the specified domain."""
    domain = utils.find_resource(cs.domains, args.domain)
    domain = cs.domains.export(domain.id)
    utils.print_dict(domain._info)

def do_limits(cs, args):
    """List all applicable limits."""
    limits = cs.domains.limits()
    print json.dumps(limits._info, sort_keys=True, indent=4)

@utils.arg('name',
           metavar='name',
           help="Specifies the name for the domain or subdomain. Must be a valid domain name.")
@utils.arg('--email-address',
           metavar='<email-address>',
           required=True,
           help="Email address to use for contacting the domain administrator.")
@utils.arg('--ttl',
           default=3600,
           metavar='<ttl>',
           help="If specified, must be greater than 300. The default value, if not specified, is 3600.")
@utils.arg('--comment',
           default=None,
           metavar='<comment>',
           help="If included, its length must be less than or equal to 160 characters.")
def do_domain_create(cs, args):
    """Create a new domain."""
    domain = cs.domains.create(args)
    print json.dumps(domain._info, sort_keys=True, indent=4)
    
@utils.arg('domain',
           metavar='<domain>',
           help="name of domain")
def do_domain_delete(cs, args):
    """Delete a domain by name."""
    domain = utils.find_resource(cs.domains, args.domain)
    cs.domains.delete(domain.id)

@utils.arg('domain',
     metavar='<domain>',
     help="name of domain")
@utils.arg('--email-address',
           metavar='<email-address>',
           help="Email address to use for contacting the domain administrator.")
@utils.arg('--ttl',
           default=3600,
           metavar='<ttl>',
           help="If specified, must be greater than 300. The default value, if not specified, is 3600.")
@utils.arg('--comment',
           default=None,
           metavar='<comment>',
           help="If included, its length must be less than or equal to 160 characters.")
def do_domain_modify(cs, args):
    """Modify a domain."""
    domainId = utils.find_resource(cs.domains, args.domain)
    cs.domains.modify(args, domainId)
    
@utils.arg('domain',
           metavar='<domain>',
           help="name of domain")
def do_subdomain_list(cs, args):
    """Print a list of available sub-domains for the given domain."""
    domainId = utils.find_resource(cs.domains, args.domain)
    domain_list = cs.domains.subdomains_list(domainId)
    columns = ['ID', 'Name', 'emailAddress']
    utils.print_list(domain_list, columns)
    
@utils.arg('domain',
           metavar='<domain>',
           help="name of domain")
def do_record_list(cs, args):
    """Print a list of records for the given domain."""
    domainId = utils.find_resource(cs.domains, args.domain)
    record_list = cs.records.list(domainId)
    columns = ['ID', 'Name', 'Type', "Data", "TTL", "Priority", "Comment"]
    utils.print_list(record_list, columns)
    
@utils.arg('domain',
           metavar='name',
           help="Specifies the domain or subdomain. Must be a valid existing domain (example.com)")
@utils.arg('--name',
           metavar='<name>',
           required=True,
           help="The full name of the new record (ftp.example.com)")
@utils.arg('--type',
           metavar='<type>',
           required=True,
           help="Specifies the record type to add (A, AAAA, CNAME, MX, NS, PTR, SRV, TXT).")
@utils.arg('--data',
           metavar='<data>',
           required=True,
           help="The data field for PTR, A, and AAAA records must be a valid IPv4 or IPv6 IP address")
@utils.arg('--ttl',
           default=3600,
           metavar='<ttl>',
           help="If specified, must be greater than 300. The default value, if not specified, is 3600.")
@utils.arg('--priority',
           metavar='<priority>',
           help="Required for MX and SRV records, but forbidden for other record types. If specified, must be an integer from 0 to 65535.")
@utils.arg('--comment',
           default=None,
           metavar='<comment>',
           help="If included, its length must be less than or equal to 160 characters.")
def do_record_create(cs, args):
    """Add new record to the specified domain."""
    domainId = utils.find_resource(cs.domains, args.domain)
    record = cs.records.create(args, domainId)
    print json.dumps(record._info, sort_keys=True, indent=4)
