import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

# フレーム上に描くためのクラス
class Draw():
    """ 初期設定 """
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.font = ImageFont.truetype('../data/fonts/arial.ttf', self.height//24, encoding="unic")

    def bbox(self):
        """ Draw bbox """
        pass

    def skeleton(self, image, pose_results):
        """ 骨格を描く """
        for result in pose_results:
            image = result.plot(conf=False, masks=False, preds=False)
        return image

    def pose_text(self, image, estimated_pose):
        """ 判断した運動を描く """
        pil_img = Image.fromarray(image)
        pil_draw = ImageDraw.Draw(pil_img)
        text_width, _ = pil_draw.textsize(estimated_pose.upper(), font=self.font)
        pil_draw.text(((self.width - text_width) / 2, self.height//16 + 10), estimated_pose.upper(),
                    (255, 255, 255), font=self.font)
        image = np.array(pil_img)
        return image

    def overlay(self, image):
        """ 四角を描く """
        alpha = 0.5
        overlay = image.copy()
        cv2.rectangle(overlay, (0, self.height//16), (self.width, self.height//8) , (25,25,25) , -1)
        image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
        return image

    def draw_line(self, image, coord1, coord2):
        """ 線を描く """
        cv2.line(image, coord1, coord2, thickness=4, color=(255, 255, 255))
        return image
