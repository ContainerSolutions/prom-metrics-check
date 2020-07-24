# prom-metrics-check

`prom-metrics-check` is a command line tools which helps checking metrics between dashboards of grafana and prometheus metrics.

If you download external dashboards to your grafana instance (eg. https://github.com/kubernetes-monitoring/kubernetes-mixin)
you are not 100% sure that all queries used in dashboard work with your prometheus instance. This tool looking for in any
dashboard all queries, then it extracts only metrics and check that all used metrics exist in your prometheus instance.

* Free software: MIT license
* Repository: https://github.com/ContainerSolutions/prom-metrics-check/
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

To use this tool locally, you will need to create port-forwards for your grafana and prometheus services.


    $ kubectl port-forward svc/grafana 3000:80
    $ kubectl port-forward svc/prometheus 9090:9090

Also, if you use an API key for Grafana you should set it in you environment.


    $ export GRAFANA_KEY=...

Now you should be able to run the following script:


    $ prom-metrics-check

To see more arguments, run the script with the `--help` flag.


    $ prom-metrics-check --help

## Work with Docker

### Build Docker Image

If you want to build the Docker image, run: `make docker-build`

### Run Docker

To run this container locally, use the `--net=host` flag.

The Makefile can also help running Docker images.

If you download this repository on Linux, you should be able to run the container with: 

    ARGS="--grafana-url=http://localhost:3000 --prometheus-urls=http://localhost:9090 --grafana-key=xyz=" make docker-run

on MacOS the command is slightly differnt:

    ARGS="--grafana-url=http://host.docker.internal:3000 --prometheus-urls=http://host.docker.internal:9090 --grafana-key=xyz=" make docker-run

If you need to run Docker from scratch you should use a different command.

#### Linux

    $ docker run --net=host --rm -e GRAFANA_URL=http://localhost:3000 -e PROMETHEUS_URLS=http://localhost:9090 -e GRAFANA_KEY=xyz containersol/prom-metrics-check:latest

#### MacOS

    $ docker run --net=host --rm -e GRAFANA_URL=http://host.docker.internal:3000 -e PROMETHEUS_URLS=http://host.docker.internal:9090 -e GRAFANA_KEY=xyz containersol/prom-metrics-check:latest
