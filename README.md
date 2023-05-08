推荐使用 pycharm 打开项目，因为已经内置 django 程序无需再在环境中下载

# Django方面

1. 建表与运行

```
python manage.py makemigrations // 记录所有在 models.py 文件中的所有变动

python manage.py migrate app01 // 将以上记录的新变动作用到数据库中

python manage.py createsuperuser // 创建管理员

// 进入 backend 文件夹，依次执行：
pip install pandas
pip install openpyxl

python manage.py runserver 127.0.0.1:8000 // 启动程序

```


# Vue方面

1. 运行

```
yarn install // 下载依赖

yarn serve // 运行程序

// 在浏览器输入相应端口
```
