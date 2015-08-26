from setuptools import setup, find_packages

setup(
    name="metahosting-common",
    version="1.0.0",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['env', 'tests']),
    install_requires=[
        'pymongo==3.0.3',
        'pika==0.9.14',
        'retrying==1.3.3',
        'python_logstash>=0.4.5'
    ]
)
