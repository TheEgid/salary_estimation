"""Get HH Stat."""
import requests
from stat_services import get_predict_salary
from itertools import count


def get_salaries_hh(language, region=1, period=30):
    limit_hh_pages = 99
    vacancies_list = []
    _url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'Программист {}'.format(language),
        'area': region,
        'from': 'cluster_area',
        'period': period
    }
    for page_number in count(start=0):
        params.update({'page': page_number})
        response = requests.get(_url, params=params)
        if response.ok:
            allpages = response.json()['pages']
            for vacancy in response.json()['items']:
                     vacancies_list.append(get_predict_salary(vacancy['salary']))
            if page_number >= allpages or page_number == limit_hh_pages:
                break
        else:
             raise ValueError('response hh error!')
    return vacancies_list
