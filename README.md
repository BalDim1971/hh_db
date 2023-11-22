# Курсовой проект по Python

# Работа с базами данных

## Задание

В рамках проекта необходимо:

- получить данные о компаниях и вакансиях с сайта hh.ru,
- спроектировать таблицы в БД PostgreSQL,
- загрузить полученные данные в созданные таблицы.

## Требования

1. Получить данные о работодателях и их вакансиях с сайта hh.ru. Использовать публичный API hh.ru и библиотеку
   requests.
2. Выбрать не менее 10 компаний для получения данные о вакансиях.
3. Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях.
4. Создать функции по работе с БД с использованием библиотеки psycopg2.
5. Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
6. Создать класс DBManager для работы с данными в БД.

## Требования к классу DBManager

Должен подключаться к БД PostgreSQL и иметь следующие методы:

1. get_companies_and_vacancies_count() — возвращает список всех компаний и количество вакансий у каждой компании.
2. get_all_vacancies() — возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
   ссылки на вакансию.
3. get_avg_salary() — возвращает средней зарплаты по вакансиям.
4. get_vacancies_with_higher_salary() — возвращает список всех вакансий, у которых зарплата выше средней по всем
   вакансиям.
5. get_vacancies_with_keyword() — возвращает список всех вакансий, в названии которых содержатся переданные в метод
   слова, например python.

## Выходные данные

- Информация о компаниях и вакансиях, полученная с платформы hh.ru и сохраненная базе данных.
- Средняя зарплата по вакансиям.
- Список вакансий с зарплатой выше чем средняя.
- Список вакансий по ключевому слову.

## Использование

Пользователь вводит с клавиатуры критерии для поиска вакансий.
На экран отображаются вакансии по критериям, заданным пользователем