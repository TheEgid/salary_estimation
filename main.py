"""Main."""
import os
import sys
from dotenv import load_dotenv
from fetch_sj import make_sj_salary_statistics
from fetch_hh import make_hh_salary_statistics
from stat_services import print_statistics_ascitables


def print_ascitables(sys_command, languages):
    hh = 'HeadHunter Moscow'
    sj = 'SuperJob Moscow'
    all_commands = [hh, sj]
    valid_commands = ['hh', 'sj', 'all']
    
    sys_command = sys_command.strip()
    print('Getting {} salary statistics for {} ...'.format(sys_command,
                                                           ', '.join(
                                                               languages)))
    if sys_command == valid_commands[0]:
        print_statistics_ascitables(hh,
                                    make_hh_salary_statistics(languages))
    elif sys_command == valid_commands[1]:
        print_statistics_ascitables(sj,
                                    make_sj_salary_statistics(secret_id,
                                                              secret_key,
                                                              languages))
    elif sys_command == valid_commands[2]:
        for command in all_commands:
            print_statistics_ascitables(command,
                                        make_hh_salary_statistics(languages))
    else:
        raise ValueError('Only valid commands: ' + ' '.join(valid_commands))


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.split(dir_path)[0])
    load_dotenv()
    secret_key = os.getenv("key")
    secret_id = os.getenv("id")
    advisable_languages = ['Java', 'PHP', 'С++', 'R', 'Python', 'JavaScript',
                           'Delphi', 'Go', '1C', 'Ruby']
    sys_command = sys.argv[1]
    print_ascitables(sys_command=sys_command, languages=advisable_languages)

