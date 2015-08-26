import pika
import logging
import json
import threading

from retrying import retry


class BlockingPikaManager(object):
    def __init__(self, config,  queue=None):
        logging.debug('Initializing Messaging')
        credentials = pika.PlainCredentials(config['user'], config['password'])
        parameters = pika.ConnectionParameters(host=config['host'],
                                               port=int(config['port']),
                                               virtual_host='',
                                               credentials=credentials)
        self.connection = self._get_connection(parameters=parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=True)
        self.thread = threading.Thread(target=self.channel.start_consuming)
        self.thread.setDaemon(True)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def _get_connection(self, parameters):
        logging.info('Establishing connection')
        return pika.BlockingConnection(parameters)

    def publish(self, routing_key, subject, message):
        message['subject'] = subject
        logging.debug('Dispatching %s, %s: %s', routing_key, subject, message)
        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   body=json.dumps(message),
                                   properties=pika.BasicProperties(
                                       content_type='application/json'))

    def subscribe(self, routing_key, callback):
        def callback_wrapper(channel, method, properties, body):
            if properties.content_type != 'application/json':
                logging.error('Invalid content_type: %s',
                              properties.content_type)
                channel.basic_reject(delivery_tag=method.delivery_tag,
                                     requeue=False)
                logging.debug('Discarding message: %r', body)
                return

            callback(json.loads(body))
            channel.basic_ack(delivery_tag=method.delivery_tag)

        logging.debug('Subscribe request for: %s', routing_key)
        self.channel.basic_consume(callback_wrapper, queue=routing_key)
        if not self.thread.is_alive():
            self.thread.start()

    def unsubscribe(self, routing_key, listener):
        # self.channel.basic_cancel(consumer_tag=listener.__name__)
        raise NotImplementedError

    def disconnect(self):
        if self.connection.is_open:
            self.connection.close()
