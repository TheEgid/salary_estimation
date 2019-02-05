"""Main."""
import argparse
import os
import sys
from dotenv import load_dotenv
from fetch_sj import get_salaries_sj
from fetch_hh import get_salaries_hh
from stat_services import print_table
from stat_services import make_salary_statistics


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', default="all", type=str,
                        help='valid commands only: hh, sj, all')
    return parser


def get_hh_statistics_list(languages_list):
    statistics_list = []
    for language in sorted(languages_list):
        salaries_list = get_salaries_hh(language)
        statistics_dict = make_salary_statistics(salaries_list, language)
        statistics_list.append(statistics_dict)
    return statistics_list


def get_sj_statistics_list(languages_list, id, key):
    statistics_list = []
    for language in sorted(languages_list):
        salaries_list = get_salaries_sj(language, id=id, key=key)
        statistics_dict = make_salary_statistics(salaries_list, language)
        statistics_list.append(statistics_dict)
    return statistics_list


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.split(dir_path)[0])
    load_dotenv()
    secret_key = os.getenv("key")
    secret_id = os.getenv("id")
    arg_parser = get_args_parser()
    args = arg_parser.parse_args()

    advisable_languages = ['Java', 'PHP', 'С++', 'R', 'Python', 'JavaScript',
                           'Delphi', 'Go', '1C', 'Ruby']

    if args.command == 'hh':
        hh_statistics_list = get_hh_statistics_list(advisable_languages)
        print_table(hh_statistics_list, 'HeadHunter Moscow')
    elif args.command == 'sj':
        sj_statistics_list = get_sj_statistics_list(advisable_languages,
                                                    id=secret_id,
                                                    key=secret_key)
        print_table(sj_statistics_list, 'SuperJob Moscow')
    elif args.command == 'all':
        hh_statistics_list = get_hh_statistics_list(advisable_languages)
        print_table(hh_statistics_list, 'HeadHunter Moscow')
        sj_statistics_list = get_sj_statistics_list(advisable_languages,
                                                    id=secret_id,
                                                    key=secret_key)
        print_table(sj_statistics_list, 'SuperJob Moscow')
    else:
        exit('Error: Bad argument')


if __name__ == '__main__':
    main()
