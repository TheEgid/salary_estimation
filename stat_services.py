"""Services Statistics."""
from terminaltables import AsciiTable


def get_predict_salary(salary_dict, multiplier=2,
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
    predict_salary = 0
    if salary_dict is None:
        return None
    if salary_dict['currency'] not in ['RUR', 'rub']:
        return None
    try:
        if salary_dict['from'] is not None and salary_dict['to'] is not None:
            predict_salary = int(salary_dict['from'] + salary_dict['to'] // multiplier)
        elif salary_dict['to'] is not None:
            predict_salary = int(salary_dict['to'] * factor_top * multiplier)
        elif salary_dict['from'] is not None:
            predict_salary = int(salary_dict['from'] * factor_bottom * multiplier)
    except KeyError:
        return None
    if predict_salary == 0:
        return None
    else:
        return predict_salary


def make_salary_statistics(salary_list, language):
    salary_not_none_list = [x for x in salary_list if x is not None]
    if not salary_not_none_list:
        salary_statistics_dict = {'vacancies_found': len(salary_list),
                                  'vacancies_processed': 0,
                                  'average_salary': None,
                                  'language': language
                                  }
    else:
        salary_statistics_dict = {'vacancies_found': len(salary_list),
                                  'vacancies_processed': len(salary_not_none_list),
                                  'average_salary': sum(salary_not_none_list) //
                                                    len(salary_not_none_list),
                                  'language': language
                                  }
    return salary_statistics_dict


def print_table(table_data, title):
    top = ['Язык программирования', 'Найдено вакансий', 'Обработано',
           'Средняя зарплата']
    _table_data = []
    for data in table_data:
        _table_data.append([data['language'],
                            data['vacancies_found'],
                            data['vacancies_processed'],
                            data['average_salary']])
    _table_data.insert(0, top)
    table_instance = AsciiTable(_table_data, title)
    print(table_instance.table)