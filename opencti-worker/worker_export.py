# coding: utf-8

import os
import yaml
import pika
import json
import base64
import time
from logger import Logger
from pycti import OpenCTI


class WorkerExport:
    def __init__(self, verbose=True):
        # Initialize logger
        self.logger = Logger(os.path.dirname(os.path.abspath(__file__)) + '/logs/worker.log')

        # Load configuration
        self.config = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml'))

        # Initialize OpenCTI client
        self.opencti = OpenCTI(
            self.config['opencti']['api_url'],
            self.config['opencti']['api_key'],
            os.path.dirname(os.path.abspath(__file__)) + '/logs/worker.log',
            self.config['opencti']['verbose']
        )

    def export_action(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            self.logger.log('Receiving new action of type: { ' + data['type'] + ' }')
            bundle = None
            if data['type'] == 'export.stix2.simple':
                bundle = self.opencti.stix2_export_entity(data['entity_type'], data['entity_id'], 'simple')
            if data["type"] == 'export.stix2.full':
                bundle = self.opencti.stix2_export_entity(data['entity_type'], data['entity_id'], 'full')

            if bundle is not None:
                bundle = base64.b64encode(bytes(json.dumps(bundle, indent=4), 'utf-8')).decode('utf-8')
                self.opencti.push_stix_domain_entity_export(data['entity_id'], data['export_id'], bundle)
        except Exception as e:
            self.logger.log('An unexpected error occurred: { ' + str(e) + ' }')
            return False

    def consume(self):
        # Initialize the RabbitMQ connection
        credentials = pika.PlainCredentials(self.config['rabbitmq']['username'], self.config['rabbitmq']['password'])
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config['rabbitmq']['hostname'],
            port=self.config['rabbitmq']['port'],
            virtual_host='/',
            credentials=credentials
        ))
        channel = connection.channel()
        channel.exchange_declare(exchange='opencti', exchange_type='topic', durable=True)
        channel.queue_declare('opencti-export', durable=True)
        channel.queue_bind(exchange='opencti', queue='opencti-export', routing_key='export.*.*')
        channel.basic_consume(queue='opencti-export', on_message_callback=self.export_action, auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    worker_export = WorkerExport()
    while True:
        try:
            worker_export.consume()
        except Exception as e:
            print(e)
            time.sleep(5)
