# 百度图片spider

为分类识别提供数据

- 只支持chrome (谷歌浏览器)

![效果展示](./readme_img/output.gif)

## 浏览器不能自动打开
- 查看谷歌浏览器版本
- 下载对应的驱动放在chromedriver文件夹中

## 使用方法
- 使用Python3
- 安装requirements.txt中的依赖库(pip install -r requirements)
- 在keywords.txt中输入要搜索的图片的关键词 一行一个
- 运行main.py即可

## 说明
 - 但关键词图片下载数量
默认刷图片时会向下翻页60次,网络较好能获得1300多张(单关键词)图片
修改: collect_links.py 的71行  for i in range(60):
-  使用了多进程开窗口 默认进程数 n_threads=4  main.py 16 行
- 存储命名: 统一放置在 download 中, 自动为每个关键词建立目录,图片保存在对应目录中名字为关键词加 索引

## 备注
此百度图片爬虫 是从YoongiKim 的 谷歌，Naver多进程图像网络爬虫（Selenium）
中精简修改而来的, 因为 他的AutoCrawler 在中国不能使用
https://github.com/YoongiKim/AutoCrawler