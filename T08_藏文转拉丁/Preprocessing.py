import xlrd

class Preprocessing:
    def __init__(self, di, di2, coponent_vowPos):
        all = []
        with open('TibetTolatSyallcode.txt', 'r', encoding='utf-8') as f:
            while (True):
                a = f.readline().lstrip('\ufeff').strip().split()
                if a: all.append(a)
                else: break
            all.reverse()
            for a in all:
                di[a[0]] = a[1]
                di2[a[1]] = a[0]


        # 读取构件数据，返回元音所在位置，如果没有则返回隐形元音返回位置
        '''
        file_path: 需要读取取文件的路径
        sheet_name: 需要读取文件的表单名称
        '''
        result = []
        wb = xlrd.open_workbook('./Classified.xls')
        sheet = wb.sheet_by_name('字符结构')
        for item in range(1, sheet.nrows):  # 1：写了title就默认以1开头，如果没写title就可以省略， sheet.nrows获取总行数
            result.append(sheet.row_values(item))  # row_values:返回所有单元格组成一个list

        for word in result:
            pos = 5
            for i in range(5, 0, -1):
                if word[i]=='': pos-=1
            coponent_vowPos[word[0]] = pos
