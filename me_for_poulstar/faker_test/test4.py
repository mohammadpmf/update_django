import faker
from datetime import datetime

faker = faker.Faker()
print(faker.date_time_ad(start_datetime=datetime(2022,6,1), end_datetime=datetime(2023,1,1)))
