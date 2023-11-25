##############################################################################################################
'''
Файл для получения настроек.

Получаем из файла database.ini данные для подключения к БД
Возможно стоит добавить данные для подключения к headhunter.ru
'''
##############################################################################################################

from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
	'''
	Функция
	:param filename:
	:param section:
	:return:
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
