# Job Scheduling
Python application for solving Job Scheduling as a Constraint Satisfaction Problem

# Basic Usage
To run:
```
python3 job_scheduling.py [filename] [number_rooms] [--log LEVEL]
```

# File Format
The file should be a CSV with each line having start time and end time

For example, if job 1 starts at t=2 and ends at t=5 and job 2 starts at t=3 and ends at t=8 then the CSV would look like:
```
2,5
3,8
```

# Output
The program will try to solve the CSP in 2 different ways, once without backjumping,
and once with backjumping.

The result will be indicated for both, along with how long was required to find a solution

