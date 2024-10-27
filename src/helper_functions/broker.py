import pika
import time
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST')
queue_name = os.getenv('RABBITMQ_QUEUE_NAME')
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_port = os.getenv('RABBITMQ_PORT')


# Publisher function to send a message
def publish_message(message):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        virtual_host="/",
        credentials=credentials
    ))
    channel = connection.channel()

    # Declare a queue (idempotent; will only be created if it doesn't exist)
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish a message to the queue
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # Make message persistent
                          ))
    print(f" [x] Sent '{message}'")
    connection.close()

# Consumer function to receive messages one at a time
def consume_message(callback):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        virtual_host="/",
        credentials=credentials
    ))
    channel = connection.channel()

    # Declare a queue (idempotent; will only be created if it doesn't exist)
    channel.queue_declare(queue=queue_name, durable=True)

    # Set up the consumer to only get one message at a time
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


