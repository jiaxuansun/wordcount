import os
import argparse
import re


def wordcount(content):
    print(re.split(r"[\s,]+", content))
    result = {
        "words": len(re.split(r"[\s,]+", content))-1,  # 单词数
        "lines": len(content.split('\n'))-1,  # 行数
        "bytes": len(content)  # 字符数
    }

    return result


def print_result(args, result):
    output = open(args.output, "w+")
    for r in result:
        s = "{}".format(r["filename"])
        if args.stoplist:
            stoplist = open(args.stoplist)
            stopchars = stoplist.read().split()
            count = 0
            for c in stopchars:
                count += len(re.findall(c, content))
            r["words"] -= count
            stoplist.close()
        if args.bytes:
            s += ", 字符数: {}".format(r["bytes"])
        if args.lines:
            s += ", 行数: {}".format(r["lines"])
        if args.words:
            s += ", 单词数: {}".format(r["words"])
        if args.code:
            s += ", 代码行/空行/注释行: {}/{}/{}".format(
                r["codelines"], r["blanklines"], r["commentlines"])
        s += '\n'
        output.write(s)
    output.close()


def main(args, rootpath):
    result = []
    filename = args.filename.replace("*", "\\w*")
    if args.recursive:
        for name in os.listdir(rootpath):
            path = os.path.join(rootpath, name)
            if os.path.isdir(path):
                result += main(args, path)
            elif re.findall(filename, name):
                fd = open(path)
                wc = wordcount(fd.read())
                wc["filename"] = name
                result.append(wc)
                fd.close()
    else:
        for name in os.listdir(rootpath):
            path = os.path.join(rootpath, name)
            if os.path.isdir(path):
                pass
            elif re.findall(filename, name):
                fd = open(path)
                wc = wordcount(fd.read())
                wc["filename"] = name
                result.append(wc)
                fd.close()

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="word count")
    parser.add_argument("-o", "--output", type=str, default="result.txt")
    parser.add_argument("-c", "--bytes", action="store_true")
    parser.add_argument("-w", "--words", action="store_true")
    parser.add_argument("-l", "--lines", action="store_true")
    parser.add_argument("-s", "--recursive", action="store_true")
    parser.add_argument("-a", "--code", action="store_true")
    parser.add_argument("-e", "--stoplist", type=str)
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    result = main(args, os.getcwd())
    print_result(args, result)
