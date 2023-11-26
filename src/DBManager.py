##############################################################################################################
"""
Файл с описанием класса DBManager.

Класс DBManager умеет подключаться к БД PostgreSQL и имеет методы:
— для возврата списка всех компаний и количество вакансий у каждой компании.
— для возврата списка всех вакансий с указанием названия компании,
  названия вакансии и зарплаты и ссылки на вакансию.
— для возврата средней зарплаты по вакансиям.
— для возврата списка всех вакансий, у которых зарплата выше средней по всем вакансиям.
— для возврата списка всех вакансий, в названии которых содержатся переданные в метод
   слова, например python.
"""

##############################################################################################################

from src.config import NAME_BD
import psycopg2


class DBManager:
	
	def __init__(self, params: dict):
		self.params = params
		self.dbname = NAME_BD
	
	def get_companies_and_vacancies_count(self):
		'''
		Считывает из БД и возвращает список всех компаний и количество вакансий по каждой компании.
		
		:return: Список пар (имя_компании + количество_вакансий)
		'''
		
		conn = psycopg2.connect(dbname=self.dbname, **self.params)
		conn.autocommit = True
		
		with conn.cursor() as cur:
			cur.execute('''SELECT DISTINCT company_name, COUNT(title)
						FROM hh_companies, hh_vacancies
						WHERE hh_vacancies.company_id = hh_companies.company_id
						GROUP BY company_name
						ORDER BY company_name;''')
			result = cur.fetchall()
			
		cur.close()
		conn.close()
		return result
	
	def get_all_vacancies(self):
		'''
		Считывает из БД и возвращает список всех вакансий.
		Название компании, названия вакансии, зарплаты и ссылки на вакансию.
		
		:return: Список вакансий
		'''
		
		conn = psycopg2.connect(dbname=self.dbname, **self.params)
		conn.autocommit = True
		
		with conn.cursor() as cur:
			cur.execute('''SELECT company_name, title, salary_from, salary_to, currency, url
						FROM hh_vacancies
						INNER JOIN hh_companies USING(company_id)
						WHERE hh_vacancies.company_id = hh_companies.company_id
						ORDER BY company_name;''')
			result = cur.fetchall()
		
		cur.close()
		conn.close()
		return result
	
	def get_avg_salary(self):
		'''
		Считывает из БД и возвращает среднюю зарплату по вакансиям.
		Из усреднения отключаем нулевую зарплату и зарплату в других валютах

		:return: Средняя зарплата
		'''
		
		conn = psycopg2.connect(dbname=self.dbname, **self.params)
		conn.autocommit = True
		
		with conn.cursor() as cur:
			cur.execute("""SELECT AVG(ABS(salary_to + salary_from) / 2)
						FROM hh_vacancies
						WHERE salary_to>0 AND salary_from>0 AND currency='RUR';""")
			result = cur.fetchall()
		
		cur.close()
		conn.close()
		return result
	
	def get_vacancies_with_higher_salary(self):
		'''
		Считывает из БД и возвращает вакансии с зарплатой выше средней.

		:return: Список вакансий
		'''
		
		conn = psycopg2.connect(dbname=self.dbname, **self.params)
		conn.autocommit = True
		
		with conn.cursor() as cur:
			cur.execute("""SELECT company_name, title, salary_from, salary_to, currency, url
						FROM hh_vacancies
						INNER JOIN hh_companies USING(company_id)
						WHERE hh_vacancies.company_id = hh_companies.company_id
						AND currency = 'RUR'
						AND salary_to > ( SELECT AVG(ABS(salary_to + salary_from) / 2)
						FROM hh_vacancies WHERE salary_to>0 AND salary_from>0 AND currency='RUR' )
						ORDER BY company_name;""")
			result = cur.fetchall()
		
		cur.close()
		conn.close()
		return result
	
	def get_vacancies_with_keyword(self, keyword: str):
		'''
		Считывает из БД и возвращает список всех вакансий, где встечаеися слово.

		:return: Список пар (имя_компании + количество_вакансий)
		'''
		
		conn = psycopg2.connect(dbname=self.dbname, **self.params)
		conn.autocommit = True
		
		with conn.cursor() as cur:
			cur.execute(f"""SELECT * FROM hh_vacancies
						WHERE title ILIKE '%{keyword}%';""")
			result = cur.fetchall()
		
		cur.close()
		conn.close()
		return result
