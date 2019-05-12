import Techniovision


def inside_contest(faculty, file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()

    programs = {}
    for line in lines:
        if "staff choice" in line and faculty in line:
            programs = get_programs(line)
            # break is not needed under the assumption there's only one staff choice for the faculty

    voters = []     # IDs of students who voted already
    for line in lines:
        if "inside contest" in line:
            words = line.split()
            # words = ['inside', 'contest', <student id>, <program>, <faculty>]
            student_id = words[2]
            if student_id not in voters:    # check the student hasn't voted already
                voters.append(student_id)
                program = words[3]
                programs[program] += 1      # add a vote = 1 point

    return get_max_key(programs)   # return program with max points

def get_programs(line):
    """
    Initialize this faculty's programs list
    Assumptions:
    1) only one staff choice line per faculty
    2) there are spaces ONLY between parameters (and in "staff choice")
    :param line: a string representing a line in the given text file
    :return: A dictionary that maps each program to the amount of points it has
    """
    words = line.split()
    # words = ['staff', 'choice', <program 1>, ..., <program n>, <faculty>]

    # first faculty starts with 20 points (staff's choice)
    programs = {words[2]: 20}
    for i in range(3, len(words) - 1):
        programs[words[i]] = 0  # all the rest are initialized to 0
    return programs


def get_max_key(dict):
    """

    :param dict:
    :return:
    """
    program_points = list(dict.values())
    max_points = max(program_points)
    max_index = program_points.index(max_points)

    return list(dict.keys)[max_index]


t = Techniovision.TechniovisionCreate()

file_name = "input.txt"
file = open(file_name, 'r')
lines = file.readlines()
file.close()

faculties = {}
for line in lines:
    if "staff choice" in line:
        words = line.split()
        faculty = words[len(words) - 1]
        program = inside_contest(faculty, file_name)
        faculties[program] = faculty

for line in lines:
    if "techniovision" in line:
        words = line.split()
        # words = ["techniovision", <student_id>, <study_program>, <student_faculty>]

        student_id = words[1]
        study_program = words[2]
        student_faculty = words[3]

        voting_faculty = faculties[study_program]

        Techniovision.TechniovisionStudentVotes(t, int(student_id),
                                                str(student_faculty),
                                                str(voting_faculty))

Techniovision.TechniovisionWinningFaculty(t)

Techniovision.TechniovisionDestroy(t)


