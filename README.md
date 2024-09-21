# Telegram-бот для управления расписанием колледжа

## Описание

Этот проект представляет собой Telegram-бота для управления расписанием колледжа. Бот помогает студентам быстро находить информацию о преподавателях, аудиториях, группах и курсовых занятиях через удобный интерфейс с кнопками. Также есть возможность просматривать расписание звонков и связываться с разработчиком.

## Возможности бота

- Выбор преподавателя по первой букве фамилии с дальнейшим просмотром расписания на web-странице.
- Поиск аудитории по этажам здания.
- Просмотр расписания для выбранной группы.
- Отправка актуального расписания звонков в виде изображения.
- Интерактивное главное меню с кнопками для быстрого доступа к функциям.
- Связь с разработчиком через web-форму.
- Возможность массовой рассылки сообщений пользователям (для администратора).
- Автоматический перезапуск бота каждые 5 минут.

## Стек технологий

- **Язык программирования:** Python
- **Библиотеки:** 
  - `aiogram` для работы с Telegram API
  - `aiohttp` для вебхуков и асинхронных запросов
  - `logging` для логирования активности пользователей
  - `asyncio` для асинхронного выполнения задач
- **Платформа:** Alwaysdata

## Структура проекта

- **`main.py`** — основной файл, который управляет логикой бота, включая обработку команд, сообщений и колбэков.
- **`Data.py`** — файл данных, содержащий информацию о преподавателях, аудиториях и курсах.

## Как запустить

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo-url.git
   ```

2. Перейдите в директорию проекта:
   ```bash
   cd college-schedule-bot
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. В файле `main.py` замените значение переменной `TOKEN` на ваш собственный токен Telegram-бота, полученный у [BotFather](https://t.me/BotFather).

5. Запустите бота:
   ```bash
   python main.py
   ```

## Основные файлы

### `main.py`
Файл содержит основную логику работы бота, включая следующие функции:
- **Главное меню:** Создание клавиатуры с основными опциями (выбор преподавателя, аудитории, курсы и т.д.).
- **Логирование:** Отслеживание действий пользователя и сохранение его ID.
- **Обработка команд:** Реализация обработки команды `/start` и других текстовых команд, а также колбэков для выбора преподавателей и аудиторий.
- **Массовая рассылка:** Функция для администратора, позволяющая отправлять сообщения всем активным пользователям.

### `Data.py`
Содержит словари с информацией о:
- Преподавателях и их расписаниях.
- Аудиториях по этажам.
- Курсах и группах с ссылками на соответствующие страницы.

## Пример использования

1. Пользователь вводит команду `/start`, и бот предлагает меню с выбором действий.
2. При выборе опции "📚 Выбрать преподавателя", бот предложит выбрать первую букву фамилии преподавателя.
3. После выбора преподавателя, бот предоставит ссылку на расписание выбранного преподавателя.
4. Администратор может отправлять массовые сообщения, используя команду `/broadcast <текст>`.

## Контакты

Если у вас возникли вопросы или предложения, вы можете связаться с разработчиком через встроенную форму в боте или через [ссылку на форму](https://forms.gle/2L1MHuK7G7zApePPA).

## Лицензия

Этот проект распространяется под [лицензией MIT](LICENSE).