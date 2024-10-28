import pika
import time
import os
import sys

rabbitmq_host = os.getenv('RABBITMQ_HOST')
queue_name = os.getenv('RABBITMQ_QUEUE')
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_port = os.getenv('RABBITMQ_PORT')

def check_env_vars():
    required_vars = {
        'RABBITMQ_HOST': os.getenv('RABBITMQ_HOST'),
        'RABBITMQ_QUEUE': os.getenv('RABBITMQ_QUEUE'),
        'RABBITMQ_USER': os.getenv('RABBITMQ_USER'),
        'RABBITMQ_PASS': os.getenv('RABBITMQ_PASS'),
        'RABBITMQ_PORT': os.getenv('RABBITMQ_PORT'),
    }
    
    missing_vars = [var for var, value in required_vars.items() if value is None]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)  # Exit the program with an error code
    else:
        print("All required environment variables are set.")

# Run the check
check_env_vars()

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
    # breakpoint()
    # Declare a queue (idempotent; will only be created if it doesn't exist)
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish a message to the queue
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                        #   properties=pika.BasicProperties(
                        #       delivery_mode=2,  # Make message persistent
                        #   )
    )
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
    # breakpoint()

    # Declare a queue (idempotent; will only be created if it doesn't exist)
    channel.queue_declare(queue=queue_name, durable=True)

    # Set up the consumer to only get one message at a time
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


