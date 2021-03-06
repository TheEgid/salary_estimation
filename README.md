# Сравниваем вакансии программистов
Проект предназначен для получения статистики зарплат программистов с сайтов hh.ru и superjob.ru в разбивке по языкам программирования.

### Как установить

Скачиваем файлы в папку salary_estimation. Для получения данных с superjob в этой же папке создаем .env файл. 
Ваш .env должен содержать строки:
```
key=ваш_ключ_приложения_с_сайта_superjob
id=ваш_айди_приложения_с сайта_superjob
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Использование

Используем консольный ввод. Аргументом передаем комманду.
Допустимые команды - 
all - выводит в ответ статистику по зарплатам программистов с сайтов hh.ru и superjob.ru
hh - выводит в ответ статистику по зарплатам программистов только с сайта hh.ru
sj - выводит в ответ статистику по зарплатам программистов только с сайта superjob.ru

Примеры запуска из консоли -
```
python3 main.py all
python3 main.py sj
python3 main.py hh
```
И программа выведет в консоль статистику в аккуратной табличной форме.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
