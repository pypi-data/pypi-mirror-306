from django.apps import AppConfig
from django.core.signals import request_finished
from django.dispatch import receiver
from bomiot.server.core.signal import bomiot_signals

class CoreConfig(AppConfig):
    name = 'bomiot.server.core'


def test_sm():
    print('这是一个测试')

@receiver(request_finished)
def do_init_data(sender, **kwargs):
    configuration = {
        'trigger': 'interval',
        'minute': 3
    }
    bomiot_signals.send(sender=test_sm, msg=configuration)