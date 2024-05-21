import pika
import logging
from config import Config

def get_rabbitmq_connection():
    try:
        params = pika.URLParameters(Config.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        return connection
    except pika.exceptions.AMQPConnectionError as e:
        logging.error("Failed to connect to RabbitMQ: %s", e)
        raise

def send_log_message(message):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue='log_queue', durable=True)
        logging.debug("Sending message to RabbitMQ: %s", message)
        channel.basic_publish(
            exchange='',
            routing_key='log_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )
        logging.debug("Message sent successfully")
        connection.close()
    except Exception as e:
        logging.error("Failed to send log message: %s", e