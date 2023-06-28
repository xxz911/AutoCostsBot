# AutoCostsBot

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![version](https://img.shields.io/badge/Version-v.1.0(Latest)-blue)
![Aigram](https://img.shields.io/badge/Aigram-v.2.25.1-info)


## О проекте
Телеграм бот помогает записывать и анализировать расходы на авто, можно установить лимит, записывать расходы с описанием и по категориям, получать статистику по периодам(день, месяц, год)

## Как установить и запустить проект
1. Скачайте репозиторий себе на компьютер.

2. Создайте виртуальное окружение и активируйте его.
   
  Пример:
  https://docs.python.org/3/library/venv.html

4. Получите свой Token у телеграмм бота @BotFather
   
  Ссылка: https://t.me/BotFather

6. В файле server.py вставьте свой Token вместо API_TOKEN
```bash
22: bot = Bot(token=API_TOKEN)
```

5. Находясь в корневой директории установите все необходимые зависимости и запустите приложение локально командами: 

```bash
  $ pip install -r requirements.txt
  
  $ python server.py
```
## Как использовать проект
Найдите в телеграмме бота(имя указанное при получение Token)

Вы должны увидеть:

<img src="https://github.com/xxz911/xxz911/blob/main/AutoCostBot.jpeg"></img>

Поздравляю! Бот готово для локального использования
