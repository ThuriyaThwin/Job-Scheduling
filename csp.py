import copy
import logging

class Job:
    """
    Job class
    """
    def __init__(self, start_time, finish_time, domain_size):
        """
        Create the object
        :param start_time: the start time
        :param finish_time: the finish time
        :param domain_size: the size of the domain
        """
        self.start_time = start_time
        self.finish_time = finish_time
        self.domain = []
        for i in range(domain_size):
            self.domain.append(i)
        self.assigned = False
        self.room = None

    def __eq__(self, other):
        """
        Define equality
        :param other: the other job
        :return: True if equal, else false
        """

        # if everything is the same
        if self.start_time == other.start_time and self.finish_time == other.finish_time and self.domain == other.domain \
            and self.assigned == other.assigned and self.room == other.room:
                return True
        # if something is different
        return False


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
            job = Job(int(i),int(j), int(number_rooms))
            # add job to jobs list
            self.jobs.append(job)
        # assign num rooms
        self.number_rooms = int(number_rooms)

    def get_eft(self):
        """
        Find the job with the earliest finish time (eft)
        :return: the job with the earliest finish time (eft), or None if there is a tie
        """

        # all jobs that have the eft
        jobs = []
        # the eft
        eft = -1
        # foreach job
        for job in self.jobs:
            if job.assigned == False:
                # if the finish time is less than current min
                if job.finish_time < eft:
                    # reset jobs
                    jobs = [job]
                    #set the eft
                    eft = job.finish_time
                # if they are equal and we didnt just assign then we have a tie
                elif job.finish_time == eft:
                    jobs.append(job)

        # if we have found a min,but more than one job has that min
        # then its a tie - so return None
        if len(jobs) != 1:
            return None

        # if we get here then there is a single job with the earliest finish time
        min_eft_job = jobs[0]
        return min_eft_job

    def find_solution(self, use_backjumping=False):
        """
        Find a solution to the given CSP if possible
        :return: True if solution found, else fase
        """

        # while not in goal state

        try:
            while not self.in_goal_state():
                # get the job to assign
                job_to_assign = self.get_job_to_assign()
                logging.debug("Assigning job: ({},{})".format(job_to_assign.start_time, job_to_assign.finish_time))
                # assign a value
                self.jobs = self.assign(job_to_assign)
                #check constraint
                self.ac3()

                # check for backjump
                if use_backjumping:
                    self.backjump()

        except Exception as err:
            logging.critical(err)
            return False

        return True

    def backjump(self):
        """
        Backjump

        The idea is to get to a new part of the search space
        by changing assignments so that future assignments are
        more efficient due to being in a new part of the search space
        """
        pass

    def find_backjumping_solution(self):
        """
        Find a solution usign backjumping
        :return: True if solution found, else false
        """
        return self.find_solution(use_backjumping=True)

    def ac3(self):
        """
        Perform ac3 consistency checking
        """
        logging.info("Running AC-3...")
        # for each job
        for job in self.jobs:
            #  if this job has been assigned
            if job.assigned:
                # look at every other job
                for j in self.jobs:
                    # if jobs overlap
                    if j.start_time in range(job.start_time, job.finish_time) or j.finish_time in range(job.start_time, job.finish_time) and job != j:
                        # remove room from domain of the job
                        logging.debug("Removing {} from domian of job ({}, {}) with domain {}".format(job.room, j.start_time, j.finish_time, j.domain))
                        try:
                            j.domain.remove(job.room)
                        except Exception:
                            logging.debug("Room already removed from domain")


    def assign(self, job):
        """
        Assign a value to the job
        :param job: The job to assign a value
        :return: the new set of jobs with this assignment
        """
        # make sure it is eligible for assignemnt
        if job.assigned == True:
            raise Exception("Cannot assign job. Job is already assigned!")

        # get index
        index = self.job_to_index(job)
        # if we have an invalid job
        if index is None:
            raise Exception("Cannot assign job. Job does not exist!")

        # get the other jobs
        other_jobs = copy.deepcopy(self.jobs)
        # delete the job being discussed
        del other_jobs[index]

        # dependencies between each other
        room_dependencies = []
        for i in range(self.number_rooms):
            room_dependencies.append(0)

        # each room
        for i in range(self.number_rooms):
            # each job that isn't the one being assigned
            for j in other_jobs:
                # if this room in the domain of the job
                if i in j.domain:
                    # add 1 to the dependency
                    room_dependencies[i] += 1

        logging.debug("Room dependencies: {}".format(room_dependencies))

        # assign the job to the room with the least dependencies in the domain of the job
        possible_assignments = []
        # for every room with dependencies
        for room, num_dependencies in enumerate(room_dependencies):
            # if the room is in the job's domain
            if room in job.domain:
                # record the room number and the num dependencies
                record = {
                    "room": room,
                    "dependencies": num_dependencies
                }
                # add to possible dependencies
                possible_assignments.append(record)

        # go through possible assignments, and make the one with the least number of dependencies
        min_dep = possible_assignments[0]["dependencies"]
        room = possible_assignments[0]["room"]
        # for every assignment
        for a in possible_assignments:
            # if this is the least dependencies
            if a["dependencies"] < min_dep:
                # set room
                room = a["room"]
                # set min dep
                min_dep = a["dependencies"]

        # make assignment
        job.assigned = True
        job.room = room
        logging.debug("Assigning to room {}".format(room))

        # get the new jobs
        new_jobs = other_jobs
        # add the newly assigned
        new_jobs.append(job)

        # assign the new jobs
        return new_jobs

    def job_to_index(self, job):
        """
        Get which index job
        :param job: The job
        :return: the index
        """

        # for each job
        for i, j in enumerate(self.jobs):
            # if the st, ft, and assigned are the same - return it
            if j.start_time == job.start_time and j.finish_time == job.finish_time and j.assigned == job.assigned:
                # return the index
                logging.debug("Found job at index {}".format(i))
                return i

        logging.debug("Could not find job index")
        return None

    def get_job_to_assign(self):
        """
        Return the job to assign
        :return: the job to assign
        """

        # first try mrv
        job = self.get_mrv()
        # now try eft
        if job is None:
            job = self.get_eft()
        #now just grab a job that isn't assigned
        if job is None:
            #for each job
            for j in self.jobs:
                # if not assigned
                if j.assigned == False:
                    # assign this job
                    job = j
                    break
        # not possible - but still check
        if job is None and not self.in_goal_state():
            raise Exception("Invalid Configuration!\nNo valid jobs and not in goal state")


        return job

    def get_mrv(self):
        """
        Get the minimum remaining values job
        :return: The job with the minimum remaining jobs, or None if tie
        """

        # the jobs with mrv
        jobs = []

        # the num of possible values that the min has
        num_values = -1

        # for each job
        for j in self.jobs:
            #make sure this job can be selected
            if j.assigned == False:
                # if its less than, then we have a new min
                if len(j.domain) < num_values:
                    jobs = [j]
                    num_values = len(j.domain)
                # if its equal, then we have a tie
                elif len(j.domain) == num_values:
                    jobs.append(j)
        # make sure there is exactly 1 mrv job
        if len(jobs) != 1:
            return None

        #return the mrv job
        job = jobs[0]
        return job

    def in_goal_state(self):
        """
        Check if CSP is in goal state
        :return: True if in goal state,else false
        """

        #iterate through jobs
        for j in self.jobs:
            # if we find an unassigned job, then are not in goal state
            if j.assigned is False:
                logging.debug("Found unassigned job!")
                return False

        # we have gotten through all jobs, and all are assigned
        # we are in goal state
        logging.info("In Goal State!")
        return True




