"""Get SJ Stat."""
import requests
from stat_services import get_predict_salary


def get_salaries_sj(language, id, key, region='Москва'):
    vacancies_list = []
    count_vacancies_per_page = 100
    category_is_programming = 48
    _url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'count': count_vacancies_per_page,
        'archive': False,
        'keyword': 'Программист {}'.format(language),
        'not_archive': True,
        'town': region,
        'catalogues': category_is_programming
    }
    headers = {'X-Api-App-Id': key,
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'api.superjob.ru',
               'Client Id': id
               }
    response = requests.get(_url, headers=headers, params=params)
    if response.ok:
        pages_qty = (response.json()['total'] // count_vacancies_per_page) + 1
    else:
        raise ValueError('response sj error!')

    for page_number in range(pages_qty):
        params.update({'page': page_number})
        response = requests.get(_url, headers=headers, params=params)
        if response.ok:
            vacancies = response.json()['objects']
            for vacancy in vacancies:
                vacancies_list.append({'from': vacancy['payment_from'],
                                       'to': vacancy['payment_to'],
                                       'currency': vacancy['currency'],
                                       'gross': False})
        else:
            raise ValueError('response sj error!')
    vacancies_list = [get_predict_salary(x) for x in vacancies_list]
    return vacancies_list
