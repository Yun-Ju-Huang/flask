from confluent_kafka import Producer
import sys
import time

def to_kafka(m_id):
    # kafka
    props = {'bootstrap.servers': '35.201.205.44:9092'}
    producer = Producer(props)
    topicName = 'dailyEat'

    try:
        kafka_msg = f'{m_id}'
        producer.produce(topicName, value=kafka_msg)
        producer.flush()
        print(f' ==> message sent to kafka : {kafka_msg}')
    except BufferError:
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    producer.flush()