import jpush
from jpush import common
from . import mysql_use

app_key = u'713db5486c35b95a967e3b3a'
master_secret = u'7dbfd6784418f04271c2e12a'

dev_key = u'8d12ba4d3a1e51459203a85a'
dev_secret = u'd675ae0745af28ed6d95f9f3'

_jpush = jpush.JPush(app_key, master_secret)
_jpush.set_logging("DEBUG")


def alias(alias_list, alert=''):
    push = _jpush.create_push()
    alias1 = {"alias": alias_list}
    push.audience = alias1

    push.notification = jpush.notification(alert=alert)
    push.platform = jpush.all_
    push.send()


def push_all():
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert="!hello python jpush api")
    push.platform = jpush.all_
    try:
        response = push.send()
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        print("JPushFailure")
    except:
        print("Exception")


def audience():
    push = _jpush.create_push()

    push.audience = jpush.audience(
        jpush.tag("tag1", "tag2"),
        jpush.alias("alias1", "alias2")
    )

    push.notification = jpush.notification(alert="Hello world with audience!")
    push.platform = jpush.all_
    print(push.payload)
    push.send()


def notification():
    push = _jpush.create_push()

    push.audience = jpush.all_
    push.platform = jpush.all_

    ios = jpush.ios(alert="Hello, IOS JPush!", sound="a.caf", extras={'k1': 'v1'})
    android = jpush.android(alert="Hello, Android msg", priority=1, style=1, alert_type=1, big_text='jjjjjjjjjj',
                            extras={'k1': 'v1'})

    push.notification = jpush.notification(alert="Hello, JPush!", android=android, ios=ios)

    # pprint (push.payload)
    result = push.send()


def options():
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert="Hello, world!")
    push.platform = jpush.all_
    push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": True}
    push.send()


def platfrom_msg():
    push = _jpush.create_push()
    push.audience = jpush.all_
    ios_msg = jpush.ios(alert="Hello, IOS JPush!", badge="+1", sound="a.caf", extras={'k1': 'v1'})
    android_msg = jpush.android(alert="Hello, android msg")
    push.notification = jpush.notification(alert="Hello, JPush!", android=android_msg, ios=ios_msg)
    push.message = jpush.message("content", extras={'k2': 'v2', 'k3': 'v3'})
    push.platform = jpush.all_
    push.send()


def silent():
    push = _jpush.create_push()
    push.audience = jpush.all_
    ios_msg = jpush.ios(alert="Hello, IOS JPush!", badge="+1", extras={'k1': 'v1'}, sound_disable=True)
    android_msg = jpush.android(alert="Hello, android msg")
    push.notification = jpush.notification(alert="Hello, JPush!", android=android_msg, ios=ios_msg)
    push.platform = jpush.all_
    push.send()


def sms():
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert="a sms message from python jpush api")
    push.platform = jpush.all_
    push.smsmessage = jpush.smsmessage("a sms message from python jpush api", 0)
    print(push.payload)
    push.send()


def validate():
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert="Hello, world!")
    push.platform = jpush.all_
    push.send_validate()
