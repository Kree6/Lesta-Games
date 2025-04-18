# 🔍 TF-IDF Analyzer — FastAPI Web App

Веб-приложение для анализа текста с использованием метрики TF-IDF.  
Позволяет загрузить `.txt` файл и получить 50 наиболее информативных слов в виде таблицы с их частотой и обратной частотой документа.

## 🚀 Демонстрация возможностей

- Загрузка текстового файла через веб-интерфейс
- Парсинг и обработка текста на Python
- Вывод 50 слов с:
  - **TF** — частота слова в документе
  - **IDF** — обратная частота документа
- Сортировка по убыванию IDF
- Поддержка **русского языка**
- Постраничный вывод (по 50 слов на страницу)
- Кнопка очистки результатов
- Фронтенд: стилизованная HTML-страница с анимациями

## 🛠️ Технологии

- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- Jinja2 (шаблонизатор)
- HTML / CSS / JavaScript
- Bootstrap + кастомные стили
