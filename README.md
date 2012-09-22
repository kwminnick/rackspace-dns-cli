rackspace-dns-cli
=================

Command line tool for Rackspace Cloud DNS - not endorsed by Rackspace

You should read the Rackspace DNS documetation at
___ http://docs.rackspace.com/

Installing this package gets you a shell command, ``rackdns``, that you
can use to interact with the Rackspace DNS API.

You'll need to provide your Rackspace username and api key. You can do this
with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export NOVA_USERNAME=user
    export NOVA_PASSWORD=yadayada
    export OS_TENANT_NAME=123456

You will also need to define the authentication url with ``--nova-url``
and the version of the API with ``--version``.  Or set them as an environment
variables as well::

    export NOVA_URL=http://auth.api.rackspacecloud.com/v2.0/
    export NOVA_VERSION=1.1


