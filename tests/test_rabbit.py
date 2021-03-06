import unittest

from metahosting.common import config_manager
from metahosting.common.messaging import get_message_subject
from metahosting.common.messaging.rabbit import BlockingPikaManager


def callback(msg):
    print 'Incoming message %s' % msg


class RabbitTest(unittest.TestCase):
    def setUp(self):
        config = config_manager.get_configuration(
            section_name='messaging',
            config_file='tests/files/config.ini',
            variables_file='tests/files/envvars.ini')
        self.queue_name = 'testing_queue'
        self.manager = BlockingPikaManager(config=config,
                                           queue=self.queue_name)

    def tearDown(self):
        pass

    def test_publish(self):
        self.manager.publish(routing_key=self.queue_name,
                             subject='nothing',
                             message={'foo': 'bar'})

    def test_subscribe(self):
        self.manager.subscribe(routing_key=self.queue_name,
                               callback=callback)
        self.manager.publish(routing_key=self.queue_name,
                             subject='nothing',
                             message={'foo': 'bar'})

    def test_unsubsribe(self):
        with self.assertRaises(NotImplementedError):
            self.manager.unsubscribe(routing_key=self.queue_name,
                                     listener=lambda x: None)

    def test_send_message(self):
        self.manager.publish(routing_key=self.queue_name,
                             subject='nothing',
                             message={'foo': 'bar'})

    def test_alt_subscribe(self):
        self.manager.subscribe(routing_key=self.queue_name,
                               callback=callback)
        self.manager.publish(routing_key=self.queue_name,
                             subject='nothing',
                             message={'foo': 'bar'})

    def test_get_subject(self):
        msg = {'content': 'content', 'foo': 'bar'}
        self.assertIsNone(get_message_subject(msg))
        subject = 'Grass is green'
        msg['subject'] = subject
        self.assertTrue('subject' in msg)
        res = get_message_subject(msg)
        self.assertEquals(res, subject)
        self.assertFalse('subject' in msg)
