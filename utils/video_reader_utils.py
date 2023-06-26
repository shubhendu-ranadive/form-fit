import cv2

# 動画やカメラのフレームを読込などのクラス
class VideoReader:
    """ 初期設定 """
    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        self._total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._current_frame = 0

    def read_frame(self):
        """ １つずつフレームを読み込む """
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret is False or frame is None:
                return None
            self._current_frame += 1
        else:
            return None
        return frame

    def read_n_frames(self, num_frames=1):
        """ nフレームを読み込む """
        frames_list = []
        for _ in range(num_frames):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret is False or frame is None:
                    return None
                frames_list.append(frame)
                self._current_frame += 1
            else:
                return None
        return frames_list

    def is_opened(self):
        """ 動画やカメラのフレームを読み込んでいるか確認 """
        return self.cap.isOpened()

    def get_frame_width(self):
        """ フレームの幅を習得 """
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_frame_height(self):
        """ フレームの高を習得 """
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_video_fps(self):
        """ 動画やカメラのFPSを取得 """
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get_current_frame(self):
        """ 動画の現在のフレームを取得 """
        return self._current_frame

    def get_total_frames(self):
        """ 動画のフレームの数を取得 """
        return self._total_frames

    def release(self):
        """ 動画やカメラを終了する """
        self.cap.release()

    def __del__(self):
        self.release()
