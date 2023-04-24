
## 运行

进入 backend 文件夹，按以下顺序执行命令：

```
python manage.py makemigrations // 记录所有在 models.py 文件中的所有变动

python manage.py migrate app01 // 将以上记录的新变动作用到数据库中

python manage.py createsuperuser // 创建管理员

python manage.py runserver 127.0.0.1:8000 // 启动程序，后面的 ip 和 端口可以自己设置，不过为了前后联调暂设如此
```


进入 frontend 文件夹，按以下顺序执行命令：

```
yarn install // 下载依赖

yarn serve // 运行程序
```
