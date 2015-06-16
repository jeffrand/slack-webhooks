from __future__ import absolute_import
import requests
import json

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
                    payload[prop] = []
                    for sub_prop in prop_val:
                        if isinstance(sub_prop, SlackDumpableMixin):
                            sub_prop = sub_prop.dump_props()
                        payload[prop].append(sub_prop)
                payload[prop] = prop_val
        return payload

class SlackWebhook(SlackDumpableMixin):
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

    def dispatch(self, text, attach=None):
        extra = {'text': text}
        if attach:
            if isinstance(attach, SlackAttachment):
                attach = [attach.dump_props()]
            else:
                attach = [a.dump_props() for a in attach
                          if isinstance(a, SlackAttachment)]
            extra['attachments'] = attach
        return requests.post(self.webhook_url, data=self.__dump_payload(extra))

class SlackAttachment(SlackDumpableMixin):
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
