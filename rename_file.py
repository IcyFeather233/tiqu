import json
import os

geyan_filelist = []

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.csv'):
                fullname = os.path.join(root, f)
                yield fullname

def main():
    base = './ans/知乎/'
    # 获取所有文件路径
    for i in findAllFile(base):
        print(i)
        geyan_filelist.append(i)
    print(geyan_filelist)

    jsonfile = open('./transfer/zhihu.json', 'r', encoding='utf-8')
    load_dict = json.load(jsonfile)

    for e in geyan_filelist:
        ee = e[9:-4] + 'txt'
        e_trans = load_dict[ee] + '.csv'
        print(e + '  ---》  ' + e_trans)
        os.rename(e, './result/知乎/' + e_trans)

if __name__ == '__main__':
    main()