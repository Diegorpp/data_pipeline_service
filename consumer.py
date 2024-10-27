from src.helper_functions.broker import consume_message

# Define a callback function to process each message
def processing(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")
    
    # TODO: Insert the pipeline processing here.
    
    # Acknowledge the message was processed
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


if __name__ == '__main__':
    consume_message(processing)