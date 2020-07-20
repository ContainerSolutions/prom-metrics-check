"""Console script for prom_metrics_check."""
import os
import sys
import argparse
import logging

from .prom_metrics_check import load_dashboard, get_all_metrics, \
    check_exist_metrics


logging.basicConfig(level='ERROR')
logger = logging.getLogger('prom-metric-check')


GRAFANA_DEFAULT_URL = 'http://localhost:3000'
PROMETHEUS_DEFAULT_URL = 'http://localhost:9090'

GRAFANA_URL = os.environ.get(
    'GRAFANA_URL', GRAFANA_DEFAULT_URL)
GRAFANA_KEY = os.environ.get(
    'GRAFANA_KEY')
PROMETHEUS_URLS = os.environ.get(
    'PROMETHEUS_URLS', PROMETHEUS_DEFAULT_URL).split(',')


def main():
    """Console script for prom_metrics_check."""
    parser = argparse.ArgumentParser(
        description='Command line tool for check metrics between '
                    'grafana and prometheus instance.')
    parser.add_argument(
        '--grafana-url',
        metavar='grafana_url',
        help=f'Set grafana url. Default value is {GRAFANA_DEFAULT_URL}',
        nargs='?',
        default=GRAFANA_URL)
    parser.add_argument(
        '--grafana-key',
        metavar='grafana_key',
        help='Set grafana key to have API access.',
        nargs='?',
        default=GRAFANA_KEY)
    parser.add_argument(
        '--prometheus-url',
        metavar='prometheus_url',
        help=f'Set prometheus url. Default value is {PROMETHEUS_DEFAULT_URL}',
        nargs='?',
        default=PROMETHEUS_URLS)
    args = parser.parse_args()
    for url in args.prometheus_url:
        dashboards = load_dashboard(url=args.grafana_url, key=args.grafana_key)
        except_metrics = get_all_metrics(dashboards=dashboards)
        missing_metrics = check_exist_metrics(except_metrics, url)
        if missing_metrics:
            logger.critical(
                f" Metrics which don't exist: {', '.join(missing_metrics)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())    # pragma: no cover
