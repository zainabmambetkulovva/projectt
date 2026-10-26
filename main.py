import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime


def load_data(filepath):
    """Загружает CSV-файл и проверяет наличие необходимых столбцов."""
    required_columns = ['date', 'category', 'quantity', 'revenue']
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    df = pd.read_csv(filepath)
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Отсутствуют необходимые столбцы: {missing_columns}")
    
    # Обработка пустых значений
    df = df.dropna()
    
    # Преобразование даты
    df['date'] = pd.to_datetime(df['date'])
    
    # Преобразование числовых столбцов
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    
    return df


def analyze_data(df):
    """Выполняет анализ данных и выводит результаты в терминал."""
    print("=" * 50)
    print("АНАЛИЗ ДАННЫХ О ПРОДАЖАХ")
    print("=" * 50)
    
    # Общая выручка
    total_revenue = df['revenue'].sum()
    print(f"\nОбщая выручка: {total_revenue:.2f}")
    
    # Количество продаж (всех записей)
    total_sales_count = len(df)
    print(f"Количество записей о продажах: {total_sales_count}")
    
    # Общее количество проданных товаров
    total_quantity = df['quantity'].sum()
    print(f"Общее количество проданных товаров: {total_quantity}")
    
    # Средняя выручка на запись
    avg_revenue = df['revenue'].mean()
    print(f"Средняя выручка на запись: {avg_revenue:.2f}")
    
    # Выручка по категориям
    print("\n" + "-" * 30)
    print("Выручка по категориям:")
    print("-" * 30)
    revenue_by_category = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
    for category, revenue in revenue_by_category.items():
        print(f"{category}: {revenue:.2f}")
    
    # Количество продаж по категориям
    print("\n" + "-" * 30)
    print("Количество продаж по категориям:")
    print("-" * 30)
    sales_by_category = df.groupby('category')['quantity'].sum().sort_values(ascending=False)
    for category, quantity in sales_by_category.items():
        print(f"{category}: {quantity}")
    
    # Самая популярная категория по выручке
    top_category_by_revenue = revenue_by_category.idxmax()
    print(f"\nСамая прибыльная категория: {top_category_by_revenue} ({revenue_by_category.max():.2f})")
    
    # Самая популярная категория по количеству проданных товаров
    top_category_by_quantity = sales_by_category.idxmax()
    print(f"Самая популярная категория по количеству: {top_category_by_quantity} ({sales_by_category.max()})")
    
    # Динамика по дням
    print("\n" + "-" * 30)
    print("Выручка по дням:")
    print("-" * 30)
    daily_revenue = df.groupby('date')['revenue'].sum()
    for date, revenue in daily_revenue.items():
        print(f"{date.date()}: {revenue:.2f}")
    
    print("=" * 50)


def create_charts(df, output_dir='output'):
    """Создает и сохраняет графики."""
    # Убедимся что папка существует
    os.makedirs(output_dir, exist_ok=True)
    
    # График 1: Столбчатая диаграмма выручки по категориям
    plt.figure(figsize=(10, 6))
    revenue_by_category = df.groupby('category')['revenue'].sum()
    bars = plt.bar(revenue_by_category.index, revenue_by_category.values, color=['#3498db', '#e74c3c', '#2ecc71'])
    plt.xlabel('Категория')
    plt.ylabel('Выручка')
    plt.title('Выручка по категориям')
    plt.xticks(rotation=45)
    for bar, value in zip(bars, revenue_by_category.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, f'{value:.0f}', 
                 ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'revenue_by_category.png'), dpi=150)
    plt.close()
    print(f"Сохранен график: {output_dir}/revenue_by_category.png")
    
    # График 2: Линейный график выручки по датам
    plt.figure(figsize=(12, 6))
    daily_revenue = df.groupby('date')['revenue'].sum().reset_index()
    plt.plot(daily_revenue['date'], daily_revenue['revenue'], marker='o', linewidth=2, markersize=8)
    plt.xlabel('Дата')
    plt.ylabel('Выручка')
    plt.title('Динамика выручки по дням')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'revenue_by_date.png'), dpi=150)
    plt.close()
    print(f"Сохранен график: {output_dir}/revenue_by_date.png")
    
    # График 3: Сравнение продаж (количество и выручка по категориям)
    plt.figure(figsize=(14, 6))
    
    # Под график 1 - количество по категориям
    plt.subplot(1, 2, 1)
    quantity_by_category = df.groupby('category')['quantity'].sum()
    bars1 = plt.bar(quantity_by_category.index, quantity_by_category.values, color='#3498db', alpha=0.7)
    plt.xlabel('Категория')
    plt.ylabel('Количество проданного')
    plt.title('Количество проданных товаров по категориям')
    plt.xticks(rotation=45)
    for bar, value in zip(bars1, quantity_by_category.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{value:.0f}', 
                 ha='center', va='bottom', fontsize=10)
    
    # Под график 2 - выручка по категориям
    plt.subplot(1, 2, 2)
    revenue_by_category = df.groupby('category')['revenue'].sum()
    bars2 = plt.bar(revenue_by_category.index, revenue_by_category.values, color='#e74c3c', alpha=0.7)
    plt.xlabel('Категория')
    plt.ylabel('Выручка')
    plt.title('Выручка по категориям')
    plt.xticks(rotation=45)
    for bar, value in zip(bars2, revenue_by_category.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, f'{value:.0f}', 
                 ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sales_comparison.png'), dpi=150)
    plt.close()
    print(f"Сохранен график: {output_dir}/sales_comparison.png")


def main():
    """Основная функция запуска анализа."""
    # Путь к CSV-файлу
    data_file = 'data/sales.csv'
    
    # Загрузка данных
    print(f"Загрузка данных из {data_file}...")
    df = load_data(data_file)
    
    print(f"Загружено {len(df)} записей.")
    
    # Анализ данных
    analyze_data(df)
    
    # Создание графиков
    print("\nПостроение графиков...")
    create_charts(df)
    
    print("\nАнализ завершен. Графики сохранены в папке 'output/'.")


if __name__ == '__main__':
    main()
