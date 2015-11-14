===============================
pynvramutil
===============================

.. .. image:: https://img.shields.io/travis/westurner/pynvramutil.svg
..        :target: https://travis-ci.org/westurner/pynvramutil

.. .. image:: https://img.shields.io/pypi/v/pynvramutil.svg
..        :target: https://pypi.python.org/pypi/pynvramutil


pynvramutil is a utility for nvram change management

| Src: https://github.com/westurner/pynvramutil
| Docs: https://github.com/westurner/pynvramutil#pynvramutil

.. | Docs: https://pynvramutil.readthedocs.org

* Free software: ISC license


Features
--------


* [X] Parse the (unsorted multiline) output from ``nvram show``
  and sort by key name
* [ ] Compare two ``nvram show`` outputs (e.g. for incremental
  changesets)
* [ ] Generate a series of ``nvram set`` commands from a changeset


``nvram show``
----------------

Config data stored in nonvolatile RAM (nvram) with many
DD-WRT and OpenWRT compatible devices
can be listed with the ``nvram`` utility included
with a given image.

For example, the output from ``nvram show``:

.. code:: bash

   # nvram show
   ssh user@host -- nvram show | tee nvramshow.output.txt

.. code::

   key1=value1
   key2=value
   two
   2
   key3=value3


Use Cases
-----------

---------------------------------
Firmware Upgrade Config Rebuild
---------------------------------
Problem: When upgrading [many different] embedded device firmwares,
it's often recommended to factory reset the configuration
(before and/or after each upgrade/downgrade);
thus dropping any manual configuration.

Solution:

* [ ] Take ``nvram show`` snapshots before and between each
  (Web UI) change
* [ ] Build sequenced diff scripts from the changesets
  between each snapshot
* [ ] Manually prune/trim
* [ ] Apply one or more changeset diffs in sequence,
  pausing to run a test script

  * [ ] Test script (online, pingable, ssh-able, web-able)


Credits
---------

Tools used in rendering this package:

-------------
Cookiecutter
-------------
*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


-------
DD-WRT
-------
| Wikipedia: https://en.wikipedia.org/wiki/DD-WRT
| Homepage: https://www.dd-wrt.com/site/
| Download: ftp://ftp.dd-wrt.com/betas/
| Src: http://svn.dd-wrt.com/browser
| Project: http://svn.dd-wrt.com/
| Docs: https://www.dd-wrt.com/wiki
| Docs: http://svn.dd-wrt.com/timeline

* DD-WRT ``nvram show`
