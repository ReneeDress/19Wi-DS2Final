# 2019-2020学年冬季学期《数据结构(2)》个人期末大作业

## 目录格式

```bash
├── P1
│		├── OnlineJudge纯享版
│		├── 含输出提示版
├── P2
│		├── Web版本
│		│			├── backend				// Django后端文件夹
│		│			├── example				// Django相关配置
│		│			├── frontend			// Vue.js前端文件夹
│		│			├── manage.py			// Django主要配置
│		│			├── db.sqlite3		// 未使用
│		│			├── database.txt	// 程序自动生成
│		│			├── sortedwl.txt 	// 程序自动生成
│		├── 命令行版本
│		│			├── Post					// 语料库文件夹
│		│			├── main.py				// 程序文件
│		│			├── database.txt	// 程序自动生成
│		│			├── sortedwl.txt 	// 程序自动生成
```



## P1

### OnlineJudge纯享版

OnlineJudge纯享版默认为11个样例自动执行，以回车分割。可在main.cpp中修改整数类型数据c，选择单个样例文件执行。直接执行main.cpp即可运行。

### 含输出提示版

含输出提示版为报告中截图版本。直接执行main.cpp即可运行。



## P2

### 开发环境

* Python 3.7.0
* Django 2.1
* Vue/cli 4.4.1

### Web版本

Web版本使用框架等如下：

* Vue.js
* Django
* Axios
* ElementUI

目录中，frontend为Vue.js相关开发文件；backend为Django App文件夹，主要函数、接口等在该目录下views.py；example文件夹与manage.py为Django相关配置文件等；并未使用自动生成的sqlite3数据库。

### 命令行版本

使用Python3.7.0配合os、re、requests模块。直接执行main.py即可运行。
