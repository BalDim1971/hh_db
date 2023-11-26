##############################################################################################################
'''
Основной запускающий файл.

Получаем от пользователя необходимые данные для поиска.
Выводим на экран полученную информацию
'''
##############################################################################################################

from src.config import config
from src.BDCreator import BDCreator
from src.HeadHunterAPI import HeadHunterAPI
from src.DBManager import DBManager


def init_bd(params: dict) -> BDCreator:
	'''
	Инициируем базу данных
	
	:return: Указатель на созданный объект для работы с БД
	'''
	
	# Проверяем возможность подключения к БД.
	bd_hh = BDCreator(params)
	bd_hh.create_db()
	bd_hh.create_table_hh_companies()
	bd_hh.create_table_hh_vacancies()
	
	return bd_hh


def connect_to_hh(keyword='Python', count_company = 15):
	'''
	Посылаем запрос к headhunter.ru, получаем данные и преобразуем в нужный формат
	
	:return: кортеж из словаря и списка
	'''
	
	hh_api = HeadHunterAPI(keyword)
	print("Ожидайте, идет опрос сайта headhunter.ru")
	employers = hh_api.get_employers(count_company)
	vacancies = hh_api.get_vacancies()
	return employers, vacancies


def save_data(bd_hh: BDCreator, employers, vacancies):
	'''
	Сохраняем списки компаний и вакансии
	
	:param bd_hh: Указатель на базу данных.
	:param employers: Список компаний.
	:param vacancies: Список вакансий.
	:return:
	'''
	
	bd_hh.insert_table_hh_company(employers)
	bd_hh.insert_table_hh_vacancies(vacancies)


def main():
	'''
	Основная функция.
	
	1. Инициирует обмен с headhunter.ru.
	2. Получает данные с сайта.
	3. Инициирует соединение с БД
	4. Сохраняет полученные данные в БД.
	
	Возвращает успешность(?) операций
	Продумать вариант: True | False или код ошибки.
	:return:
	'''
	
	# Получаем настройки для работы с БД
	params = config()

	# Инициируем базу данных
	bd_hh = init_bd(params)
	
	# Получаем ключевое слово
	keyword = input('Введите слово для запроса (по умолчанию "Python"): ')
	if len(keyword) == 0:
		keyword = 'Python'
	
	count_company = input('Укажите количество компаний для поиска (по умолчанию 15) (10-15): ')
	if len(count_company) == 0 or not count_company.isdigit():
		count_company = 15
	count_company = int(count_company)
	
	# Подключаемся к headhunter.ru, получаем данные и преобразуем в нужный формат
	employers, vacancies = connect_to_hh(keyword, count_company)
	
	# Записываем данные в БД
	save_data(bd_hh, employers, vacancies)
	
	db_manager = DBManager(params)
	
	company_and_vacancies = db_manager.get_companies_and_vacancies_count()
	print('\nСписок компаний и количество вакансий')
	for row in company_and_vacancies:
		print(row[0], row[1])
	
	all_vacancies = db_manager.get_all_vacancies()
	print('\nСписок всех вакансий')
	for row in all_vacancies:
		print(row)
		
	avg_salary = db_manager.get_avg_salary()
	print('\nСредняя зарплата')
	for row in avg_salary:
		print(row[0])
	
	high_salary = db_manager.get_vacancies_with_higher_salary()
	print('\nВакансии с зарплатой выше средней')
	for row in high_salary:
		print(row)
	
	keyword = input('\nВведите слово для поиска (по умолчанию "Стажер"): ')
	if len(keyword) == 0:
		keyword = 'Стажер'
	find_keyword = db_manager.get_vacancies_with_keyword(keyword)
	print(f'\nВакансии с наличием слова "{keyword}"')
	for row in find_keyword:
		print(row)


if __name__ == '__main__':
	main()