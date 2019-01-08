from __future__ import print_function
from terminaltables import AsciiTable
import requests
import pprint
from itertools import groupby

def predict_rub_salary(salary_dict):
    if salary_dict is None:
        return None
    elif salary_dict['currency'] == 'RUR':
        try:
            if (salary_dict['from'] is None) and (salary_dict['to'] is not None):
                return int(salary_dict['to']) * 0.8
            elif (salary_dict['from'] is not None) and (salary_dict['to'] is None):
                return int(salary_dict['from'] * 1.2)
            elif (salary_dict['from'] is None) and (salary_dict['to'] is None):
                return None
            else:
                return int((int(salary_dict['from']) + int(salary_dict['to']))/2)
        except:
            return None
    else:
        return None


def get_main_vacancies_qty(id_list):
    """Extract image links.

    Args:
        id_list(list): the list of images ID
    Returns:
        id_list(list): the list of urls for images
    """
    main_vacancies_dict = {}
    id_list.sort()
    for id in id_list:
        params = {
            'text': 'Программист {}'.format(id),
            'area': 1,
            'from': 'cluster_area',
            'period': 30
        }
        _url = 'https://api.hh.ru/vacancies'
        response = requests.get(_url, params=params)
        if response.ok:
            main_vacancies_dict.update({id: [response.url, response.json()['pages']]})
        else:
            return None
    return main_vacancies_dict


def make_page_vacancy_url(vacancies_dict):
    new_vacancies_dict = []
    for lang, [_url, _pages_qty] in vacancies_dict.items():
        for page_number in range(0, _pages_qty):
            new_vacancies_dict.append({lang: '{}&page={}'.format(_url,
                                                                 str(page_number))})
    return new_vacancies_dict


def extract_vacancy_url(url_dict):
    for lang, _url in url_dict.items():
        salary_list = []
        response = requests.get(_url)
        if response.ok:
            fetch = response.json()['items']
            for vacancy in fetch:
                salary_list.append((lang, predict_rub_salary(vacancy['salary'])))
            return salary_list
        else:
            return None


def make_salary_stat(raw_data):
    salary_stat = {}
    languages_raw_data_list = []
    data = sorted(raw_data, key=lambda x: x[0])
    for k, g in groupby(data, lambda x: x[0]):
        languages_raw_data_list.append(list(g))

    for languages_raw in languages_raw_data_list:
        languages_raw_not_none = [x for x in languages_raw if x[1] is not None]
        languages_mean = sum([(i[1]) for i in languages_raw_not_none]) // \
                         len([(i[1]) for i in languages_raw_not_none])

        language_stat = {languages_raw_not_none[0][0]:
                             {'vacancies_found': len(languages_raw),
                              'vacancies_processed': len(languages_raw_not_none),
                              'average_salary': int(languages_mean)
                              }
                         }
        salary_stat.update(language_stat)
    return salary_stat


def print_language_stat_asciitables(title, stat_dict):
    top = ['Язык программирования', 'Найдено вакансий', 'Обработано',
           'Средняя зарплата']
    _table_data = []
    for language, language_stat in stat_dict.items():
        _table_data.append([language,
                            language_stat['vacancies_found'],
                            language_stat['vacancies_processed'],
                            language_stat['average_salary']])

    _table_data.insert(0, top)

    table_instance = AsciiTable(_table_data, title)
    table_instance.justify_columns[2] = 'left'
    print(table_instance.table)


def make_headhunter_salary_statistics(_languages):
    main_vacancies_list = get_main_vacancies_qty(_languages)
    all_vacancies_dict = make_page_vacancy_url(main_vacancies_list)
    temp_vacancy_language_list = [extract_vacancy_url(x) for x in
                                  all_vacancies_dict]
    vacancy_language_list = (
    [vacancy for sublist in temp_vacancy_language_list for vacancy in sublist])
    return make_salary_stat(vacancy_language_list)


if __name__ == '__main__':

    advisable_languages = ['Java', 'PHP', 'С++', 'R', 'Python', 'JavaScript', 'Delphi', 'Go', 'Swift', 'Ruby']

    hh = make_headhunter_salary_statistics(advisable_languages)
    print_language_stat_asciitables('HeadHunter Moscow', hh)

