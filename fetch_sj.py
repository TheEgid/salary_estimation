"""Get SJ Stat."""
import os
import requests
from dotenv import load_dotenv

from fetch_hh import predict_rub_salary
from fetch_hh import make_salary_stat
from fetch_hh import group_salary_list
from fetch_hh import print_language_stat_ascitables


def setNone(v):
    """Setting None if value is Zero."""
    if v == 0:
        return None
    else:
        return v


def connection_sj(_id, _key, language_list, mode='get_number', page_number=0):
    _url = 'https://api.superjob.ru/2.0/vacancies/'
    all_vacancies_dict = {}
    count_vacancies_per_page = 100
    category = 48
    language_list.sort()
    for language in language_list:
        params = {
            'page': page_number,
            'count': count_vacancies_per_page,
            'archive': False,
            'keyword': 'Программист {}'.format(language),
            'not_archive': True,
            'town': 'Москва',
            'catalogues': category
        }
        headers = {'X-Api-App-Id': _key,
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Host': 'api.superjob.ru',
                   'Client Id': _id
                   }
        response = requests.get(_url, headers=headers, params=params)
        if response.ok:
            if mode == 'get_number':
                all_vacancies_dict.update({language: response.json()['total']})
            elif mode == 'get_stata':
                all_vacancies_dict.update({language: response.json()})

        else:
            raise ValueError('response error!')
    return all_vacancies_dict

def get_all_vacancies_pages_dict(_id, _key, _language_list):
    count_vacancies_per_page = 100
    all_vacancies_pages_dict = {}
    try:
        all_vacancies_dict = connection_sj(_id, _key, _language_list)
        for language, all_vacancies_qty in all_vacancies_dict.items():
            if all_vacancies_qty <= count_vacancies_per_page:
                all_vacancies_pages_dict.update({language: 1})
            elif all_vacancies_qty > count_vacancies_per_page:
                all_vacancies_pages_dict.update({language: 1 + (all_vacancies_qty //
                                                                count_vacancies_per_page)})
        return all_vacancies_pages_dict
    except KeyError:
        return None


def get_vacancies_dict(_id, _key, all_vacancies_pages_dict):
    language_and_salary_list = []
    language_list = []
    try:
        for language, all_vacancies_qty in all_vacancies_pages_dict.items():
            language_list.append(language)
            for page_number in range(0, all_vacancies_qty):
                fetch = connection_sj(_id, _key, language_list,
                                      page_number=page_number,
                                      mode='get_stata')
                for language, vacancies in fetch.items():
                    for vacancy in vacancies['objects']:
                        language_and_salary_list.append(
                            [language, {'from': vacancy['payment_from'],
                                        'to': vacancy['payment_to'],
                                        'currency': vacancy['currency'],
                                        'gross': False}])
        language_and_salary_list = [[x[0], (predict_rub_salary(x[1]))] for x
                                    in language_and_salary_list]
        language_and_salary_list = [(x[0], setNone(x[1])) for x
                                    in language_and_salary_list]
        return language_and_salary_list
    except (KeyError, ValueError):
        return None


def make_sj_salary_statistics(_id, _key, _language_list):
    """Сollects statistics from superjob.ru and display the average salary."""
    pages_number_dict = get_all_vacancies_pages_dict(_id, _key,
                                                     _language_list)
    searched_vacancies = get_vacancies_dict(secret_id, secret_key,
                                            pages_number_dict)
    grupped_stat = group_salary_list(searched_vacancies)
    return make_salary_stat(grupped_stat)

if __name__ == '__main__':
    load_dotenv()
    secret_key = os.getenv("key")
    secret_id = os.getenv("id")
    advisable_languages = ['Java', 'PHP', 'С++', 'R', 'Python', 'JavaScript',
                           'Delphi', 'Go', '1C', 'Ruby']

    sj = make_sj_salary_statistics(secret_id, secret_key, advisable_languages)
    print_language_stat_ascitables('SuperJob Moscow', sj)



