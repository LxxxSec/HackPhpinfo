# HackPhpinfo使用介绍

## What?

这是一款基于正则匹配的phpinfo信息收集工具，项目地址如下：

-   https://github.com/LxxxSec/HackPhpinfo

主要解决以下痛点：

-   CTF比赛中可能会有phpinfo页面泄露，而出题人的考点通常在某个扩展中，phpinfo过多的信息可能会导致选手落下某个关键信息

## How to use?

工具很简单，使用bs4解析phpinfo页面，存储phpinfo页面中设置的值，接着用规则去匹配，如果匹配成功则输出匹配结果

使用下方pip命令安装bs4即可

```
pip3 install beautifulsoup4
```

本工具使用curl请求页面，通常来说Windows和unix都自带了curl，如果在比赛过程中需要POST或者Header传额外参数才能得到phpinfo页面，可以自行参考curl的用法

使用方法也很简单：

-   在第一个参数中传入curl命令即可，记得用双引号引起来

```
python3 HackPhpinfo.py "curl http://127.0.0.1/phpinfo.php"
```

![image-20230120112348282](https://lxxx-markdown.oss-cn-beijing.aliyuncs.com/pictures/202301201123357.png)

## How to expand?

工具的核心在rules.json规则，目前支持检测以下规则：

-   gettext
-   allow_url_include
-   opcache
-   auto_append_file
-   auto_prepend_file
-   FLAG
-   网站根目录
-   PHP版本
-   imagick扩展
-   当前用户
-   phar.readonly
-   disable_functions

如果有更多需要的规则，欢迎提issue补充~

规则编写说明如下：

-   6为规则编号
-   name为规则名称
-   regex中可以编写规则，e和v都支持python正则表达式
-   message表示探测到之后需要输出信息，message支持`{{}}`模板语法，用于取出值
-   level表示输出的等级（字体颜色），目前包括：红色、绿色、蓝色。其中红色为警告，绿色比蓝色输出更重要

```json
"6": {
  "name": "PHP Version",
  "regexes": {
    "regex1": {
      "e": "^PHP Version$",
      "v": "."
    }
  },
  "message": "PHP版本为: {{self.rules['6']['regexes']['regex1']['v']}}",
  "level": "blue"
}
```

## PS

如果有无法正常解析phpinfo的情况，可以提issue发以下信息排查：

-   PHP版本
-   操作系统

目前测试了以下几个PHP版本都是可以正常解析的

-   7.3.10
-   5.4.45
-   5.6.40
-   7.4.5
