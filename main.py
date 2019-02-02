"""Main."""
import argparse
import os
import sys
from dotenv import load_dotenv
from fetch_sj import make_sj_salary_statistics
from fetch_hh import make_hh_salary_statistics
from stat_services import print_table


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', default="all", type=str,
                        help='valid commands only: hh, sj, all')
    return parser


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
        hh_statistics_list = make_hh_salary_statistics(advisable_languages)
        print_table(hh_statistics_list, 'HeadHunter Moscow')
    elif args.command == 'sj':
        sj_statistics_list = make_sj_salary_statistics(advisable_languages,
                                                       id=secret_id,
                                                       key=secret_key)
        print_table(sj_statistics_list, 'SuperJob Moscow')
    elif args.command == 'all':
        hh_statistics_list = make_hh_salary_statistics(advisable_languages)
        print_table(hh_statistics_list, 'HeadHunter Moscow')
        sj_statistics_list = make_sj_salary_statistics(advisable_languages,
                                                       id=secret_id,
                                                       key=secret_key)
        print_table(sj_statistics_list, 'SuperJob Moscow')
    else:
        exit('Error: Bad argument')


if __name__ == '__main__':
    main()
