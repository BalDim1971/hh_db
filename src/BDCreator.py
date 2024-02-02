##############################################################################################################
'''
Файл с описанием класса DBCreator

Класс DBCreator предназначен для:
— создания базы данных;
— создания таблиц.
'''
##############################################################################################################

import psycopg2
from src.config import NAME_BD


class BDCreator:
    """
    Класс для создания базы данных.

    Атрибуты:
    dbname - имя базы данных;
    params - параметры подключения к БД.
    """

    def __init__(self, params: dict):
        """
        Инициируем переменные класса.

        :param dbname: Имя базы данных.
        :param params: Параметры подключения к БД.
        """

        self.dbname = NAME_BD
        self.params = params

    def create_db(self):
        """
        Создаем БД с проверкой наличия
        :return:
        """

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname = '{self.dbname}'")
            result = cur.fetchone()
            if result[0] == 0:
                cur.execute(f"CREATE DATABASE {self.dbname};")
                conn.commit()
            else:
                print(f"База данных с названием {self.dbname} уже существует.")
        cur.close()
        conn.close()

    def create_table_hh_companies(self):
        """
        Создание таблицы с данными компаний
        :return:
        """

        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS hh_vacancies;')
            cur.execute('DROP TABLE IF EXISTS hh_companies;')
            cur.execute('''CREATE TABLE IF NOT EXISTS hh_companies(
                           company_id int,
                           company_name varchar(100) NOT NULL,
                           CONSTRAINT pk_hh_companies_company_id PRIMARY KEY (company_id)
                        );''')
        conn.close()

    def create_table_hh_vacancies(self):
        """
		Создание таблицы с вакансиями
		:return:
        """

        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS hh_vacancies(
	                        vacancy_id int UNIQUE,
	                        title varchar(100),
	                        url varchar(200),
	                        description text,
	                        salary_from int,
	                        salary_to int,
	                        currency varchar(10),
	                        city varchar(50),
	                        company_id int,
	                        date text,
	                        CONSTRAINT fk_hh_vacancies_hh_companies FOREIGN KEY(company_id) REFERENCES hh_companies(company_id)
	                    );''')
            conn.commit()

    def insert_table_hh_company(self, data: dict):
        """
    	Вставить в таблицу БД данные по компании

    	:param data: данные о компании;
    	:return:
    	"""

        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for key, value in data.items():
                cur.executemany("INSERT INTO hh_companies VALUES (%s, %s) "
                            "ON CONFLICT (company_id) DO NOTHING",
                            [(key, value)])

    def insert_table_hh_vacancies(self, data: list):
        """
		Вставить в таблицу БД данные о вакансиях

		:param data: данные о вакансиях;
		:return:
		"""

        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        conn.autocommit = True

        print(len(data))
        with conn.cursor() as cur:
            for item in data:
                cur.executemany("INSERT INTO hh_vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            "ON CONFLICT(vacancy_id) DO NOTHING",
                            [(item['vacancies_id'],
                              item['title'],
                              item['url'],
                              item['description'],
                              item['salary_from'],
                              item['salary_to'],
                              item['currency'],
                              item['city'],
                              item['employer_id'],
                              item['date'])])

##############################################################################################################
