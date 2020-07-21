# prom-metrics-check

`prom-metrics-check` is command line tools which help checking metric between dashboards of grafana and prometheus metrics.

* Free software: MIT license
* Rspository: https://github.com/ContainerSolutions/prom-metrics-check/
* DockerHub: containersol/prom-metrics-check:latest

## Features

* Connect via API to Grafana and get all metrics which are use in any dashboards
* Connect via API to Prometheus and check exist metrics


## Installation

### Stable release

To install prom-metrics-check, run this command directly from repository:


    $ pip install git+https://github.com/ContainerSolutions/prom-metrics-check.git


This is the preferred method to install prom-metrics-check, as it will always install the most recent stable release.

If you don't have [pip] installed, this [Python installation guide] can guide
you through the process.

[pip]: https://pip.pypa.io
[Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/


### From sources

The sources for prom-metrics-check can be downloaded from the [Github repo].

You can either clone the public repository:


    $ git clone git://github.com/ContainerSolutions/prom-metrics-check

Or download the [tarball]:


    $ curl -OJL https://github.com/ContainerSolutions/prom-metrics-check/tarball/master

Once you have a copy of the source, you can install it with:


    $ python setup.py install

[Github repo]: https://github.com/ContainerSolutions/prom-metrics-check
[tarball]: https://github.com/ContainerSolutions/prom-metrics-check/tarball/master


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

## Work with DOCKER

### Build docker

If you need build docker from scrath use command: `make docker-build`

### Run docker

To run this container you should use extra flag when you run docker image localy: `--net=host`.
On make file we prepared extra command ro run your docker:

If you download this repository and try run this container follow this command on linux:

    ARGS="--grafana-url=http://localhost:3000 --prometheus-urls=http://localhost:9090 --grafana-key=xyz=" make docker-run

on MacOO you should update host:

    ARGS="--grafana-url=http://host.docker.internal:3000 --prometheus-urls=http://host.docker.internal:9090 --grafana-key=xyz=" make docker-run

If you need run this docker from scratch you should different command.

#### Linux

    $ docker run --net=host --rm -e GRAFANA_URL=http://localhost:3000 -e PROMETHEUS_URLS=http://localhost:9090 -e GRAFANA_KEY=xyz containersol/prom-metrics-check:latest

#### MacOS

    $ docker run --net=host --rm -e GRAFANA_URL=http://host.docker.internal:3000 -e PROMETHEUS_URLS=http://host.docker.internal:9090 -e GRAFANA_KEY=xyz containersol/prom-metrics-check:latest
