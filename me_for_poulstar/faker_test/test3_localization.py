# from faker import Faker
# fake = Faker('it_IT')
# for _ in range(10):
#     print(fake.name())


from faker import Faker
fake = Faker(['it_IT', 'ja_JP', 'fa_IR'])
for _ in range(10):
    print(fake.name())

