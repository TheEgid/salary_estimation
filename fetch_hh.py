"""Get HH Stat."""
from __future__ import print_function
import requests
import pprint
from itertools import groupby
from terminaltables import AsciiTable


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
                new_vacancies.append({language: '{}&page={}'.format(_url,
                                                                 str(page_number))})
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
    for language, _url in url_dict.items():
        response = requests.get(_url)
        if response.ok:
            fetch = response.json()['items']
            for vacancy in fetch:
                language_and_salary_list.append((language,
                                        predict_rub_salary(vacancy['salary'])))
            return language_and_salary_list
        else:
            raise ValueError('response error!')


def predict_rub_salary(salary_dict, multiplier=2,
                       factor_top=0.4, factor_bottom=0.6):
    """
    Predict salary calculation. By default - ruble.

    Args:
        salary_dict (dict): The dictionary with a range of salaries.
        multiplier(int, optional): Equal to the number of salary bounds in the
            dictionary. Defaults to 2.
        factor_top(float, optional): The factor of the top salary bound.
            Defaults to 0.4
        factor_bottom(float, optional): The factor of the bottom salary bound.
            Defaults to 0.6
    Returns:
        predict_rub_salary(int)
    Raises:
        All exceptions returns None.
    Examples:
        IN: predict_rub_salary({'from': 100000, 'to': 120000,
                        'currency': 'RUR', 'gross': False}
        OUT: 110000
    """
    if salary_dict is None:
        return None
    elif (salary_dict['currency'] == 'RUR') or (salary_dict['currency'] == 'rub'):
        try:
            if (salary_dict['from'] is None) and (salary_dict['to'] is not None):
                return int(salary_dict['to']) * factor_top * multiplier
            elif (salary_dict['from'] is not None) and (salary_dict['to'] is None):
                return int(salary_dict['from']) * factor_bottom * multiplier
            elif (salary_dict['from'] is None) and (salary_dict['to'] is None):
                return None
            else:
                return (int(salary_dict['from']) + int(salary_dict['to'])) // multiplier
        except KeyError:
            return None
    else:
        return None
    
    
def make_salary_stat(input_salary_list):
    """
    Making salary statistics.

    Args:
        input_salary_list (list): Raw salary data list.
    Returns:
        salary_stat_dict(dict): Dictionary of dictionaries -
                {language name: {'vacancies_found': statistics,
                              'vacancies_processed': statistics,
                              'average_salary': statistics}}
    """
    salary_stat_dict = {}
    languages_salary_list = []
    sorted_salary_list = sorted(input_salary_list, key=lambda x: x[0])
    for _language, _raw_salary in groupby(sorted_salary_list, lambda x: x[0]):
        languages_salary_list.append(list(_raw_salary))
    for languages_salary in languages_salary_list:
        languages_salary_not_none_list = [x for x in languages_salary if x[1]
                                          is not None]
        languages_salary_not_none_mean = sum([(i[1]) for i in
                                              languages_salary_not_none_list]) // \
                                         len([(i[1]) for i in
                                              languages_salary_not_none_list])
        language_stat = {languages_salary_not_none_list[0][0]:
                             {'vacancies_found': len(languages_salary),
                              'vacancies_processed': len(languages_salary_not_none_list),
                              'average_salary': int(languages_salary_not_none_mean)
                              }
                         }
        salary_stat_dict.update(language_stat)
    return salary_stat_dict


def print_language_stat_ascitables(title, stat_dict):
    """
    Display the amount salary.

    Args:
        title(str): The title of ANCI table.
        stat_dict(dict): The body of ANCI table.
    """
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
    print(table_instance.table)


def make_headhunter_salary_statistics(_languages):
    """
    Сollects statistics from hh.ru website and display the average salary.

    Args:
        _languages(list): The list with names of programming language.
    """
    searched_vacancies = get_all_pages_vacancies_dict(_languages)
    all_vacancies = make_page_vacancy_url_list(searched_vacancies)
    temp_vacancy_language_list = [extract_language_and_salary(x) for
                                  x in all_vacancies]
    vacancy_language_list = (
    [vacancy for sublist in temp_vacancy_language_list for vacancy in sublist])
    
    return make_salary_stat(vacancy_language_list)


if __name__ == '__main__':
    advisable_languages = ['Java', 'PHP', 'С++', 'R', 'Python', 'JavaScript',
                           'Delphi', 'Go', '1C', 'Ruby']

    hh = make_headhunter_salary_statistics(advisable_languages)
    print_language_stat_ascitables('HeadHunter Moscow', hh)

