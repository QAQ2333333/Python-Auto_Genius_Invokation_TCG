import time
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\OCR\tesseract.exe'

temp_shui = cv2.imread('water.png')
temp_huo = cv2.imread('fire.png')
temp_fen = cv2.imread('wind.png')
temp_lei = cv2.imread('lei.png')
temp_cao = cv2.imread('glass.png')
temp_bin = cv2.imread('ice.png')
temp_yan = cv2.imread('stone.png')
temp_all = cv2.imread('all.png')

temp_shui_ = cv2.imread('water_.png')
temp_huo_ = cv2.imread('fire_.png')
temp_fen_ = cv2.imread('wind_.png')
temp_lei_ = cv2.imread('lei_.png')
temp_cao_ = cv2.imread('glass_.png')
temp_bin_ = cv2.imread('ice_.png')
temp_yan_ = cv2.imread('stone_.png')
temp_all_ = cv2.imread('all_.png')

dices = [(318, 504), (318, 695), (318, 878), (318, 1067), (523, 504), (523, 695), (523, 878), (523, 1067)]
name = ['水', '火', '风', '雷', '草', '冰', '岩', '万能']
need_dices = [0, 4, 7]  # 按照上面的顺序选择需要保留的元素
turn_num = 2
people_num = 0
player_health = [1, 1, 1]
inin_num = 1


# 初始定位窗口位置
def init_shot():
    global x_window, y_window, width, height
    # 通过窗口标题获取窗口对象
    window_title = '原神'
    app_window = gw.getWindowsWithTitle(window_title)[0]

    # 获取窗口的位置和大小
    x_window, y_window, width, height = app_window.left, app_window.top, app_window.width, app_window.height


# 截图
def screenshot():
    global img
    global image
    # 截取窗口的截图
    shot = pyautogui.screenshot(region=(x_window, y_window, width, height))
    image_np = np.array(shot)
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image = img[29:930, 8:1608]


# 判断重投阶段的元素
def judge_dice():
    screenshot()
    templ1 = image[318:355, 504:530]
    templ2 = image[318:355, 695:717]
    templ3 = image[318:355, 878:906]
    templ4 = image[318:355, 1067:1094]
    templ5 = image[523:560, 504:530]
    templ6 = image[523:560, 695:717]
    templ7 = image[523:560, 878:906]
    templ8 = image[523:560, 1067:1094]

    # cv2.imshow('ss',temp2)
    # cv2.waitKey()

    match = [templ1, templ2, templ3, templ4, templ5, templ6, templ7, templ8]
    templ = [temp_shui, temp_huo, temp_fen, temp_lei, temp_cao, temp_bin, temp_yan, temp_all]

    need = [1, 1, 1, 1, 1, 1, 1, 1]
    for j, diagram in enumerate(match):

        lst = []

        for i, imgs in enumerate(templ):
            re = cv2.matchTemplate(imgs, diagram, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(re)
            lst.append(min_val)
            # print(name[i] + f"最佳匹配度: {min_val}")

        min_value = min(lst)
        min_index = lst.index(min_value)
        print(name[min_index] + f' 为最佳匹配元素')

        if min_index in [0, 4, 7]:
            need[j] = 0

        # print()

    print(need)
    return need


def sure():
    x = x_window + 789
    y = y_window + 789
    pyautogui.click(x, y, clicks=1, button='left')
    print('INFO:已点击')


def clean():
    time.sleep(1)
    pyautogui.click(797 + x_window, 443 + y_window, clicks=2, button='left')


def end():
    print('INFO:结束阶段————————')
    print('INFO:将结束本回合')
    time.sleep(2)
    pyautogui.click(64 + x_window, 445 + y_window, clicks=1, button='left')
    time.sleep(1)
    pyautogui.click(169 + x_window, 445 + y_window, clicks=1, button='left')
    time.sleep(5)


# 调和元素
def harmony():
    x1 = 840 + x_window
    y1 = 900 + y_window
    x2 = 1551 + x_window
    y2 = 499 + y_window
    pyautogui.click(797 + x_window, 443 + y_window, clicks=2, button='left')
    time.sleep(0.5)
    pyautogui.click(x1, y1, clicks=2, button='left')
    pyautogui.mouseDown()
    time.sleep(0.5)
    pyautogui.mouseUp()
    pyautogui.click(x1, y1, clicks=1, button='left')
    pyautogui.moveTo(x2, y2, duration=0.1)
    pyautogui.mouseUp()
    pyautogui.click(x2, y2, clicks=2, button='left')
    time.sleep(1)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    print('INFO:已调和')

    time.sleep(1)
    x = x_window + 789
    y = y_window + 789
    pyautogui.click(x, y, clicks=1, button='left')
    print('INFO:已点击')
    time.sleep(1)
    clean()


# 点击元素骰
def click_dice(where):
    screenshot()
    for num, point in enumerate(where):
        if point:
            y1, x1 = dices[num]
            y = y_window + y1
            x = x_window + x1
            pyautogui.click(x, y, clicks=1, button='left')
            time.sleep(0.05)
    print('INFO:已点击')
    sure()


# 右下角
def judge_stage():  # 右下角
    gray = cv2.cvtColor(image[853:870, 119:180], cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 120, 225, cv2.THRESH_BINARY)

    # 应用一些形态学操作来减少噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='chi_sim')
    # print(text)
    return text


# 重投
def judge_stage_pro():  # 重投
    gray = cv2.cvtColor(image[140:192, 700:900], cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 120, 225, cv2.THRESH_BINARY)

    # 应用一些形态学操作来减少噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='chi_sim')
    # print(f'识别到：{text}')
    return text


# 角色
def judge_stage_pro_max():  # 角色
    gray = cv2.cvtColor(image[711:736, 1473:1566], cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 140, 225, cv2.THRESH_BINARY)

    # 应用一些形态学操作来减少噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='chi_sim')
    # print(f'识别到：{text}')
    return text


# 判断能不能放技能，True是需要调和，False是可以行动
def judge_enough(which, element, n):
    templ_1 = image[156:172, 1546:1565]
    templ_2 = image[194:209, 1546:1565]
    templ_3 = image[232:249, 1546:1565]
    templ_4 = image[270:287, 1546:1565]
    templ_5 = image[307:325, 1546:1565]
    templ_6 = image[346:363, 1546:1565]
    templ_7 = image[384:401, 1546:1565]
    templ_8 = image[422:439, 1546:1565]

    name = ['水', '火', '风', '雷', '草', '冰', '岩', '万能']
    need_element = [7]
    for ele in element:
        need_element.append(ele)

    match = [templ_1, templ_2, templ_3, templ_4, templ_5, templ_6, templ_7, templ_8]
    templ = [temp_shui_, temp_huo_, temp_fen_, temp_lei_, temp_cao_, temp_bin_, temp_yan_, temp_all_]

    need = [0, 0, 0, 0, 0, 0, 0, 0]
    for j, diagram in enumerate(match):
        if j < n:

            lst = []

            for i, imgs in enumerate(templ):
                re = cv2.matchTemplate(imgs, diagram, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(re)
                lst.append(min_val)
                # print(name[i] + f"最佳匹配度: {min_val}")

            min_value = min(lst)
            min_index = lst.index(min_value)
            print(name[min_index] + f' 为最佳匹配元素')

            if min_index in need_element:
                need[min_index] += 1

    print(f'INFO:识别到行动元素：{need}')

    point = 0

    for points in need:
        point += points

    if which == 1:
        if point >= 1:
            print(f'INFO:检测到有效元素：{point},即将行动')
            return False, None
        else:
            print(f'INFO:检测到有效元素：{point},不可以行动，将进行元素调和')
            return True, 1

    elif which == 2 or 3:
        if point >= 3:
            print(f'INFO:检测到有效元素：{point},即将行动')
            return False, None
        else:
            print(f'INFO:检测到有效元素：{point},不可以行动，将进行元素调和')
            r = 3 - point
            return True, r


# 判断角色站位
def judge_position(c):
    screenshot()
    positions = []
    people_position = [(558, 687), (735, 864), (907, 1040)]
    for x1_position, x2_position in people_position:
        gray = cv2.cvtColor(image[484:504, x1_position:x2_position], cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 224, 225, cv2.THRESH_BINARY_INV)
        white = np.sum(thresh == 0)

        positions.append(white)

    best = max(positions)
    best_position = positions.index(best)
    print(f'INFO:当前角色位置：{best_position}')
    if best_position == c - 1:
        return True, best_position
    else:
        print(f'INFO:不满足要求,即将切换角色位置：{c - 1}')
        return False, best_position


# 释放技能
def click_skill(what):  # 123技能
    if what == 1:
        print('INFO:将释放1技能')
        pyautogui.click(1316 + x_window, 807 + y_window, clicks=1, button='left')
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()

    elif what == 2:
        print('INFO:将释放2技能')
        pyautogui.click(1423 + x_window, 807 + y_window, clicks=1, button='left')
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()

    elif what == 3:
        print('INFO:将释放3技能')
        pyautogui.click(1500 + x_window, 807 + y_window, clicks=1, button='left')
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()


# 换人
def change(who):
    global turn_num
    if who == 1:
        print('INFO:执行换人：1号位')
        print(f'当前执行策略第{turn_num}步')
        pyautogui.click(619 + x_window, 626 + y_window, clicks=1, button='left')
        time.sleep(1.4)
        pyautogui.moveTo(1519 + x_window, 798 + y_window, duration=0.1)
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        clean()
        time.sleep(5)
        turn_num = turn_num + 1
    elif who == 2:
        print('INFO:执行换人：2号位')
        print(f'当前执行策略第{turn_num}步')
        pyautogui.click(791 + x_window, 626 + y_window, clicks=1, button='left')
        time.sleep(1.4)
        pyautogui.moveTo(1519 + x_window, 798 + y_window, duration=0.1)
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        clean()
        time.sleep(5)
        turn_num = turn_num + 1
    elif who == 3:
        print('INFO:执行换人：3号位')
        print(f'当前执行策略第{turn_num}步')
        pyautogui.click(972 + x_window, 626 + y_window, clicks=1, button='left')
        time.sleep(1.4)
        pyautogui.moveTo(1519 + x_window, 798 + y_window, duration=0.1)
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        clean()
        time.sleep(5)
        turn_num = turn_num + 1
    elif who == 4:
        pyautogui.moveTo(1519 + x_window, 798 + y_window, duration=0.1)
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        time.sleep(0.35)
        pyautogui.mouseUp()
        clean()
        time.sleep(5)

# 判断行动点数
def get_point():
    screenshot()
    gray = cv2.cvtColor(image[537:562, 56:76], cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 200, 225, cv2.THRESH_BINARY)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    print(f'INFO:当前剩余行动点数：{text}')
    if text != '':
        try:
            number = int(text)
            return number

        except:
            return 0

    else:
        print('WARMING:未识别到行动点数')
        return 0


# 判断角色是否死亡
def health(who_is_first):
    global player_health
    health_list1 = [(544, 577), (717, 761), (893, 932)]
    for ii, (xx, yy) in enumerate(health_list1):
        if who_is_first != ii:
            gray = cv2.cvtColor(image[536:564, xx:yy], cv2.COLOR_BGR2GRAY)

        if who_is_first == ii:
            gray = cv2.cvtColor(image[499:528, xx:yy], cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 224, 225, cv2.THRESH_BINARY_INV)

        # cv2.imshow('Processed Image', gray)
        # cv2.waitKey()

        white = np.sum(thresh == 0)
        if white > 10:
            player_health[ii] = 1
        else:
            player_health[ii] = 0


# 行动(攻击）
def attack(skill, ele):
    global turn_num
    get_p = get_point()
    if get_p >= 3:
        b, times = judge_enough(skill, ele, get_p)
        if b:
            for _ in range(0, times):
                harmony()
        if not b:
            print(f'当前执行策略第{turn_num}步')
            turn_num = turn_num + 1
            click_skill(skill)

    if get_p < 3:
        end()


# 主判断
def judge():
    global people_num
    global turn_num
    response = judge_stage()

    if '行动' in response:
        print('INFO:识别到行动阶段，正在确认：5s')
        time.sleep(6.5)
        screenshot()
        response = judge_stage()
        if '行动' in response:
            print('INFO:确认完成')
            print('INFO:行动阶段——————————')
            return 1
        else:
            print('WARMING:确认失败，当前阶段不为行动阶段')
    elif '等' in response:
        print('INFO:等待阶段——————————')
        time.sleep(1.5)
        return None

    else:
        print('INFO:未知阶段——————————')
        time.sleep(1.5)

        response2 = judge_stage_pro()
        if '重' in response2:
            print('INFO:识别到重投阶段，正在确认：2s')
            screenshot()
            response2 = judge_stage_pro()
            if '重' in response2:
                print('INFO:确认完成')
                print('INFO:重投阶段——————————')
                return 0

        response3 = judge_stage_pro_max()
        if '角色' in response3:
            time.sleep(2)
            screenshot()
            rr = judge_stage_pro_max()
            if '角色' in rr:
                if people_num == 0:
                    people_num = 1
                    turn_num = 1
                    return 2
                elif people_num == 1:
                    turn_num = 7
        return None


# 读取策略
def read(line):
    global need_position
    with open('plan.txt', 'r') as f:
        n_element = []
        for i, l in enumerate(f, start=1):
            if i == line:
                l = l.strip()
                try:
                    request = l[0:6]
                    if request == 'change':
                        need_position = int(l[6:7])
                    request_num = int(l[6:7])
                    n_element.append(int(l[7:8]))
                    try:
                        hjiuesfd = int(l[8:9])
                        n_element.append(hjiuesfd)
                    except:
                        break
                    break
                except:
                    print('WARMING:读取策略出现问题')
                    break
            else:
                request = '所有策略已经执行完毕'
                request_num = None

    print(f'INFO:执行操作：{request}，操作位号：{request_num}')
    return request, request_num, n_element


# 主函数
def main():
    global turn_num, need_position
    turn_num = 2
    print('项目地址：https://github.com/QAQ2333333/Python-Auto_Genius_Invokation_TCG')
    print('INFO：即将开始自动七圣召唤————————————')
    time.sleep(2)

    init_shot()
    sure()
    while True:
        screenshot()
        state = judge()  # 0为重投阶段，1为行动阶段,2为选择角色

        if state == 0:
            q = judge_dice()
            click_dice(q)
            print('INFO:完成重投操作，将休眠5s')
            time.sleep(5)

        elif state == 1:
            print('INFO:开始行动——————————')
            request, request_num, need_element = read(turn_num)
            if request == 'change':
                need_position = request_num
                k, l = judge_position(request_num)
                health(l)
                if player_health[request_num]:
                    if l == request_num:
                        turn_num = turn_num + 1
                        print('INFO:跳过换人阶段')
                    else:
                        change(request_num)
                else:
                    print('WARMING:角色已死亡')
                    turn_num = turn_num + 1
            elif request == 'attack':
                g, h = judge_position(need_position)
                health(h)
                if g and player_health[h]:
                    attack(request_num, need_element)
                else:
                    if player_health[h] == 0:
                        print('WARMING:角色已死亡')
                    change(need_position)
            elif request == '所有策略已经执行完毕':
                turn_num = turn_num + 1
                attack(1, [0])

        elif state == 2:
            if inin_num:
                inin_num = 1
                request, request_num, need_element = read(1)
                change(request_num)
            else:
                change(4)

if __name__ == '__main__':
    main()
