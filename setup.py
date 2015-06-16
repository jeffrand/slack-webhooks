#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements
import uuid
import os

path = os.path.realpath(__file__)
req_path = os.path.join(os.path.dirname(path), 'requirements.txt')

install_reqs = parse_requirements(req_path, session=uuid.uuid1())

setup(name='slack_webhooks',
      version='1.0.2',
      description='Webhook helper for Slack',
      author='Jeff Rand',
      author_email='jeffreyrand@gmail.com',
      install_requires=[str(ir.req) for ir in install_reqs],
      url='https://github.com/jeffrand/slack-webhooks',
      packages=['slack_webhooks'],
)
