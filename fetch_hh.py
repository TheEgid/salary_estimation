"""Get HH Stat."""
from __future__ import print_function
import requests
import urllib.parse
from stat_services import predict_rub_salary
from stat_services import make_salary_stat
from stat_services import group_list


class VacanciesDictionaryError(Exception):
    """Declare special exception."""
    pass


def get_all_pages_vacancies_dict(language_list, search_period=30):
    """
    Get dictionaries with vacancies of programmers from Web API HeadHunter.ru.

    Args:
        language_list(list): The list with names of programming language.
        search_period(int, optional): Over these last days search. Defaults to 30.
    Returns:
        all_pages_vacancies_dict(dict): Dictionary key is name of programming language.
            Dictionary value contains list (2 elements). First element is first page url with 
            search results vacancies for particular programming language. Second element is 
            number of all pages (urls with search results).         
    Raises:
        ValueError: Raises an exception.
    """
    _url = 'https://api.hh.ru/vacancies'
    all_pages_vacancies_dict = {}
    language_list.sort()
    for language in language_list:
        params = {
            'text': 'Программист {}'.format(language),
            'area': 1,
            'from': 'cluster_area',
            'period': search_period
        }
        response = requests.get(_url, params=params)
        if response.ok:
            all_pages_vacancies_dict.update({language: [response.url, response.json()['pages']]})
        else:
            raise ValueError('response error!')
    return all_pages_vacancies_dict


def make_page_vacancy_url_list(all_pages_vacancies_dict):
    """
    Get all pages with search results vacancies for particular programming language.

    Args:
        all_pages_vacancies_dict(dict): Dictionary key is name of programming
        language. Dictionary value contains list (2 elements). First element is
        first page url with search results vacancies for particular programming
        language. Second element is number of all pages (urls with search results).
    Returns:
        new_vacancies(list): The list of dictionares with all pages url with 
            search results vacancies for particular programming language
    Raises:
        VacanciesDictionaryError: Raises an exception KeyError, ValueError.
    """
    new_vacancies = []
    try:
        for language, [_url, _pages_qty] in all_pages_vacancies_dict.items():
            for page_number in range(0, _pages_qty):
                query = urllib.parse.urlparse(_url).query
                url_params = dict(urllib.parse.parse_qsl(query))
                url_params.update({'page': page_number})
                url = _url[:_url.find("?")]
                new_vacancies.append({language: (url, url_params)})
        return new_vacancies
    except (KeyError, ValueError):
        raise VacanciesDictionaryError


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
    """Сollects statistics from hh.ru and display the average salary."""
    searched_vacancies = get_all_pages_vacancies_dict(language_list)
    all_vacancies_urls = make_page_vacancy_url_list(searched_vacancies)
    temp_vacancy_language_list = \
        [extract_language_and_salary(x) for x in all_vacancies_urls]
    vacancy_language_list = \
        group_list([vacancy for sublist in temp_vacancy_language_list
                           for vacancy in sublist])
    return make_salary_stat(vacancy_language_list)

