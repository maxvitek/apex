APEX
====

This is a small and simple python package for interacting
with the `Neptune Systems Apex Aquacontroller`_.  At the
moment, it allows only for simple interactions, like
fetching the status of the Apex system, probes, and outlets,
and setting them.

Usage
-----

.. code-block:: pycon

    >>> from apex import Apex
    >>> a = Apex('10.0.1.35')
    >>> a.get_api()
    >>> a.set_outlet('Heater_4_5', 'auto')

Contributions
-------------

#. Let's get the xml data off the server and return a pandas dataframe.
#. What else?


.. _Neptune Systems Apex Aquacontroller: http://www.neptunesystems.com/products/apex-controllers/apex-controller-system/
