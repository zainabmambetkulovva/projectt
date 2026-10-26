# Анализ и визуализация данных о продажах

Проект для анализа данных о продажах с использованием Pandas и Matplotlib.

## Структура проекта

```
├── data/
│   └── sales.csv          # Данные о продажах
├── output/                # Сохраненные графики
├── main.py                # Основной скрипт анализа
├── requirements.txt       # Зависимости
├── .gitignore
└── README.md
```

## Установка и запуск

### 1. Создайте виртуальное окружение

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Запустите анализ

```bash
python main.py
```

Графики будут сохранены в папке `output/`:
- `revenue_by_category.png` — столбчатая диаграмма выручки по категориям
- `revenue_by_date.png` — линейный график выручки по датам
- `sales_comparison.png` — график сравнения продаж

## Данные

Файл `data/sales.csv` содержит следующие столбцы:
- `date` — дата продажи
- `category` — категория товара (Electronics, Clothing, Food)
- `quantity` — количество проданных единиц
- `revenue` — выручка

## Требования

- Python 3.7+
- pandas
- matplotlib
