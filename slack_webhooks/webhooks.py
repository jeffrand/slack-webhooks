from __future__ import absolute_import
import requests
import json
from functools import wraps

class SlackDumpableMixin(object):
    ''' Mixin for dumping properties '''
    def dump_props(self):
        payload = {}
        for prop in self.slack_props:
            prop_val = getattr(self, prop, None)
            if prop_val:
                if isinstance(prop_val, SlackDumpableMixin):
                    payload[prop] = prop_val.dump_props()
                elif isinstance(prop_val, (list, tuple)):
                    # this might be overkill
                    payload[prop] = []
                    for sub_prop in prop_val:
                        if isinstance(sub_prop, SlackDumpableMixin):
                            sub_prop = sub_prop.dump_props()
                        payload[prop].append(sub_prop)
                payload[prop] = prop_val
        return payload

class SlackWebhook(SlackDumpableMixin):
    ''' Wrapper for Slack Incoming Webhooks '''
    def __init__(self, webhook_url, username=None, icon_url=None,
                 icon_emoji=None, channel=None):
        if icon_url and icon_emoji:
            raise ValueError('You cannot can only specify one of: icon_url, icon_emoji')

        self.slack_props = ('username', 'channel', 'icon_url', 'icon_emoji')
        self.webhook_url = webhook_url
        self.username = username
        self.channel = channel
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji

        super(self.__class__, self).__init__()

    def __dump_payload(self, extra):
        payload = self.dump_props()
        payload.update(extra)
        return json.dumps(payload)

    def decorate(self, success_text, failure_text,
                 success_attachment=None, failure_attachment=None):
        ''' Decorator with success/failure text and attachments '''
        def inner_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    ret = func(*args, **kwargs)
                    self.send(success_text, attachment=success_attachment)
                    return ret
                except Exception:
                    self.send(failure_text, attachment=failure_attachment)
                    raise
            return wrapper
        return inner_decorator

    def send(self, text, attachment=None):
        extra = {'text': text}
        if attachment:
            if isinstance(attachment, SlackAttachment):
                attachment = [attachment.dump_props()]
            else:
                attachment = [a.dump_props() for a in attachment
                          if isinstance(a, SlackAttachment)]
            extra['attachments'] = attachment
        return requests.post(self.webhook_url, data=self.__dump_payload(extra))

class SlackAttachment(SlackDumpableMixin):
    ''' Wrapper for Slack Attachments '''
    def __init__(self, fallback, color=None, pretext=None, author_name=None,
                 author_link=None, author_icon=None, title=None, title_link=None,
                 text=None, fields=None, image_url=None, thumb_url=None):

            self.fallback = fallback
            self.color = color
            self.pretext = pretext
            self.author_name = author_name
            self.author_link = author_link
            self.author_icon = author_icon
            self.title = title
            self.title_link = title_link
            self.text = text
            self.fields = fields
            self.image_url = image_url
            self.thumb_url = thumb_url

            self.slack_props = ('fallback', 'color', 'pretext', 'author_name',
                                'author_link', 'author_icon', 'title',
                                'title_link', 'text', 'fields', 'image_url',
                                'thumb_url')

            super(self.__class__, self).__init__()
