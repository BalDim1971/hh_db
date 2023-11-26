##########################################################################################################
'''
Файл описывает класс доступа к API сайта hh.ru
'''
##########################################################################################################

from abc import ABC, abstractmethod
import requests
from src.config import HH_URL
import time


class AbstractAPI(ABC):
	'''
	Абстрактный класс, предоставляющий шаблон класса для создания классов доступа к сайтам с вакансиями.

	Содержит параметры:
	__url: str - адрес сайта вакансий
	headers - заголовок запроса для доступа к данным сайта
	params - параметры запроса
	json_data - данные, полученные с сайта, преобразованные в формат json
	'''
	
	def __init__(self, url: str):
		'''
		Инициируем базовый класс.

		Параметры:
		url: str - адрес сайта вакансий
		'''
		self.__url = url
	
	@property
	def url(self):
		'''
		Возвращает значение приватной переменной - адреса сайта
		:return: адрес сайта
		'''
		
		return self.__url
	
	@url.setter
	def url(self, url: str):
		'''
		Устанавливаем новое значение адреса сайта.

		Параметр:
		url: str - новый адрес
		'''
		
		self.__url = url
	

class HeadHunterAPI(AbstractAPI):
	'''
	Класс реализует доступ через API к сайту с вакансиями hh.ru
	'''
	
	def __init__(self, keyword: str, count_company=15):
		'''
		Инициируем класс доступа к hh.ru
		'''
		
		self.count_company = count_company
		self.json_data = {}
		self.employers = {}
		self.vacancies = []
		
		self.__params = {
			'items_on_page': 200,
			'per_page': 100,
			'page': 0,
			'archive': False,
			'text': keyword
		}
		
		super().__init__(HH_URL)
	
	def get_vacancies(self):
		'''
		Получает с сайта вакансии.

		:return: Список полученных с сайта вакансий в виде списка словарей
		'''
		
		for employer_id in self.employers.keys():
			self.__params['employer_id'] = employer_id
			response = requests.get(self.url, params=self.__params, timeout=10)
			response.raise_for_status()
			self.json_data.clear()
			self.json_data = response.json()['items']
			time.sleep(0.5)
			
			for item in self.json_data:
				one_vacancy = {}
				if item['salary'] is None:
					item['salary'] = {}
					item['salary']['from'] = 0
					item['salary']['to'] = 0
					item['salary']['currency'] = 'RUR'
				if item['salary']['from'] is None:
					item['salary']['from'] = 0
				if item['salary']['to'] is None:
					item['salary']['to'] = 0
				
				one_vacancy['vacancies_id'] = item['id']
				one_vacancy['title'] = item['name']
				one_vacancy['url'] = item['alternate_url']
				one_vacancy['description'] = item['snippet']['responsibility']
				one_vacancy['salary_from'] = item['salary']['from']
				one_vacancy['salary_to'] = item['salary']['to']
				one_vacancy['currency'] = item['salary']['currency']
				one_vacancy['city'] = item['area']['name']
				one_vacancy['date'] = item['published_at']
				one_vacancy['employer_id'] = item['employer']['id']
				one_vacancy['employer_name'] = item['employer']['name']

				self.vacancies.append(one_vacancy)
		
		return self.vacancies
	
	def get_employers(self):
		'''
		Пытаемся вернуть компании в соответствии с ключевым словом для поиска
		
		Создаем список из self.count_company неповторяющихся компаний
		:return: Список id компаний и их названий
		'''
		
		#
		response = requests.get(self.url, params=self.__params, timeout=10)
		response.raise_for_status()
		self.json_data = response.json()['items']
		
		for item in self.json_data:
			if len(self.employers) == self.count_company:
				break
			if item['employer']['id'] in self.employers.keys() or item['employer']['name'] in self.employers.values():
				continue
			self.employers[item['employer']['id']] = item['employer']['name']
		
		return self.employers

##################################################################################################
