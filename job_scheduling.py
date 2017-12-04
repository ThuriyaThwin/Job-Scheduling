import csp
import argparse
import logging

def set_log_level(level):
    logging.basicConfig(level={
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }.get(level, logging.WARNING))  # should-be-impossible-super-duper-fallback
    return level


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("csp_file", help="File detailing the CSP to solve (see README for format)")
    parser.add_argument('--log', type=set_log_level, default='WARNING', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help="Logging level")
    args = parser.parse_args()

def setup():
    parse_command_line_arguments()

def run():
    pass

if __name__ == "__main__":
    setup()
    run()