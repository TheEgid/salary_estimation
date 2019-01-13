"""Main."""
import os
import sys
from dotenv import load_dotenv
from fetch_sj import make_sj_salary_statistics
from fetch_hh import make_hh_salary_statistics
from stat_services import print_statistics_ascitables


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.split(dir_path)[0])
    load_dotenv()
    secret_key = os.getenv("key")
    secret_id = os.getenv("id")
    advisable_languages = ['Java', 'PHP', 'С++', 'R', 'Python', 'JavaScript',
                           'Delphi', 'Go', '1C', 'Ruby']
    sys_command = ''.join(sys.argv[1])

    print('Getting {} salary statistics for {} ...'.format(
        sys_command, ', '.join(advisable_languages)))

    if sys_command.strip() == 'hh':
        print_statistics_ascitables('HeadHunter Moscow',
                                make_hh_salary_statistics(advisable_languages))
    elif sys_command.strip() == 'sj':
        print_statistics_ascitables('SuperJob Moscow',
                                make_sj_salary_statistics(secret_id, secret_key,
                                        advisable_languages))
    elif sys_command.strip() == 'all':
        print_statistics_ascitables('HeadHunter Moscow',
                                make_hh_salary_statistics(advisable_languages))
        print_statistics_ascitables('SuperJob Moscow',
                                make_sj_salary_statistics(secret_id, secret_key,
                                        advisable_languages))
    else:
        raise ValueError('no command')