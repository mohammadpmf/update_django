# Providers
from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)
print(f"ipv4 private:{fake.ipv4_private()}")
print(f"ipv4 public:{fake.ipv4_public()}")