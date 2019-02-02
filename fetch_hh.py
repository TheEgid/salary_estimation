"""Get HH Stat."""
import requests
from stat_services import get_predict_salary
from stat_services import make_salary_statistics


def make_hh_salary_statistics(languages_list):
    hh_statistics_list = []
    for language in sorted(languages_list):
        hh_salaries_list = get_salaries_hh(language)
        hh_statistics_dict = make_salary_statistics(hh_salaries_list, language)
        hh_statistics_list.append(hh_statistics_dict)
    return hh_statistics_list


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
