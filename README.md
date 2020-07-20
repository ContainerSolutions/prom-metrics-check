# prom-metrics-check

`prom-metrics-check` is command line tools which help checking metric between dashboards of grafana and prometheus metrics.

* Free software: MIT license
* Documentation: https://prom-metrics-check.readthedocs.io.


## Features

* Connect via API to Grafana and get all metrics which are use in any dashboards
* Connect via API to Prometheus and check exist metrics


## Installation

### Stable release

To install prom-metrics-check, run this command directly from repository:


    $ pip install git+https://github.com/ContainerSolutions/prom-metrics-check.git


This is the preferred method to install prom-metrics-check, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


### From sources

The sources for prom-metrics-check can be downloaded from the `Github repo`_.

You can either clone the public repository:


    $ git clone git://github.com/ContainerSolutions/prom-metrics-check

Or download the `tarball`_:


    $ curl -OJL https://github.com/ContainerSolutions/prom-metrics-check/tarball/master

Once you have a copy of the source, you can install it with:


    $ python setup.py install

.. _Github repo: https://github.com/ContainerSolutions/prom-metrics-check
.. _tarball: https://github.com/ContainerSolutions/prom-metrics-check/tarball/master


## Usage

To use this tool locally you need create port-forward to your grafana and prometheus services.


    $ kubectl port-forward svc/grafana 3000:80
    $ kubectl port-forward svc/prometheus 9090:9090

Also if you use API KEY for grafana you should set it in you environment.


    $ export GRAFANA_KEY=...

Now you are ready, try run this script in your system python interpreter.


    $ prom-metrics-check

To see more argument run script with help flag.


    $ prom-metrics-check --help
