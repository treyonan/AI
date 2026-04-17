from faker import Faker
import csv 
import random 


fake =Faker()

with open('friends.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name','Age','City','Email'])

    for _ in range(100):
        name = fake.name()
        age = random.randint(18, 65)
        city = fake.city()
        email = fake.email()
        writer.writerow([name, age, city, email])


        