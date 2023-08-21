from ultralytics import YOLO
import cv2

from utils.operation_utils import Operation
from utils.drawing_utils import Draw
from utils.pose_utils.const import POSE, VISIBILITY_THRESHOLD

pose = YOLO('yolov8n-pose.pt')

# 骨格検出クラス
class Pose():
    """ 初期設定 """
    def __init__(self, video_reader) -> None:
        self.video_reader = video_reader
        self.operation = Operation()
        self.squat_counter = self.pushup_counter = self.armcurl_counter = 0
        self.key_points = self.prev_pose = self.current_pose = None
        self.ang1_tracker = []
        self.ang4_tracker = []
        self.pose_tracker = []
        self.armcurl_tracker = []
        self.headpoint_tracker = []
        self.width = int(self.video_reader.get_frame_width())
        self.height = int(self.video_reader.get_frame_height())
        self.video_fps = self.video_reader.get_video_fps()
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.draw = Draw(self.width, self.height)

    def get_keypoints(self, image, pose_result):
        """ キーポイント取得関数 """
        key_points = {}
        for idx, landmark in enumerate(pose_result[0].keypoints.data[0].cpu().numpy().tolist()):
            if (landmark[2] < VISIBILITY_THRESHOLD):
                continue
            if landmark:
                key_points[idx] = landmark[:2]
        return key_points

    def is_point_in_keypoints(self, str_point):
        """ ポイントがキーポイントかを確認関数 """
        return POSE[str_point] in self.key_points

    def get_point(self, str_point):
        """ キーポイントから点を取ってくる """
        return self.key_points[POSE[str_point]] if self.is_point_in_keypoints(str_point) else None

    def get_available_point(self, points):
        """ 優先度高いポイントからキーポイントを取得する """
        available_point = None
        for point in points:
            if self.is_point_in_keypoints(point) and available_point is None:
                available_point = self.get_point(point)
                break
        return available_point

    def two_line_angle(self, str_point1, str_point2, str_point3):
        """ 2つの線の間の角度する """
        coord1 = self.get_point(str_point1)
        coord2 = self.get_point(str_point2)
        coord3 = self.get_point(str_point3)
        return self.operation.angle(coord1, coord2, coord3)

    def one_line_angle(self, str_point1, str_point2):
        """ 地面から線の角度 """
        coord1 = self.get_point(str_point1)
        coord2 = self.get_point(str_point2)
        return self.operation.angle_of_singleline(coord1, coord2)

    def predict_pose(self):
        """ 骨格予測するための関数 """
        ang1 = ang2 = ang3 = ang4 = ang5 = ang6 = ang7 = None
        is_squat = is_pushup = is_armcurl = False
        diff_head_hand_y = None

        # shoulder-elbow-wristの間の角度計算
        if self.is_point_in_keypoints("left_shoulder") and \
            self.is_point_in_keypoints("left_elbow") and \
            self.is_point_in_keypoints("left_wrist") and \
            self.is_point_in_keypoints("right_shoulder") and \
            self.is_point_in_keypoints("right_elbow") and \
            self.is_point_in_keypoints("right_wrist"):
            ang1 = self.two_line_angle("left_shoulder", "left_elbow", "left_wrist")
            ang7 = self.two_line_angle("right_shoulder", "right_elbow", "right_wrist")
        elif self.is_point_in_keypoints("left_shoulder") and \
            self.is_point_in_keypoints("left_elbow") and \
            self.is_point_in_keypoints("left_wrist"):
            ang1 = self.two_line_angle("left_shoulder", "left_elbow", "left_wrist")
        elif self.is_point_in_keypoints("right_shoulder") and \
            self.is_point_in_keypoints("right_elbow") and \
            self.is_point_in_keypoints("right_wrist"):
            ang1 = self.two_line_angle("right_shoulder", "right_elbow", "right_wrist")

        # shoulder-hip-ankleの間の角度計算
        if self.is_point_in_keypoints("left_shoulder") and \
            self.is_point_in_keypoints("left_hip") and \
            self.is_point_in_keypoints("left_ankle"):
            ang2 = self.two_line_angle("left_shoulder", "left_hip", "left_ankle")
        elif self.is_point_in_keypoints("right_shoulder") and \
            self.is_point_in_keypoints("right_hip") and \
            self.is_point_in_keypoints("right_ankle"):
            ang2 = self.two_line_angle("right_shoulder", "right_hip", "right_ankle")
        else:
            pass

        # shoulder-ankle と hip-ankleの地面から角度計算
        left_shoulder_ankle = self.is_point_in_keypoints("left_shoulder") and self.is_point_in_keypoints("left_ankle")
        right_shoulder_ankle = self.is_point_in_keypoints("right_shoulder") and self.is_point_in_keypoints("right_ankle")
        left_hip_ankle = self.is_point_in_keypoints("left_hip") and self.is_point_in_keypoints("left_ankle")
        right_hip_ankle = self.is_point_in_keypoints("right_hip") and self.is_point_in_keypoints("right_ankle")
        left_shoulder_hip = self.is_point_in_keypoints("left_shoulder") and self.is_point_in_keypoints("left_hip")
        right_shoulder_hip = self.is_point_in_keypoints("right_shoulder") and self.is_point_in_keypoints("right_hip")
        if left_shoulder_ankle or right_shoulder_ankle:
            shoulder = "left_shoulder" if left_shoulder_ankle else "right_shoulder"
            ankle = "left_ankle" if left_shoulder_ankle else "right_ankle"
            ang3 = self.one_line_angle(shoulder, ankle)
        elif left_hip_ankle or right_hip_ankle:
            hip = "left_hip" if left_hip_ankle else "right_hip"
            ankle = "left_ankle" if left_hip_ankle else "right_ankle"
            ang3 = self.one_line_angle(hip, ankle)
        elif left_shoulder_hip or right_shoulder_hip:
            shoulder = "left_shoulder" if left_shoulder_ankle else "right_shoulder"
            hip = "left_hip" if left_hip_ankle else "right_hip"
            ang3 = self.one_line_angle(shoulder, hip)
            pass

        # elbow-wristの地面から角度計算
        left_elbow_wrist = self.is_point_in_keypoints("left_elbow") and self.is_point_in_keypoints("left_wrist")
        right_elbow_wrist = self.is_point_in_keypoints("right_elbow") and self.is_point_in_keypoints("right_wrist")
        if left_elbow_wrist or right_elbow_wrist:
            elbow = "left_elbow" if left_elbow_wrist else "right_elbow"
            wrist = "left_wrist" if left_elbow_wrist else "right_wrist"
            ang4 = self.one_line_angle(elbow, wrist)
        else:
            pass

        # hip-knee-ankleの間の角度計算
        left_knee_ankle = self.is_point_in_keypoints("left_knee") and self.is_point_in_keypoints("left_ankle")
        right_knee_ankle = self.is_point_in_keypoints("right_knee") and self.is_point_in_keypoints("right_ankle")
        left_hip_knee = self.is_point_in_keypoints("left_hip") and self.is_point_in_keypoints("left_knee")
        right_hip_knee = self.is_point_in_keypoints("right_hip") and self.is_point_in_keypoints("right_knee")
        if left_knee_ankle or right_knee_ankle:
            knee = "left_knee" if left_knee_ankle else "right_knee"
            ankle = "left_ankle" if left_knee_ankle else "right_ankle"
            ang5 = self.one_line_angle(knee, ankle)
        else:
            pass
        if left_hip_knee or right_hip_knee:
            knee = "left_knee" if left_hip_knee else "right_knee"
            hip = "left_hip" if left_hip_knee else "right_hip"
            ang6 = self.one_line_angle(hip, knee)
        else:
            pass

        # 立っているかどうかを確認する
        # 立っていない場合、ifを実行
        if ang3 is not None and ((0 <= ang3 <= 50) or (130 <= ang3 <= 180)):
            # プッシュアップを判定するロジック
            if (ang1 is not None or ang2 is not None) and ang4 is not None:
                if (160 <= ang2 <= 180) or (0 <= ang2 <= 20):
                    self.pushup_counter += 1
                    self.ang1_tracker.append(ang1)
                    self.ang4_tracker.append(ang4)
        # 立っている場合、else ifにを実行
        elif ang3 is not None and (70 <= ang3 <= 110):
            # アームカールを判定するロジック
            if ang1 is not None and ang7 is None:
                if (10 <= ang1 <= 70):
                    is_armcurl = True
                    self.armcurl_tracker.append(is_armcurl)
                    if (self.armcurl_tracker[-1] == True) and (self.armcurl_tracker[-2] == False):
                        self.armcurl_counter += 1
                    is_pushup = is_squat = False
                else:
                    is_armcurl = False
                    self.armcurl_tracker.append(is_armcurl)
            elif ang1 is not None and ang7 is not None:
                if ((10 <= ang1 <= 70) or (10 <= ang7 <= 70)):
                    is_armcurl = True
                    self.armcurl_tracker.append(is_armcurl)
                    if (self.armcurl_tracker[-1] == True) and (self.armcurl_tracker[-2] == False):
                        self.armcurl_counter += 1
                    is_pushup = is_squat = False
                else:
                    is_armcurl = False
                    self.armcurl_tracker.append(is_armcurl)

        # 24フレームを連続でプッシュアップを判断した場合、プッシュアップとして認識する
        if self.pushup_counter >= 24 and len(self.ang1_tracker) == 24 and len(self.ang4_tracker) == 24:
            ang1_diff1 = abs(self.ang1_tracker[0] - self.ang1_tracker[12])
            ang1_diff2 = abs(self.ang1_tracker[12] - self.ang1_tracker[23])
            ang1_diff_mean = (ang1_diff1 + ang1_diff2) / 2
            ang4_mean = sum(self.ang4_tracker) / len(self.ang4_tracker)
            del self.ang1_tracker[0]
            del self.ang4_tracker[0]
            if ang1_diff_mean < 5 and not 75 <= ang4_mean <= 105:
                is_pushup = is_squat = is_armcurl = False
                self.armcurl_tracker.append(is_armcurl)
            else:
                is_pushup = True
                is_squat = is_armcurl = False
                self.armcurl_tracker.append(is_armcurl)

        # キーポイントの距離計算
        head_point = self.get_available_point(["nose", "left_ear", "right_ear", "left_eye", "right_eye"])
        hip = self.get_available_point(["left_hip", "right_hip"])
        knee = self.get_available_point(["left_knee", "right_knee"])
        foot = self.get_available_point(["left_ankle", "right_ankle"])
        hand_point = self.get_available_point(["left_wrist", "right_wrist"])

        if head_point is not None and hand_point is not None:
            self.headpoint_tracker.append(head_point[1]) # height only
            diff_head_hand_y = head_point[1] - hand_point[1]
        if ang3 is not None and ang5 is not None and diff_head_hand_y is not None:
            if ((70 <= ang3 <= 110) or (70 <= ang5 <= 110)) and len(self.headpoint_tracker) == 24:
                height_mean = int(sum(self.headpoint_tracker) / len(self.headpoint_tracker))
                height_norm = self.operation.normalize(height_mean, head_point[1], foot[1])
                del self.headpoint_tracker[0]
                if height_norm < 0 and diff_head_hand_y < 0 and not 70 <= abs(ang6) <= 110:
                    is_squat = True
                    is_pushup = is_armcurl = False
                    self.armcurl_tracker.append(is_armcurl)
                else:
                    is_squat = False

        if diff_head_hand_y is not None and ang3 is not None:
            if diff_head_hand_y > 0 and 80 <= ang3 <= 100:
                is_pushup = is_squat = False

        # 24フレームまでメモリに記憶する
        if len(self.ang1_tracker) == 24:
            del self.ang1_tracker[0]
        if len(self.ang4_tracker) == 24:
            del self.ang4_tracker[0]
        if len(self.headpoint_tracker) == 24:
            del self.headpoint_tracker[0]
        if len(self.armcurl_tracker) == 24:
            del self.armcurl_tracker[0]

        if is_squat:
            return "Squat"
        elif is_pushup:
            return "Pushup"
        elif is_armcurl:
            return "Arm Curl"

        return None

    def estimate(self) -> None:
        """ 骨格検出関数 """
        if self.video_reader.is_opened() is False:
            print("[ERROR] File Not Found.")

        out = cv2.VideoWriter("output.avi", self.fourcc, self.video_fps, (self.width, self.height))
        while self.video_reader.is_opened():
            image = self.video_reader.read_frame()
            if image is None:
                print("Ignoring empty camera frame.")
                break

            # 処理速度を上げるために, 画像をReadOnlyにする(画像の上に書けない)
            # 骨格検出後で、画像の上に書けるようにWriteに戻す
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.predict(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = self.draw.skeleton(image, results)
            image = self.draw.overlay(image)

            if results[0].keypoints is not None:
                self.key_points = self.get_keypoints(image, results)
                estimated_pose = self.predict_pose()
                if estimated_pose is not None:
                    self.current_pose = estimated_pose
                    self.pose_tracker.append(self.current_pose)
                    if len(self.pose_tracker) == 10 and len(set(self.pose_tracker[-6:])) == 1:
                        image = self.draw.pose_text(image, "Prediction: {}  Count: {}".format(estimated_pose, self.armcurl_counter))

            if len(self.pose_tracker) == 10:
                del self.pose_tracker[0]
                self.prev_pose = self.pose_tracker[-1]

            out.write(image)
            cv2.imshow('Exercise Prediction', image)
            key = cv2.waitKey(3)
            if key == 27:
                break
        self.video_reader.release()
        cv2.destroyAllWindows()
