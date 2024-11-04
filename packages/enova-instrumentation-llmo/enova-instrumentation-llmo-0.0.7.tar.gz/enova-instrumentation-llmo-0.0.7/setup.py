# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['llmo',
 'llmo.instrumentation',
 'llmo.instrumentation.fastapi',
 'llmo.instrumentation.vllm',
 'llmo.metrics_adapter']

package_data = \
{'': ['*']}

install_requires = \
['fastapi',
 'opentelemetry-api',
 'opentelemetry-distro',
 'opentelemetry-exporter-otlp',
 'opentelemetry-instrumentation-fastapi',
 'opentelemetry-sdk',
 'vllm==v0.6.0']

setup_kwargs = {
    'name': 'enova-instrumentation-llmo',
    'version': '0.0.7',
    'description': 'llmo instrumentation for OpenTelemetry',
    'long_description': None,
    'author': 'wenxinxie',
    'author_email': 'wenxin@emergingai-tech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
