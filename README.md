# Django方面

进入 backend 文件夹，按以下顺序执行命令：

1. 安装 corsheaders

```
pip3 install django-cors-headers
```

2. 找到主目录下settings.py

```
INSTALLED_APPS = [
    ···
    'corsheaders',
    ···
]
```

3. 同样在settings.py文件中

```
MIDDLEWARE = [
    ···
    'corsheaders.middleware.CorsMiddleware',  # 解决跨域问题，注意与common.CommonMiddleware的顺序
    'django.middleware.common.CommonMiddleware',
    ···
]
// 注意：'corsheaders.middleware.CorsMiddleware' 要放在最前面
```

4. 还是在settings.py文件中

```
# 增加跨域忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# 允许所有方法
CORS_ALLOW_METHODS = ('*')
# 允许所有请求头
CORS_ALLOW_HEADERS = ('*')
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True 
```

如果想更安全或者是更加有针对性一点的话，可以就添加白名单：

```
CORS_ORIGIN_WHITELIST = (
	'localhost:8080',
)
\\ 凡是出现在白名单里的域名都可以访问后端。
```

5. 建表与运行

```
python manage.py makemigrations // 记录所有在 models.py 文件中的所有变动

python manage.py migrate app01 // 将以上记录的新变动作用到数据库中

python manage.py createsuperuser // 创建管理员

python manage.py runserver 127.0.0.1:8000 // 启动程序，后面的 ip 和 端口可以自己设置，不过为了前后联调暂设如此
```


# Vue方面

1.vue这边主要就用一个axios，有了他就可以进行跨域访问后端的系统了
首先就是要下载，使用npm下载：

```
npm install axios
```

2. 在项目目录的src里面的main.js引入axios以及挂载axios

```
import axios from 'axios'
//挂载axios
Vue.prototype.$http = axios
//访问根路径
axios.defaults.baseURL = "http://127.0.0.1:1101"
```

3. 运行

```
yarn install // 下载依赖

yarn serve // 运行程序
```