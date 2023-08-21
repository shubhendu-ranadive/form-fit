import sys

from utils.pose_utils.pose import Pose
from utils.video_reader_utils import VideoReader

# 運動クラス
class Exercise():
    """ 運動クラスオブジェクトの初期設定 """
    def __init__(self) -> None:
        self.video_reader = VideoReader(0)
        self.exercise = Pose

    """ 運動判断関数 """
    def estimate_exercise(self):
        #pose_estimator = getattr(sys.modules[__name__], self.exercise)
        pose_estimator = Pose(self.video_reader)
        pose_estimator.estimate()
