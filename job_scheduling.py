from csp import JobSchedulingCSP
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
    }.get(level, logging.WARNING),
                        filename="csp.log")  # should-be-impossible-super-duper-fallback
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
    """
    Parse command line arguments and return the things needed for CSP
    :return: jobs: 2D array
             number_rooms: the number of rooms for the jobs
    """

    # get command args
    args = parse_command_line_arguments()
    # take values out of args dict into variables
    filename = args.csp_file
    number_rooms = int(args.number_rooms)

    #try to read in the file
    jobs = None
    try:
        # read the file
        jobs = numpy.loadtxt(filename, delimiter=",")
        logging.debug(jobs)
    except Exception as err:
        # log and exit
        logging.critical("Invalid File!")
        logging.debug(err)
        exit(1)

    return jobs, number_rooms

def run(jobs, number_rooms):
    """
    Run the algorithm until completion
    :param jobs: 2D array for the jobs with (start, finish)
    :param number_rooms: the number of rooms
    :return: the assignments or None if not possible
    """

    # create CSP
    csp = JobSchedulingCSP(jobs, number_rooms)
    #try to find a solution
    solution_found = csp.find_solution()

    # if we found a solution
    if solution_found:
        print("Solution Found!")
        # print the assignments
        for job in csp.jobs:
            print("({}, {}) assigned to Room: {}".format(job.start_time, job.finish_time, job.room))
    else:
        # print the error
        print("No Solution Found!\nYou can check csp.log to see if an error occurred.")


if __name__ == "__main__":
    jobs, number_rooms = setup()
    run(jobs, number_rooms)