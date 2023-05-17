import cv2

import math

mx = 0
my = 0
radius0 = 81
radius1 = 102
lcx = 124
lcy = 198
lcenter = (lcx, lcy)  # 左圆心
rcx = 1142
rcy = 198
rcenter = (rcx, rcy)  # 右圆心
# 读取图片文件
img = cv2.imread("mskover.png")

# 获取图像尺寸
height, width, channels = img.shape
img_copy = img.copy()  # 保存原始图片的副本
print(img.shape)


def get_cercle(cx, cy):
    angle_rad = math.atan2(cy - my, mx - cx)
    if angle_rad >= 0:
        angle_rad1 = angle_rad
    else:
        angle_rad1 = angle_rad + 2 * 3.1415926
    # 就用弧度算，不需要转角度
    y2 = int(cy - (radius1 * math.sin(angle_rad1)))
    x2 = int(cx + (radius1 * math.cos(angle_rad1)))
    y1 = int(cy - (radius0 * math.sin(angle_rad1)))
    x1 = int(cx + (radius0 * math.cos(angle_rad1)))
    return x1, y1, x2, y2


def get_mouse_pos(event, x, y, flags, param):
    global mx, my, img, y2, x2, y1, x1
    # 微调高度，注意y轴正方向
    trim_up = -5
    trim_upup = -10
    if event == cv2.EVENT_MOUSEMOVE:

        mx, my = x, y

        img_draw = img_copy.copy()
        print("鼠标坐标：", (x, y))
        angle_rad = 0
        # 把左右圆心标注出来
        img_draw[lcy - 1:lcy + 1, lcx - 1:lcx + 1] = [255, 255, 255]
        img_draw[rcy - 1:rcy + 1, rcx - 1:rcx + 1] = [255, 255, 255]

        # 计算左侧半圆弧度值
        if lcx > mx >= 0:
            x1, y1, x2, y2 = get_cercle(lcx, lcy)

        # 计算中间上部条形
        if lcx <= mx <= rcx and 0 < my <= rcy:
            x1 = x2 = mx
            y1 = lcy - radius1
            y2 = lcy - radius0
        # 计算中间下部条形
        if lcx <= mx <= rcx and my > rcy:
            x1 = x2 = mx
            y1 = lcy + radius1
            y2 = lcy + radius0
        # 计算右侧半圆弧度值
        if mx > rcx:
            x1, y1, x2, y2 = get_cercle(rcx, rcy)
        # 画线
        cv2.line(img_draw, (x1, y1), (x2, y2), (0, 255, 0), 3)
        # 在图片上添加文本
        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型
        text0 = "flag:"  # flag
        text1 = str(y1)  # flag
        text2 = str(x1)  # 一条线上有几个合格
        text3 = "rate:"
        color = (255, 255, 255)  # BGR 格式颜色
        thickness = 1  # 粗细
        font_scale = 0.8  # 字体大小
        text_size0, _ = cv2.getTextSize(text0, font, font_scale, thickness)
        text_size1, _ = cv2.getTextSize(text1, font, font_scale, thickness)
        text_size2, _ = cv2.getTextSize(text2, font, font_scale, thickness)
        text_size3, _ = cv2.getTextSize(text3, font, font_scale, thickness)
        # text_size[0] text长度，text_size[1] text高度
        # 写字上部
        if 0 < my <= rcy:
            # 写字，右侧半圆上部
            if mx > rcx:
                if text_size2[0] + x2 > width - rcx:
                    # 第一个汉字语句
                    cv2.putText(img_draw, text0, (x1 - text_size2[0] - text_size0[0], y1 + text_size2[1]), font,
                                font_scale, color,
                                thickness)
                    # 数据1
                    cv2.putText(img_draw, text1, (x1 - text_size2[0], y1 + text_size2[1]), font, font_scale, color,
                                thickness)
                    # 数据2
                    cv2.putText(img_draw, text2, (x1 - text_size2[0], y1 + 2 * text_size2[1]), font, font_scale, color,
                                thickness)
                    # 第二个汉字语句
                    cv2.putText(img_draw, text3, (x1 - text_size3[0] - text_size3[0], y1 + 2 * text_size2[1]), font,
                                font_scale, color,
                                thickness)
            # 写字，左侧半圆上部
            if mx < lcx:
                if text_size2[0] + text_size3[0] > x2:
                    cv2.putText(img_draw, text0, (x1, y1 + text_size2[1]), font, font_scale, color,
                                thickness)
                    cv2.putText(img_draw, text1, (x1 + text_size0[0], y1 + text_size2[1]), font, font_scale, color,
                                thickness)
                    cv2.putText(img_draw, text2, (x1 + text_size3[0], y1 + 2 * text_size2[1]), font, font_scale, color,
                                thickness)
                    cv2.putText(img_draw, text3, (x1, y1 + 2 * text_size2[1]), font, font_scale, color,
                                thickness)

            # 写字，中间条形上部
            if lcx <= mx <= rcx:
                cv2.putText(img_draw, text0, (x1 - text_size0[0], y1 - text_size2[1] + trim_upup), font, font_scale,
                            color,
                            thickness)
                cv2.putText(img_draw, text1, (x1, y1 - text_size2[1] + trim_upup), font, font_scale, color, thickness)
                cv2.putText(img_draw, text2, (x1, y1 + trim_up), font, font_scale, color, thickness)
                cv2.putText(img_draw, text3, (x1 - text_size3[0], y1 + trim_up), font, font_scale, color, thickness)
        else:
            # 写字，右侧半圆下部
            if mx > rcx:
                # if text_size2[0] + x2 > width:
                cv2.putText(img_draw, text0, (x1 - text_size2[0] - text_size0[0], y1 - text_size2[1]), font, font_scale,
                            color,
                            thickness)
                cv2.putText(img_draw, text1, (x1 - text_size2[0], y1 - text_size2[1]), font, font_scale, color,
                            thickness)
                cv2.putText(img_draw, text2, (x1 - text_size2[0], y1), font, font_scale, color,
                            thickness)
                cv2.putText(img_draw, text3, (x1 - text_size2[0] - text_size3[0], y1), font, font_scale, color,
                            thickness)
                # else:
                # cv2.putText(img_draw, text1, (x1 - text_size2[0], y1 - text_size2[1]), font, font_scale, color,
                #             thickness)
                # cv2.putText(img_draw, text2, (x1 - text_size2[0], y1), font, font_scale, color,
                #             thickness)
            # 写字，左侧半圆下部
            if mx < lcx:
                if text_size2[0] + text_size3[0] > x2:
                    cv2.putText(img_draw, text0, (x1, y1 - text_size2[1]), font, font_scale, (255, 255, 0),
                                thickness)
                    cv2.putText(img_draw, text1, (x1 + text_size0[0], y1 - text_size2[1]), font, font_scale, color,
                                thickness)
                    cv2.putText(img_draw, text2, (x1 + text_size3[0], y1), font, font_scale, color,
                                thickness)
                    cv2.putText(img_draw, text3, (x1, y1), font, font_scale, color,
                                thickness)

            # 写字，中间条形下部,分成三部分
            # 左
            if lcx + text_size3[0] > mx >= lcx:
                cv2.putText(img_draw, text0, (x1, y2 - text_size2[1]+trim_upup), font, font_scale, (0, 0, 255),
                            thickness)
                cv2.putText(img_draw, text1, (x1 + text_size0[0], y2 - text_size2[1]+trim_upup), font, font_scale, color,
                            thickness)
                cv2.putText(img_draw, text2, (x1 + text_size3[0], y2+trim_up), font, font_scale, color, thickness)
                cv2.putText(img_draw, text3, (x1, y2+trim_up), font, font_scale, color, thickness)
            # 中间
            if lcx + text_size3[0] <= mx <= rcx - text_size2[0]:
                cv2.putText(img_draw, text0, (x1 - text_size0[0], y2 - text_size2[1]+trim_upup), font, font_scale, color,
                            thickness)
                cv2.putText(img_draw, text1, (x1, y2 - text_size2[1]+trim_upup), font, font_scale, color, thickness)
                cv2.putText(img_draw, text2, (x1, y2+trim_up), font, font_scale, color, thickness)
                cv2.putText(img_draw, text3, (x1 - text_size3[0], y2+trim_up), font, font_scale, color, thickness)
            # 右侧
            if rcx - text_size2[0] < mx <= rcx:
                cv2.putText(img_draw, text0, (x1 - text_size2[0] - text_size0[0], y2 - text_size2[1]+trim_upup), font, font_scale,
                            color,
                            thickness)
                cv2.putText(img_draw, text1, (x1 - text_size2[0], y2 - text_size2[1]+trim_upup), font, font_scale, color,
                            thickness)
                cv2.putText(img_draw, text2, (x1 - text_size2[0], y2+trim_up), font, font_scale, color,
                            thickness)
                cv2.putText(img_draw, text3, (x1 - text_size2[0] - text_size3[0], y2+trim_up), font, font_scale, color,
                            thickness)

        # 显示更新后的图像
        cv2.imshow("image", img_draw)


# 初始化显示窗口
cv2.namedWindow("image")

# 绑定鼠标事件处理函数
cv2.setMouseCallback("image", get_mouse_pos)
# 在窗口中显示图片
cv2.imshow("image", img)

cv2.waitKey(0)

# 释放窗口资源
cv2.destroyAllWindows()
