
class Job:
    """
    Job class
    """
    def __init__(self, start_time, finish_time):
        """
        Create the object
        :param start_time: the start time
        :param finish_time: the finish time
        """
        self.start_time = start_time
        self.finish_time = finish_time


class JobSchedulingCSP:
    """
    A job scheduling CSP class
    """

    def __init__(self, jobs, number_rooms):
        """

        :param jobs: A 2D array of jobs with (start, finish)
        :param number_rooms: the number of rooms
        """
        # initialize local jobs
        self.jobs = []

        # for each job passed in
        for i,j in jobs:
            # create job object
            job = Job(i,j)
            # add job to jobs list
            self.jobs.append(job)
        # assign num rooms
        self.number_rooms = number_rooms

    def get_eft(self):
        """
        Find the job with the earliest finish time (eft)
        :return: the job with the earliest finish time (eft), or None if there is a tie
        """
        # the number of jobs with the earliest finish time
        num_satisfied_jobs = 0
        # the min eft
        min_eft_job = None
        # foreach job
        for job in self.jobs:
            # did we just assign the mineft job?
            just_assigned = False
            # if we haven't assigned the first time
            if min_eft_job is None:
                # assign and set just assigned to True
                min_eft_job = job
                just_assigned = True
            # if the finish time of this job is less - we have a new min
            if job.finish_time < min_eft_job.finish_time:
                # save this job as min
                min_eft_job = job
                # reset the number of satisfied jobs to 1
                num_satisfied_jobs = 1
            # if they are equal and we didnt just assign then we have a tie
            elif job.finish_time == min_eft_job.finish_time and not just_assigned:
                # add one
                num_satisfied_jobs += 1

        # if we have found a min,but more than one job has that min
        # then its a tie - so return None
        if num_satisfied_jobs != 1 or min_eft_job is None:
            return None

        # if we get here then there is a single job with the earliest finish time
        return min_eft_job




