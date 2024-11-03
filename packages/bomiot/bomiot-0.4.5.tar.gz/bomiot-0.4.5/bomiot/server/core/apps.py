from django.apps import AppConfig
from bomiot.server.core.signal import bomiot_signals

class CoreConfig(AppConfig):
    name = 'bomiot.server.core'

    def ready(self):
        configuration = {
            'trigger': 'interval',
            'minute': 0
        }
        bomiot_signals.send(sender=test_sm, msg=configuration)

def test_sm():
    print('这是一个测试')