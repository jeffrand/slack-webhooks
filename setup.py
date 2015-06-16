#!/usr/bin/env python

from setuptools import setup

setup(name='slack_webhooks',
      version='1.0.3',
      description='Webhook helper for Slack',
      author='Jeff Rand',
      author_email='jeffreyrand@gmail.com',
      install_requires=[
        'requests==2.7.0',
      ],
      url='https://github.com/jeffrand/slack-webhooks',
      packages=['slack_webhooks'],
)
