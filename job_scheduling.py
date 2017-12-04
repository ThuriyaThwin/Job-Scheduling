import csp
import argparse
import logging
import numpy

def set_log_level(level):
    """
    Set the logging level
    :param level: The level at which to log
    :return: the now set logging level
    """

    #set the logging level
    logging.basicConfig(level={
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }.get(level, logging.WARNING))  # should-be-impossible-super-duper-fallback
    return level


def parse_command_line_arguments():
    """
    Parse the command line arguments
    :return: dict of command line args
    """

    # create the arg parser
    parser = argparse.ArgumentParser()
    # the filenmae
    parser.add_argument("csp_file", help="File detailing the CSP to solve (see README for format)")
    # the number rooms to house the jobs
    parser.add_argument("number_rooms", help="The number of rooms in which to schedule the jobs")
    # the logging level
    parser.add_argument('--log', type=set_log_level, default='WARNING', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help="Logging level")
    # parse them
    args = parser.parse_args()

    return args

def setup():

    # get command args
    args = parse_command_line_arguments()
    # take values out of args dict into variables
    filename = args.csp_file
    number_rooms = args.number_rooms

    #try to read in the file
    jobs = None
    csp = None
    try:
        jobs = numpy.loadtxt(filename, delimiter=",")
        logging.debug(jobs)
    except Exception as err:
        logging.critical("Invalid File!")
        logging.debug(err)
        exit(1)

    return csp, jobs

def run():
    pass

if __name__ == "__main__":
    csp, jobs = setup()
    run()