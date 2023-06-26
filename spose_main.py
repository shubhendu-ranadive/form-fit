# アプリを実施するためのメインPythonファイル
from utils.exercise_utils import Exercise

if __name__ == '__main__':

    # 運動を判断するための関数
    pose = Exercise()
    pose.estimate_exercise()
