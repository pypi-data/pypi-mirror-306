SafelySaveOnline
================

SafelySaveOnline is a python libary making it easy to save encrypted
dictionaries and store them on a server.
It is meant to use in small projects.

Installing
----------

You can install SafelySaveOnline with:

::

   pip install safelysaveonline

Usage
-----

Import SafelySaveOnline with:

::

   import safelysave

Create a SSO file with:

::

   key: bytes = safelysave.create_sso_file(file_path, 'webdav', webdav_address)

Remember the returned key.

Create a instance with:

::

    sso = safelysave.sso(file_path, key)

Now add an dictionary with:

::

   sso.add_data(ictionary)

Sync it to your server with:

::

   sso.sync()

You can find out more at
https://codeberg.org/VisualXYW/safelysaveonline/wiki (WIP).
Note that there are currently problems with syncing to git repositories. Use at your own risk.
