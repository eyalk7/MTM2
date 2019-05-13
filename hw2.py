import Techniovision

"""************************************** FUNCTIONS **********************************"""


def inside_contest(faculty, file_name):
    """
    Calculates the most voted study program in given faculty
    based on the commands in the file
    :param faculty: Name of the faculty
    :param file_name: Filename of file with commands
    :return: The name of the most voted study program
    """

    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()

    # iterate on the file's lines, find a line with "staff choise" and the given faculty.
    # get_programs() transform the line to a dictionary with the faculty's /
    # programs as keys and num of points as data
    programs = {}
    for line in lines:
        if "staff choice" in line and faculty in line:
            programs = get_programs(line)
            # break is not needed under the assumption there's only one staff choice for the faculty

    # iterate again on the file's line, find lines with "inside contest" and the given faculty
    # update the 'programs' points dictionary with the students votes
    # each student votes ones
    voters = []     # IDs of students who voted already
    for line in lines:
        if "inside contest" in line and faculty in line:
            words = line.split()
            # words = ['inside', 'contest', <student id>, <program>, <faculty>]
            student_id = words[2]
            if student_id not in voters:    # check the student hasn't voted already
                voters.append(student_id)
                program = words[3]
                programs[program] += 1      # add a vote = 1 point

    return get_max_program(programs)   # return program with max points


def get_programs(line):
    """
    Initialize this faculty's programs list
    Assumptions:
    1) only one staff choice line per faculty
    2) there are spaces ONLY between parameters (and in "staff choice")

    :param line: a string representing a line in the given text file
    :return: A dictionary that maps each program to its amount of points
    """
    words = line.split()
    # words = ['staff', 'choice', <program 1>, ..., <program n>, <faculty>]

    # first faculty starts with 20 points (staff's choice)
    programs = {words[2]: 20}
    for i in range(3, len(words) - 1):
        programs[words[i]] = 0  # all the rest are initialized to 0
    return programs


def get_max_program(dict):
    """
    Get the study program that will represent the faculty
    :param dict: The dictionary that maps each program  in the faculty
                 to its amount of points
    :return: The name of the study program with the highest amount of points
    """

    # find max value in the points dictionary and return it's key (name of program)
    program_points = list(dict.values())
    max_points = max(program_points)
    max_index = program_points.index(max_points)

    return list(dict.keys())[max_index]


"""************************************** PROGRAM **********************************"""
# create new Techniovision
t = Techniovision.TechniovisionCreate()

# get the lines from the given input file
file_name = "input.txt"
file = open(file_name, 'r')
lines = file.readlines()
file.close()

# iterate on the file's lines. for each line with "staff choise" /
# get faculty's chosen program with inside_contest() /
# save in 'faculties' dictionary with the chosen programs  /
# as keys and faculties names as data
faculties = {}
for line in lines:
    if "staff choice" in line:
        words = line.split()
        faculty = words[len(words) - 1]
        program = inside_contest(faculty, file_name)
        faculties[program] = faculty

# iterate again on the file's lines. for each line with "techniovision" /
# update the Techniovision votes count with the outside functions.
for line in lines:
    if "techniovision" in line:
        words = line.split()
        # words = ["techniovision", <student_id>, <study_program>, <student_faculty>]

        student_id = words[1]
        study_program = words[2]
        student_faculty = words[3]

        # if the student voted a program that doesn't represent a faculty
        # his vote doesn't count
        if study_program in faculties.keys():
            voting_faculty = faculties[study_program]
            Techniovision.TechniovisionStudentVotes(t, int(student_id),
                                                    str(student_faculty),
                                                    str(voting_faculty))

# print the winning faculty and deallocate the Techniovision object
Techniovision.TechniovisionWinningFaculty(t)
Techniovision.TechniovisionDestroy(t)

"""************************************** END OF FILE **********************************"""
