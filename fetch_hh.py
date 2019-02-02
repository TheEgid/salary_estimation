"""Get HH Stat."""
import requests
from stat_services import get_predict_salary


def get_salaries_hh(language, region=1, period=30):
    vacancies_list = []
    _url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'Программист {}'.format(language),
        'area': region,
        'from': 'cluster_area',
        'period': period
    }
    response = requests.get(_url, params=params)
    if response.ok:
        pages_qty = response.json()['pages']
    else:
        raise ValueError('response hh error!')
    for page_number in range(pages_qty):
        params.update({'page': page_number})
        response = requests.get(_url, params=params)
        if response.ok:
            for vacancy in response.json()['items']:
                vacancies_list.append(get_predict_salary(vacancy['salary']))
        else:
            raise ValueError('response hh error!')
    return vacancies_list
