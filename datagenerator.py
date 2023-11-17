import random
from datetime import datetime, timedelta
import faker  # You may need to install this library using: pip install faker

# Create a Faker instance to generate fake data
fake = faker.Faker()

def generate_random_message(usernames, num_messages):
    date_format = "%d/%m/%Y, %H:%M - "
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)

    messages = []
    for _ in range(num_messages):
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days),
                                             hours=random.randint(0, 23),
                                             minutes=random.randint(0, 59))
        username = random.choice(usernames)

        # Determine the message type
        message_type = random.choices(['text', 'link', 'media'], weights=[0.9, 0.05, 0.05])[0]

        if message_type == 'text':
            message_content = fake.sentence()
        elif message_type == 'link':
            message_content = fake.url()
        elif message_type == 'media':
            message_content = f"Attached Media: {fake.file_path()}"

        message = f"{random_date.strftime(date_format)}{username}: {message_content}"
        messages.append(message)

    return "\n".join(messages)

# Generate a dataset with 1000 random messages from three users
usernames = ["user1", "user2", "user3"]
dataset = generate_random_message(usernames, 1000)

# Save the dataset to a file
with open('large_chat_dataset.txt', 'w') as file:
    file.write(dataset)

