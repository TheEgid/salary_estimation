"""Get HH Stat."""
from __future__ import print_function
import requests
from stat_services import predict_rub_salary
from stat_services import make_salary_stat
from stat_services import group_list


def get_vacancies_pages_qty_list(language_list, search_period=30):
    _url = 'https://api.hh.ru/vacancies'
    all_pages_vacancies_list = []
    for language in language_list:
        params = {
            'text': 'Программист {}'.format(language),
            'area': 1,
            'from': 'cluster_area',
            'period': search_period
        }
        response = requests.get(_url, params=params)
        if response.ok:
            all_pages_vacancies_list.append((language, response.json()['pages']))
        else:
            raise ValueError('response error!')
    return all_pages_vacancies_list


def make_page_vacancy_url_list(qtyes, search_period=30):
    lang, _pages_qty = qtyes
    new_vacancies = []
    url = 'https://api.hh.ru/vacancies'
    for page_number in range(0, _pages_qty):
        params = {
            'text': 'Программист {}'.format(lang),
            'area': 1,
            'from': 'cluster_area',
            'period': search_period,
            'page': page_number
        }
        new_vacancies.append({lang: (url, params)})
    return new_vacancies


def extract_language_and_salary(url_dict):
    """
    Extract.

    Args:
        url_dict(dict)
    Returns:
        language_and_salary_list(list)
    Raises:
        ValueError: Raises an exception.
    """
    language_and_salary_list = []
    for language, (_url, _url_params) in url_dict.items():
        response = requests.get(_url, params=_url_params)
        if response.ok:
            fetch = response.json()['items']
            for vacancy in fetch:
                language_and_salary_list.append((language,
                                                 predict_rub_salary(vacancy['salary'])))
            return language_and_salary_list
        else:
            raise ValueError('response error!')


def make_hh_salary_statistics(language_list):
    language_list.sort()
    vacancies_pages_qty = get_vacancies_pages_qty_list(language_list)
    all_vacancies_urls = [make_page_vacancy_url_list(x) for x in
                          vacancies_pages_qty]
    temp_vacancy_language_list = []
    for lang in all_vacancies_urls:
        for salary_dict in lang:
            temp_vacancy_language_list.append(
                extract_language_and_salary(salary_dict))

    vacancy_language_list = \
        group_list([vacancy for sublist in temp_vacancy_language_list
                    for vacancy in sublist])
    return make_salary_stat(vacancy_language_list)

