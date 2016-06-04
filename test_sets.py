import copy

test_file_name = "pattern"
test_logic_name = "YourLogic"

class Team:
    def __init__(self, file, team):
        self._file = file
        self._team = team

    @staticmethod
    def _team_to_str(team):
        res = ""
        for p in team:
            res += '<player x="' + p[0] + \
                   '" y="' + p[1] + \
                   '" r="30" name="Penguin" logic="' + p[2] + '"/>'
        return res

    def to_string(self):
        return """
        <config>
            <file_name>""" + self._file + """</file_name>
            <players>""" + self._team_to_str(self._team) + """
            </players>
        </config>
        """

class TestSet:
    def __init__(self, ball, t1, t2):
        self._t1 = t1
        self._t2 = t2
        self._ball = ball


    def to_strings(self):
        gc = """<config><board left="110" right="1072" top="45" bottom="680"/>
             <gate top="283" bottom="415"/>
             <player_deviation>0</player_deviation>
             <max_score left="1" right="1"/>
              <balls>
                   <ball x=\"""" + self._ball[0] + """\"
                         y=\"""" + self._ball[1] + """\"
                         r="10"/>
              </balls>
        </config>"""

        return (gc, self._t1.to_string(), self._t2.to_string())


GLOBAL_TEST_SET = {
    "simple_test":
        TestSet(ball=('591', '363'),
                t1=Team('sample_logics', []),
                t2=Team(test_file_name, [('700', '363', test_logic_name)])),
    "reverse_gate":
        TestSet(ball=('591', '363'),
                t1=Team(test_file_name, [('450', '363', test_logic_name)]),
                t2=Team('sample_logics', [])),
    "angle_test":
        TestSet(ball=('591', '363'),
                t1=Team('sample_logics', []),
                t2=Team(test_file_name, [('832', '524', test_logic_name)])),
    "reverse_gate_angle":
        TestSet(ball=('591', '363'),
                t1=Team(test_file_name, [('450', '524', test_logic_name)]),
                t2=Team('sample_logics', [])),
    "small_angle_test":
        TestSet(ball=('400', '363'),
                t1=Team('sample_logics', []),
                t2=Team(test_file_name, [('460', '524', test_logic_name)])),
    "reverse_direction":
        TestSet(ball=('591', '363'),
                t1=Team('sample_logics', []),
                t2=Team(test_file_name, [('450', '363', test_logic_name)])),
    "angle_reverse_direction":
        TestSet(ball=('591', '363'),
                t1=Team('sample_logics', []),
                t2=Team(test_file_name, [('450', '524', test_logic_name)])),
    "complex_reverse_gate":
        TestSet(ball=('591', '363'),
                t1=Team(test_file_name, [('700', '363', test_logic_name)]),
                t2=Team('sample_logics', [])),
    "goal_keeper":
        TestSet(ball=('591', '363'),
                t1=Team('sample_logics', [('300', '363', 'StayLeftLogic')]),
                t2=Team(test_file_name, [('700', '363', test_logic_name)]))
    }