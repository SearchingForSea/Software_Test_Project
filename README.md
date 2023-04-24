# Django����

���� backend �ļ��У�������˳��ִ�����

1. ��װ corsheaders

```
pip3 install django-cors-headers
```

2. �ҵ���Ŀ¼��settings.py

```
INSTALLED_APPS = [
    ������
    'corsheaders',
    ������
]
```

3. ͬ����settings.py�ļ���

```
MIDDLEWARE = [
    ������
    'corsheaders.middleware.CorsMiddleware',  # ����������⣬ע����common.CommonMiddleware��˳��
    'django.middleware.common.CommonMiddleware',
    ������
]
// ע�⣺'corsheaders.middleware.CorsMiddleware' Ҫ������ǰ��
```

4. ������settings.py�ļ���

```
# ���ӿ������
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# �������з���
CORS_ALLOW_METHODS = ('*')
# ������������ͷ
CORS_ALLOW_HEADERS = ('*')
# ����Я��cookie
CORS_ALLOW_CREDENTIALS = True 
```

��������ȫ�����Ǹ����������һ��Ļ������Ծ���Ӱ�������

```
CORS_ORIGIN_WHITELIST = (
	'localhost:8080',
)
\\ ���ǳ����ڰ�����������������Է��ʺ�ˡ�
```

5. ����������

```
python manage.py makemigrations // ��¼������ models.py �ļ��е����б䶯

python manage.py migrate app01 // �����ϼ�¼���±䶯���õ����ݿ���

python manage.py createsuperuser // ��������Ա

python manage.py runserver 127.0.0.1:8000 // �������򣬺���� ip �� �˿ڿ����Լ����ã�����Ϊ��ǰ�������������
```


# Vue����

1.vue�����Ҫ����һ��axios���������Ϳ��Խ��п�����ʺ�˵�ϵͳ��
���Ⱦ���Ҫ���أ�ʹ��npm���أ�

```
npm install axios
```

2. ����ĿĿ¼��src�����main.js����axios�Լ�����axios

```
import axios from 'axios'
//����axios
Vue.prototype.$http = axios
//���ʸ�·��
axios.defaults.baseURL = "http://127.0.0.1:1101"
```

3. ����

```
yarn install // ��������

yarn serve // ���г���
```