from confluent_kafka import Consumer

broker = 'kafka01, kafka02, kafka03'
group = 'peter-consumer01'
topic = 'peter-test06'

c = Consumer({
    'bootstrap.servers': broker,
    'group.id': group,
    'auto.offset.reset': 'earliest'
})
c.subscribe([topic])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print('Topic: {}, '
          'Partition: {}, '
          'Offset: {}, '
          'Received message: {}'.format(msg.topic(),
                                        msg.partition(),
                                        msg.offset(),
                                        msg.value().decode('utf-8')))
c.close()
