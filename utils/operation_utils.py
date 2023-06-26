import math

# 線の角度、点の距離などの演算クラス
class Operation():
    """ 初期設定 """
    def __init__(self) -> None:
        pass

    def angle_of_singleline(self, point1, point2):
        """ 線の角度演算 """
        x_diff = point2[0] - point1[0]
        y_diff = point2[1] - point1[1]
        return math.degrees(math.atan2(y_diff, x_diff))
    
    def vector(self, point2, point1):
        """線をベクトル化する"""
        return (point1[0]-point2[0], point1[1]-point2[1])

    def angle(self, point1, point2, point3):
        """ 2つの線の間の角度演算 """

        if(point1==(0,0) or point2==(0,0) or point3==(0,0)):
            return 0
    
        vector1 = self.vector(point2, point1)
        vector2 = self.vector(point2, point3)

        numerator = (vector1[0]*vector2[0]) + (vector1[1]*vector2[1])
        denominator = (math.sqrt((vector1[0] ** 2)+(vector1[1] ** 2))) * \
            (math.sqrt((vector2[0] ** 2)+(vector2[1] ** 2)))
        
        if (numerator/denominator) == -1:
            return 180

        ang = math.degrees(math.acos(numerator/denominator))
        return ang

    def dist_xy(self, point1, point2):
        """ 2つの点の間の距離 """
        diff_point1 = (point1[0] - point2[0]) ** 2
        diff_point2 = (point1[1] - point2[1]) ** 2
        return (diff_point1 + diff_point2) ** 0.5

    def dist_x(self, point1, point2):
        """ 2つの点の間のx距離 """
        return abs(point2[0] - point1[0])

    def dist_y(self, point1, point2):
        """ 2つの点の間のy距離 """
        return abs(point2[1] - point1[1])

    def point_position(self, point, line_pt_1, line_pt_2):
        """ 点は線の左側か右側を判断する """
        value = (line_pt_2[0] - line_pt_1[0]) * (point[1] - line_pt_1[1]) - \
                    (line_pt_2[1] - line_pt_1[1]) * (point[0] - line_pt_1[0])
        if value >= 0:
            return "left"
        return "right"

    def normalize(self, value, min_val, max_val):
        """ 点のx,y座標を正常化する """
        return (value - min_val) / (max_val - min_val)
