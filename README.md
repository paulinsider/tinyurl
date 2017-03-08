# tinyurl
Usage: tinyurl.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        输入文件，以行为单位，目标url和别名之
                        间用空格隔开。
  -o OUTPUT, --output=OUTPUT
                        输出文件，以行为单位。
  -c, --check           检查所用别名是否被占用。
  -g, --generate        生成短地址，如果别名被占用则使用随机
                        生成的。