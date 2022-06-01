# coding=utf-8
import os
import argparse
import string

import chardet

# 所支持的目标编码
support_charset = {"utf-8", "GB2312"}


def file_list(path:string, target_encoding:string):
    """查找需要转码的文件
    :param path: 需要搜索的路径
    :param target_encoding: 需要转换成的目标编码
    """
    need_convert = []
    # 遍历所有文件，选择需要转化的文件
    for root, _, files in os.walk(path, topdown=True):  # 自顶向下遍历
        if len(files) == 0:     # 跳过空文件夹
            continue
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                text = f.read()
                char_encoding = chardet.detect(text)["encoding"]
                # 如果不再支持列表中说明可能是二进制或者ASCII编码不需要转换
                if char_encoding in support_charset and char_encoding != target_encoding:
                    need_convert.append((file_path, char_encoding))
    return need_convert


def convert(source: tuple, target_encoding):
    """对目标文件转码
    :param source: 包括file_path与file_encoding, 其中file_path 需要转码的文件地址, file_encoding 需要转码的文件所用编码
    :parm target_encoding: 需要转换成的目标编码
    """
    file_path = source[0]
    file_encoding = source[1]
    target_path = file_path + ".temp"       # 所创建的临时文件名称
    with open(source[0], 'r', encoding=file_encoding) as f, open(target_path, 'w', encoding=target_encoding) as t:
        text = f.read()
        t.write(text)
    os.remove(source[0])                # 将源编码文件删除
    os.rename(target_path, source[0])   # 将临时文件编码重命名为原文件


def main():
    parse = argparse.ArgumentParser(description="文件编码转换")
    parse.add_argument("--path",help="需要转码的文件夹路径", default=".")
    parse.add_argument("--target",help="目标编码目前支持utf-8与GB2312", default="utf-8")
    args = parse.parse_args()           # 开始解析命令行产生
    path = args.path                    # 需要转码的路径
    target_encoding= args.target        # 需要转换成的目标编码 
    files = file_list(path, target_encoding)    
    for file in files:
        print("convert %s from %s to %s\n", file[0], file[1], target_encoding)
        convert(file, target_encoding)


if __name__ == "__main__":
    main()