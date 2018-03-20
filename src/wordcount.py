import os
import argparse
import re


def wordcount(content):
    print(re.split(r"[\s,]+", content))
    result = {
        "words": len(re.split(r"[\s,]+", content))-1,  # 单词数
        "lines": len(content.split('\n'))-1,  # 行数
        "bytes": len(content)-1  # 字符数
    }

    return result


def codecount(fd):
    codelines = 0
    blanklines = 0
    commentlines = 0
    isComment = False
    isString = False
    isCode = False
    for line in fd.readlines():
        line = line.strip().replace('{', '').replace(
            '}', '').replace(';', '')  # 去掉{};以便计算空行
        if not isComment and not line:
            blanklines += 1
            continue
        if isComment:
            commentlines += 1
        elif line.replace('/', '').replace('*', ''):
            codelines += 1
        line = '\n'+line+'\n'
        for i in range(1, len(line)):
            if line[i] == '"' and line[i-1] != '\\':
                isString = not isString
            if not isString:
                if line[i] == '/' and line[i+1] == '/' and not isComment:
                    if not line[:i].split():
                        blanklines += 1
                    commentlines += 1
                    break
                if line[i] == '/' and line[i+1] == '*' and not isComment:
                    isComment = True
                    commentlines += 1
                    i += 1
                if line[i] == '*' and line[i+1] == '/':
                    isComment = False
                    i += 1

    result = {
        "codelines": codelines,
        "blanklines": blanklines,
        "commentlines": commentlines
    }

    return result


def print_result(args, result):
    output = open(args.output, "w+")
    for r in result:
        s = "{}".format(r["filename"])
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
                if args.stoplist:
                    fd.seek(0)
                    content = fd.read()
                    stoplist = open(args.stoplist)
                    stopchars = stoplist.read().split()
                    count = 0
                    for c in stopchars:
                        count += len(re.findall(c, content))
                    r["words"] -= count
                    stoplist.close()
                if args.code:
                    fd.seek(0)
                    wc.update(codecount(fd))
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
                if args.stoplist:
                    fd.seek(0)
                    content = fd.read()
                    stoplist = open(args.stoplist)
                    stopchars = stoplist.read().split()
                    count = 0
                    for c in stopchars:
                        count += len(re.findall(c, content))
                    r["words"] -= count
                    stoplist.close()
                if args.code:
                    fd.seek(0)
                    wc.update(codecount(fd))
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
