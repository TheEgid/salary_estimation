"""Services Statistics."""
from __future__ import print_function
from itertools import groupby
from terminaltables import AsciiTable




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


def group_salary_list(input_salary_list):
    """Grouping."""
    grouped_languages_salary_list = []
    sorted_salary_list = sorted(input_salary_list, key=lambda x: x[0])
    for _language, _raw_salary in groupby(sorted_salary_list, lambda x: x[0]):
        grouped_languages_salary_list.append(list(_raw_salary))
    return grouped_languages_salary_list


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
    for languages_salary in input_salary_list:

        languages_salary_not_none_list = [x for x in languages_salary if x[1]
                                          is not None]
        if len(languages_salary_not_none_list) == 0:
            language_stat = {languages_salary[0][0]:
                                 {'vacancies_found': len(languages_salary),
                                  'vacancies_processed': 0,
                                  'average_salary': 'No Data'
                                  }
                             }
            salary_stat_dict.update(language_stat)
        else:
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


def print_statistics_ascitables(title, stat_dict):
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