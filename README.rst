==========
RQ Monitor
==========


Description
-----------

RQMonitor is a simple Tornado-based application to monitor RQ queues and workers.


Installation
------------

Installing from pip
~~~~~~~~~~~~~~~~~~~

Simply invoke::

  $ pip install rq-monitor


Installing from sources
~~~~~~~~~~~~~~~~~~~~~~~

You can clone the ``rq-monitor`` git repository and install it manually::

  $ git clone git://github.com/andrzej-jankowski/rq-monitor.git .
  $ pip install -e .


Run
---

To run ``rq-monitor`` use the command::

  $ rq-monitor

Then run your web browser and put ``localhost:7272`` in address field.

To get more help invoke::

  $ rq-monitor -h


Remarks
-------

This software uses Highcharts JS. Highcharts is not free for commercial use.

Highcharts site: `www.highcharts.com <http://www.highcharts.com/>`_
