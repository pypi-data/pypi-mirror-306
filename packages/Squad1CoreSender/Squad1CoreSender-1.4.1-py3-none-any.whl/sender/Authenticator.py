import uuid

import pika


class Authenticator:
    """

    """
    def __init__(self, connection, channel, module):
        """

        :param connection:
        :param channel:
        """
        self.corr_id = None
        self.response = None
        self.connection = connection
        self.channel = channel
        result = channel.queue_declare(queue=f'{module}.rpc', exclusive=True)
        self.callback_queue = result.method.queue
        channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True
        )

    def _on_response(self, ch, method, props, body):
        """

        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id:
            self.response = body.decode('utf-8')
        else:
            raise Exception('Authenticator bad response')

    def authenticate(self, message, timeout_ms=1000):
        """

        :param message:
        :param timeout_ms:
        :return:
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='gestion_interna.rpc',
            routing_key='gestion_interna.rpc',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=message
        )
        start_time = time.time()
        timeout = timeout_ms / 1000
        while self.response is None:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                raise Exception('Authenticator did not respond in time')
            self.connection.process_data_events()
        return self.response