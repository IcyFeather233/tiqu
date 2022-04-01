import csv
import multiprocessing
import os
import re
import distance
import json

geyan_filelist = []


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.csv'):
                fullname = os.path.join(root, f)
                yield fullname


# 标题,作者,朝代,原文,目标句子,翻译,注释,赏析
def handle_one_file(filename):
    # 首先就创建对应的输出文件，注意这个文件名要经过映射处理
    new_file = open('./ans/百度知道/' + filename[13:], 'w+', encoding='utf-8')

    # # 然后先把第一行写进去
    # writer = csv.writer(new_file)
    # writer.writerow(['标题', '作者', '原文句子', '译文句子', '赏析', '原文分词', '译文分词', '赏析分词'])

    print(filename + ' 进入处理步骤')
    # 按行读文件
    originfile = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(originfile)
    rows = [row for row in reader]

    for each in rows[1:]:
        print(each)
        # 跳过空行
        if len(each) == 0:
            continue
        # 目标句子
        target = each[5]
        # 去掉括号和其中的内容
        target = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", target)
        print('目标句子为： ' + target)
        # 分割目标句子为短句子
        target_list = re.split('。|！|？', target)
        for e_target in target_list:
            if e_target == '':
                continue
            print('切割后的目标句子含有：' + e_target)
            # 一个目标句子切割完了之后，其实还是属于同一首诗，一个找到了，就要马上break
            is_repeat = check_repeat(e_target, filename)
            # 重复了马上跳到下一行检测
            if is_repeat:
                break

    originfile.close()
    new_file.close()


def check_repeat(target, filename):
    print('进入了check repeat, filename为' + filename)
    # 这里一定要是追加
    new_file = open('./ans/百度知道/' + filename[13:], 'a+', encoding='utf-8')
    writer = csv.writer(new_file)
    print('创建了file')
    standard_file = open('./res/诗句、译文、赏析文件.csv', 'r', encoding='utf-8')
    print('读取完毕')
    reader = csv.reader(standard_file)
    rows = [row for row in reader]
    # 遍历  诗句、译文、赏析文件.csv
    for each in rows[1:]:
        # content是原文
        content = each[2]
        print('标准文件中的原文内容： ' + content + '\n')
        content_list = re.split('。|！|？', content)
        for e in content_list:
            if len(e) == 0:
                continue
            print('切割后的标准文件原句： ' + e)
            if distance.levenshtein(target, e) <= 2:
                # 判定为重复
                print('判定' + target + '和' + e + '为重复')
                writer.writerow(each)
                new_file.close()
                standard_file.close()
                # 找到重复了
                return True
    new_file.close()
    standard_file.close()
    return False


def main():
    base = './res/百度知道/'
    # 获取所有文件路径
    for i in findAllFile(base):
        print(i)
        geyan_filelist.append(i)
    # 开12个进程，每个文件用单独一个进程处理
    pool = multiprocessing.Pool(12)
    for each_geyanfile in geyan_filelist:
        print('---开启新进程---')
        print('该进程处理： ' + each_geyanfile)
        # 传入文件路径
        pool.apply_async(handle_one_file, args=(each_geyanfile,))
    # 结束
    pool.close()
    pool.join()
    print('---end---')


if __name__ == '__main__':
    main()
