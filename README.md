# slack-webhooks
Easily integrate [Slack webhooks](https://api.slack.com/incoming-webhooks) with your project.

## Examples

### Send a message

```
from slack_webhooks import SlackWebhook, SlackAttachment

webhook = SlackWebhook('https://hooks.slack.com/services/foo/bar/baz'
                       icon_emoji=':panda:')
webhook.send('Cool beans!')
```

### Supports [Attachments](https://api.slack.com/docs/attachments)

```
attachment = SlackAttachment('Party Time!', text='Party Time',
                             title='What time is it?', color='good')
webhook.send('Cool beans!', attachment=attachment)
```

### Decorate a fuction with success and failure messages/attachments

```
a2 = SlackAttachment('Oh no!', text='Nooooo',
                      title='Bad things?', color='danger')
@webhook.decorate('woo', boo', success_attachment=attachment,
                  failure_attachment=a2)
def do_stuff(foo):
    print foo
```
