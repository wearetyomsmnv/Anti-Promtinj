import sys
import argparse
import openai
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

# Парсинг аргументов командной строки
commands = argparse.ArgumentParser(description='Basic parameters')
commands.add_argument('query', type=str, help='Query for chatgpt')
commands.add_argument('api_key', help='Specify the api-key for chat-gpt')

args = commands.parse_args()

query = args.query
api_key = args.api_key

train_data = [
    "SELECT * FROM users WHERE name = 'John';",
    "DROP DATABASE users;",
    "ls -l /home/user/",
    "rm -rf /",
    "SELECT * FROM users WHERE name = 'Sarah';",
    "INSERT INTO users (name, password) VALUES ('Admin', 'password');",
    "cp /var/log/messages /home/user/",
    "mkdir /tmp/backdoor && echo 'sudo /bin/bash' > /tmp/backdoor/root && chmod +x /tmp/backdoor/root"
]
train_labels = [1, 1, 0, 0, 1, 1, 0, 1]

# Извлечение признаков из данных для обучения
vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(train_data)

# Обучение классификатора с помощью метода опорных векторов
clf = svm.SVC()
clf.fit(train_vectors, train_labels)

# Использование OpenAI API для улучшения классификации
openai.api_key = args.api_key
model_engine = "text-davinci-002"
query = openai.Completion.create(
    engine=model_engine,
    prompt=args.query,
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.5,
)['choices'][0]['text']

# Извлечение признаков из запроса
query_vector = vectorizer.transform([query])

# Классификация запроса
result = clf.predict(query_vector)
if result[0] == 1:
    print("Запрос содержит SQL-инъекцию")
    sys.exit(0)
elif result[0] == 0:
    print("ok")
