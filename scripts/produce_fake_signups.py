from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

fake = Faker()

while True:
    data = {
        "name": fake.name(),
        "email": fake.email(),
        "age": random.randint(18, 60)
    }
    producer.send("user-signups", value=data)
    print("Produced:", data)
    time.sleep(1)
