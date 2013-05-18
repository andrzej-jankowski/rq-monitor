 # -*- encoding: utf-8 -*-

import sys
from setuptools import setup, find_packages


assert sys.version_info >= (2, 7), "Python 2.7+ required."


from rq_monitor import VERSION
version = ".".join(str(num) for num in VERSION)


setup(
    name='rq-monitor',
    version=version,
    license='Apache Software License v2.0',
    author='Andrzej Jankowski',
    url='http://github.com/andrzej-jankowski',
    author_email='andew.jankowski@gmail.com',
    description='RQ Monitor - simple RQ dashboard.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'rq==0.3.7',
        'tornado==3.0.1',
    ],
    entry_points={
        'console_scripts': [
            'rq-monitor = rq_monitor.app:main',
        ],
    },
)
