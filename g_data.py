import pyperclip


def ch2num(ch_num):
    if '万' in ch_num:
        ch_num = ch_num.replace('万', '')
        num = float(ch_num) * 10000
    else:
        num = float(ch_num)
    return int(num)


def read_csv(path):
    '''读取csv文件

    :param path: 文件路径
    :return: 字典列表
    '''
    with open(path, encoding='ansi') as f:
        f_csv = csv.DictReader(f)
        rows = [i for i in f_csv]
        return rows


def write_csv(data_dic_lst, path):
    '''写入 csv

    :param data_dic_lst: 字典列表
    :param path: 路径
    :return: none
    '''
    headers = [i for i in data_dic_lst[0].keys()]
    with open(path, 'w', encoding='ansi', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(data_dic_lst)


def read_clip():
    return pyperclip.paste()


def write_clip(text):
    pyperclip.copy(text)


def a_one(i_input):
    if type(i_input) == int:
        num = i_input - 1
        sequence = list(map(lambda x: chr(x), range(ord('A'), ord('Z') + 1)))
        L = []
        if num > 25:
            while True:
                d = int(num / 26)
                remainder = num % 26
                if d <= 25:
                    L.insert(0, sequence[remainder])
                    L.insert(0, sequence[d - 1])
                    break
                else:
                    L.insert(0, sequence[remainder])
                    num = d - 1
        else:
            L.append(sequence[num])

        return "".join(L)
    if type(i_input) == str:
        s = i_input
        sequence = list(map(lambda x: chr(x), range(ord('A'), ord('Z') + 1)))
        l = len(s)
        sum = 0
        if l > 1:
            for i_input in range(l - 1):
                index = sequence.index(s[i_input])
                num = pow(26, l - 1) * (index + 1)
                l = l - 1
                sum = sum + num
            sum = sum + sequence.index(s[-1])
        else:
            sum = sum + sequence.index(s[-1])
        return sum + 1
