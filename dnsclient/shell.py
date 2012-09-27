# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack LLC.
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
Command-line interface to the Rackspace DNS API.
"""

import argparse
import httplib2
import sys
import logging

import dnsclient
from dnsclient import client
from dnsclient import exceptions as exc
from dnsclient import utils
from dnsclient.v1_0 import shell as shell_v1_0

DEFAULT_OS_COMPUTE_API_VERSION = "1.0"

logger = logging.getLogger(__name__)

class RackDNSClientArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(RackDNSClientArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        """
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, "error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                     " for more information.\n" %
                     {'errmsg': message.split(choose_from)[0],
                      'mainp': progparts[0],
                      'subp': progparts[2]})

class RackDNSShell(object):

    def get_base_parser(self):
        parser = RackDNSClientArgumentParser(
            prog='rackdns',
            description=__doc__.strip(),
            epilog='See "rackdns help COMMAND" '\
                'for help on a specific command.',
            add_help=False,
           formatter_class=RackDNSHelpFormatter,
           )
        
        # Global arguments
        parser.add_argument('-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS,
        )

        parser.add_argument('--version',
                            action='version',
                            version=dnsclient.__version__)

        parser.add_argument('--debug',
            default=False,
            action='store_true',
            help="Print debugging output")

        parser.add_argument('--os-username',
            metavar='<auth-user-name>',
            default=utils.env('OS_USERNAME', 'NOVA_USERNAME'),
            help='Defaults to env[OS_USERNAME].')
        parser.add_argument('--os_username',
            help=argparse.SUPPRESS)

        parser.add_argument('--os-password',
            metavar='<auth-password>',
            default=utils.env('OS_PASSWORD', 'NOVA_PASSWORD'),
            help='Defaults to env[OS_PASSWORD].')
        parser.add_argument('--os_password',
            help=argparse.SUPPRESS)

        parser.add_argument('--os-tenant-name',
            metavar='<auth-tenant-name>',
            default=utils.env('OS_TENANT_NAME', 'NOVA_PROJECT_ID'),
            help='Defaults to env[OS_TENANT_NAME].')
        parser.add_argument('--os_tenant_name',
            help=argparse.SUPPRESS)

        parser.add_argument('--os-auth-url',
            metavar='<auth-url>',
            default=utils.env('OS_AUTH_URL', 'NOVA_URL'),
            help='Defaults to env[OS_AUTH_URL].')
        parser.add_argument('--os_auth_url',
            help=argparse.SUPPRESS)
                
        parser.add_argument('--no-cache',
            default=utils.env('OS_NO_CACHE', default=False),
            action='store_true',
            help="Don't use the auth token cache.")
        parser.add_argument('--no_cache',
            help=argparse.SUPPRESS)

        parser.add_argument('--insecure',
            default=utils.env('NOVACLIENT_INSECURE', default=False),
            action='store_true',
            help="Explicitly allow dnsclient to perform \"insecure\" "
                 "SSL (https) requests. The server's certificate will "
                 "not be verified against any certificate authorities. "
                 "This option should be used with caution.")
        
        # alias for --os-password, left in for backwards compatibility
        parser.add_argument('--apikey', '--password', dest='apikey',
            default=utils.env('NOVA_API_KEY'),
            help=argparse.SUPPRESS)

        return parser

    def get_subcommand_parser(self):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')

        actions_module = shell_v1_0

        self._find_actions(subparsers, actions_module)
        self._find_actions(subparsers, self)

        return parser

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # I prefer to be hypen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command,
                help=action_help,
                description=desc,
                add_help=False,
                formatter_class=RackDNSHelpFormatter
            )
            subparser.add_argument('-h', '--help',
                action='help',
                help=argparse.SUPPRESS,
            )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def setup_debugging(self, debug):
        if not debug:
            return

        streamhandler = logging.StreamHandler()
        streamformat = "%(levelname)s (%(module)s:%(lineno)d) %(message)s"
        streamhandler.setFormatter(logging.Formatter(streamformat))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(streamhandler)
        
        httplib2.debuglevel = 1

    def main(self, argv):
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self.setup_debugging(options.debug)

        subcommand_parser = self.get_subcommand_parser()
        self.parser = subcommand_parser

        if options.help and len(args) == 0:
            subcommand_parser.print_help()
            return 0

        args = subcommand_parser.parse_args(argv)
    
        # Short-circuit and deal with help right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0
        
        (os_username, os_password, 
         os_tenant_name, os_auth_url, apikey,
         insecure, no_cache) = (
                        args.os_username, args.os_password,
                        args.os_tenant_name, args.os_auth_url, args.apikey, 
                        args.insecure, args.no_cache)
                    
        if not utils.isunauthenticated(args.func):
            if not os_username:
                raise exc.CommandError("You must provide a username "
                            "via either --os-username or env[OS_USERNAME]")
                
            if not os_password:
                if not apikey:
                    raise exc.CommandError("You must provide a password "
                            "via either --os-password or via "
                            "env[OS_PASSWORD]")
                else:
                    os_password = apikey

            if not os_tenant_name:
                raise exc.CommandError("You must provide a tenant name "
                            "via either --os-tenant-name or "
                            "env[OS_TENANT_NAME]")

            if not os_auth_url:
                    raise exc.CommandError("You must provide an auth url "
                            "via either --os-auth-url or env[OS_AUTH_URL] "
                            "or specify an auth_system which defines a "
                            "default url with --os-auth-system "
                            "or env[OS_AUTH_SYSTEM")
        
        self.cs = client.Client("1.0", os_username,
                os_password, os_tenant_name, os_auth_url, insecure,
                no_cache=no_cache, http_log_debug=options.debug)
        
        try:
            if not utils.isunauthenticated(args.func):
                self.cs.authenticate()
        except exc.Unauthorized:
            raise exc.CommandError("Invalid OpenStack Nova credentials.")
        except exc.AuthorizationFailure:
            raise exc.CommandError("Unable to authorize user")

        args.func(self.cs, args)

        
        return
    
    @utils.arg('command', metavar='<subcommand>', nargs='?',
                    help='Display help for <subcommand>')
    def do_help(self, args):
        """
        Display help about this program or one of its subcommands.
        """
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()

class RackDNSHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(RackDNSHelpFormatter, self).start_section(heading)

def main():
    try:
        RackDNSShell().main(sys.argv[1:])

    except Exception, e:
        logger.debug(e, exc_info=1)
        print >> sys.stderr, "ERROR: %s" % unicode(e)
        sys.exit(1)


if __name__ == "__main__":
    main()