#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Container Solutions",
    author_email='cre@container-solutions.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="prom-metrics-check is command line tools which help checking "
                "metric between dashboards of grafana and prometheus metrics.",
    entry_points={
        'console_scripts': [
            'prom-metrics-check=prom_metrics_check.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='prom-metrics-check',
    name='prom-metrics-check',
    packages=find_packages(include=['prom_metrics_check', 'prom_metrics_check.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ContainerSolutions/prom-metrics-check',
    version='0.1.0',
    zip_safe=False,
)
