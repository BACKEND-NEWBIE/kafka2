from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

value_schema_str = """
{"namespace": "student.avro",
 "type": "record",
 "doc": "This is an example of Avro.",
 "name": "Student",
 "fields": [
     {"name": "name", "type": ["null", "string"], "default": null, "doc": "Name of the student"},
     {"name": "class", "type": "int", "default": 1, "doc": "Class of the student"}
 ]
}
"""

value_schema = avro.loads(value_schema_str)

c = AvroConsumer({
    'bootstrap.servers': 'kafka01,kafka02,kafka03',
    'group.id': 'python-groupid01',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': 'http://kafka03:8081'},reader_value_schema=value_schema)

c.subscribe(['peter-avro01-kafka1'])

while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value())

c.close()