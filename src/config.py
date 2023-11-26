##############################################################################################################
'''
Файл для получения настроек и инициализации констант.

Получаем из файла database.ini данные для подключения к БД
Возможно стоит добавить данные для подключения к headhunter.ru
Инициируем константу для адреса сайта, с которых берем вакансии.
'''
##############################################################################################################

from configparser import ConfigParser

HH_URL: str = 'https://api.hh.ru/vacancies'
NAME_BD = 'headhunter'

def config(filename="database.ini", section="postgresql"):
	'''
	Функция считывает из файла настройки и возвращает в виде словаря
	:param filename: имя файла настроек
	:param section: раздел для инициализации
	:return: словарь с переменными
	'''
	
	# Создаем парсер для разбора настроечного файла
	parser = ConfigParser()
	
	# Читаем настроечный файл
	parser.read(filename)
	if parser.has_section(section):
		params = parser.items(section)
		db = dict(params)
	else:
		raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))
	return db

#########################################################
