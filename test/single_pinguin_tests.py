import nose
import game
import sys
import test_sets
import pickle


WTF_R_U_DOING_STEP_LIMIT = 50000
SLOW_STEP_LIMIT = 5000
INTERMEDIATE_STEP_LIMIT = 1000
NORMAL_STEP_LIMIT = 500
FAST_STEP_LIMIT = 100

def check_global_ts(ts_name, time_limit, right_wins=True):
    ts = test_sets.GLOBAL_TEST_SET[ts_name]
    cfg = ts.to_strings()
    test_game = game.Game(cfg[0], cfg[1], cfg[2])

    counter = 0
    while counter < time_limit and not test_game.is_paused():
        counter += 1
        test_game.step()

    sys.stderr.write(ts_name + " step number : " + str(counter) + "; ")

    assert counter < time_limit, ts_name + ' : step limit exceeded'
    assert test_game.is_game_ended(False), ts_name + ' : game is not ended'
    assert not test_game.is_technical_issue(), ts_name + ' : game was killed due to technical error'
    if right_wins:
        assert test_game.get_score()[0] < test_game.get_score()[1], ts_name + ' : you are loose this game'
    else:
        assert test_game.get_score()[0] > test_game.get_score()[1], ts_name + ' : you are loose this game'


def test_simple_test():
    check_global_ts('simple_test', FAST_STEP_LIMIT)

def test_angle_test():
    check_global_ts('angle_test', FAST_STEP_LIMIT)

def test_small_angle_test():
    check_global_ts('small_angle_test', NORMAL_STEP_LIMIT)

def test_reverse_direction():
    check_global_ts('reverse_direction', INTERMEDIATE_STEP_LIMIT)

def test_angle_reverse():
    check_global_ts('angle_reverse_direction', INTERMEDIATE_STEP_LIMIT)

def test_reverse_gate():
    check_global_ts('reverse_gate', FAST_STEP_LIMIT, right_wins=False)

def test_reverse_gate_angle():
    check_global_ts('reverse_gate_angle', FAST_STEP_LIMIT, right_wins=False)

def test_complex_reverse_gate():
    check_global_ts('complex_reverse_gate', NORMAL_STEP_LIMIT, right_wins=False)

def test_goal_keeper():
    check_global_ts('goal_keeper', INTERMEDIATE_STEP_LIMIT)
