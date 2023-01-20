import json
from bs4 import BeautifulSoup
import re
import sys
import os


class Phpinfo:
    def __init__(self):
        self.curl = sys.argv[1] + " -s --connect-timeout 5"  # -s参数取消curl输出
        self.content = os.popen(self.curl)
        self.rules = json.load(open("rules.json"))
        self.P = {}
        self.count = 0
        self.result = {}
        self.level = {"green": "\033[32m", "blue": "\033[34m", "red": "\033[31m"}
        self.end = "\033[0m"
        print(self.level["blue"] + "[+] " + self.curl)

    def resolvePhpinfo(self):
        content = self.content
        if content is None:
            return
        soup = BeautifulSoup(content, "html.parser")
        for div in soup.find_all("div"):
            for table in div.find_all("table"):
                # for tbody in table.find_all("tbody"):
                for tr in table.find_all("tr"):
                    e = ""
                    for tde in tr.find_all("td", class_="e"):
                        e = tde.string.strip()
                    for tdv in tr.find_all("td", class_="v"):
                        if tdv.string:
                            self.P[e] = tdv.string
                            break
        if (not self.rules) or (not self.P):
            print(self.level["red"] + "[-] 不存在phpinfo页面或无法解析" + self.end)
            sys.exit()
        # print(self.P)

    def resolveRules(self):
        for d in self.rules:
            regexes = self.rules[d]["regexes"]
            for reg in regexes:
                e = regexes[reg]["e"]
                v = regexes[reg]["v"]
                for i in self.P:
                    pe = re.compile(e, re.I).search(i)
                    if pe:
                        pv = re.compile(v, re.I).search(self.P[i])
                        if pv:
                            self.rules[d]["regexes"][reg]["v"] = self.P[i]
                            self.count += 1
                            self.resolveRes(self.rules[d]["message"], self.rules[d]["level"])

    def resolveRes(self, message, level):
        magictext = re.compile("{{(.*?)}}").search(message)
        if magictext:
            plaintext = re.compile(r"(.*){{.*}}(.*)").search(message)
            # 假设有`xxx{{abc}}yyy` `plaintext.group(1))`匹配xxx，`plaintext.group(2))`匹配yyy
            if len(plaintext.groups()) == 1:
                log = "[+] " + plaintext.group(1) + eval(magictext.group(1))
                self.result[log] = level
            elif len(plaintext.groups()) == 2:
                log = "[+] " + plaintext.group(1) + eval(magictext.group(1)) + plaintext.group(2)
                self.result[log] = level
        else:
            log = "[+] " + message
            self.result[log] = level

    def prinRes(self):
        logs = sorted(self.result.items(), key = lambda kv:(kv[1], kv[0]))
        for log in logs:
            print(self.level[log[1]] + log[0] + self.end)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('eg: python3 HackPhpinfo.py "curl http://127.0.0.1/phpinfo.php"')
        sys.exit()
    phpinfo = Phpinfo()
    phpinfo.resolvePhpinfo()
    phpinfo.resolveRules()
    phpinfo.prinRes()
