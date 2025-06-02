# Telegram Bot — Маркетинговый Бот с Меню и Оплатой

Этот бот реализован на базе `Aiogram 3.x` и поддерживает следующее:
- Приветственное меню
- Галерею примеров
- Каталог с вариантами оплаты
- Покупку подписки через Telegram Payments
- Поддержку FSM и `ChatAction.TYPING` для имитации набора

---

## 📦 Функциональность

- `/start` — запуск меню с приветствием
- Inline-кнопки для навигации
- Оплата с помощью Card, Stripe, Lava
- Интеграция с Telegram Invoice (`LabeledPrice`)
- Автоматическое отображение "набирает сообщение..."

---

## 📁 Структура проекта

```
bot/
├── bot.py                 # Инициализация бота
├── handlers/
│   └── user_handlers.py   # Основные обработчики
├── keyboards/buttons.py   # Кнопки клавиатуры
├── sourcefile/
│   ├── texts.py           # Тексты сообщений
│   └── pictures.py        # Пути к изображениям
├── controllers.py         # Отправка сообщений, работа с пользователями
├── states.py              # FSM-состояния
├── callbacks.py           # Callback-константы
├── filters.py             # Кастомные фильтры
├── types.py               # Доп. типы (например, NavigationHistory)
config.py                  # Конфиг
models.py                  # ORM-модель User
main.py                    # Точка входа
logger.py                  # Логирование
```

---

## ⚙️ Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/chelush/cheese_bot.git
cd telegram-bot
```

### 2. Установи зависимости

```bash
pip install -r requirements.txt
```

### 3. Создай `.env`

```python
TELEGRAM_BOT_TOKEN=<TELEGRAM_TOKEN>

POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

### 4. Запусти бота

```bash
python main.py
```

---

## 🐳 Docker (опционально)

```bash
docker build -t telegram-bot .
docker run --env-file .env telegram-bot
```

---

## 🛠 Используемое

- Python 3.12+
- Aiogram 3.x
- Telegram Bot API
- Docker (опционально)

---

## 📌 Примечание

Бот использует `@with_typing`, который показывает "печатает...", прежде чем отправить сообщение, для более естественного UX.

FSM используется для хранения состояния пользователя при работе с заказами.

---

## 🧑 Автор

Разработано студентом НИУ ВШЭ ❤️