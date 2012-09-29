rackspace-dns-cli
=================

Command line tool for Rackspace Cloud DNS - not endorsed by Rackspace

The guts of the code has been copied from the python-novaclient project.

You should read the Rackspace DNS documetation at
http://docs.rackspace.com/

Installing this package gets you a shell command, ``rackdns``, that you
can use to interact with the Rackspace DNS API.

You'll need to provide your Rackspace username and api key. You can do this
with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=user
    export OS_PASSWORD=yadayada
    export OS_TENANT_NAME=123456

You will also need to define the authentication url with ``--nova-url``.  
And explictly state you are using the Rackspace Auth system.  
Or set them as an environment variables as well::

    export OS_AUTH_URL=http://auth.api.rackspacecloud.com/v2.0/
    export NOVA_RAX_AUTH=1

You'll find the complete documentation on the shell by running ``rackdns help``::

	usage: rackdns [--version] [--debug] [--os-username <auth-user-name>]
	               [--os-password <auth-password>]
	               [--os-tenant-name <auth-tenant-name>]
	               [--os-auth-url <auth-url>]
	               [--no-cache] [--insecure]
 	              <subcommand> ...
	
	Command-line interface to the Rackspace DNS API.
	
	Positional arguments:
  		<subcommand>
    		domain-create       Create a new domain.
    		domain-delete       Delete a domain by name.
    		domain-export       Export details of the specified domain.
    		domain-list         Print a list of available domains.
    		domain-modify       Modify a domain.
    		domain-show         Show details about the given domain
    		limits              List all applicable limits.
    		record-create       Add new record to the specified domain.
    		record-delete       Delete a record of the specified domain.
    		record-list         Print a list of records for the given domain.
    		record-modify       Modify a record of the specified domain.
    		subdomain-list      Print a list of available sub-domains for the given
                        		domain.
    		help                Display help about this program or one of its
	                        	subcommands.
	
	Optional arguments:
	  --version             show program's version number and exit
	  --debug               Print debugging output
	  --os-username <auth-user-name>
	                        Defaults to env[OS_USERNAME].
	  --os-password <auth-password>
	                        Defaults to env[OS_PASSWORD].
	  --os-tenant-name <auth-tenant-name>
	                        Defaults to env[OS_TENANT_NAME].
	  --os-auth-url <auth-url>
	                        Defaults to env[OS_AUTH_URL].
	  --no-cache            Don't use the auth token cache.
	  --insecure            Explicitly allow dnsclient to perform "insecure" SSL
	                        (https) requests. The server's certificate will not be
	                        verified against any certificate authorities. This
	                        option should be used with caution.

	See "rackdns help COMMAND" for help on a specific command.
