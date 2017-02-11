# 前言

本来想打包发布的,但最后没做出完整的那就算了。

Ucenter是一个独立的用户中心，详情自行百度，谷歌。

多个应用可以连接到ucenter中，应用能用ucenter api（比如该项目client.py写的方法)请求Ucenter维护用户数据。ucenter 也会应某些事件自行发起对你应用的请求(所以自己的应用要处理ucenter发来的请求).



下面是个简单的介绍ucenter单点登录流程的时序图(github 的Markdown不支持时序图,想看自行找工具,然后复制粘贴即可)

``` sequence
participant website_A
participant website_B
Browser->Login:请求
Login->UCenter:发送用户名密码
UCenter->Login:校验成功返回数据
Login->UCenter:我要让其他网站\n知道我登入了
note right of UCenter:这步骤不是必须写的\n但不用这步怎么能叫单点
UCenter->Login:返回一组<script>标签
Login->Browser:发送script标签组
Browser->website_A:请求script中的链接
website_A->Browser:写入网站A的cookie,用于标示他已经登入了
Browser->website_B:请求script中的链接
website_B->Browser:写入网站B的cookie\n用于标示他已经登入了
```
# 使用

首先配置Client

``` python
from ucenter_api import Config
Config.UC_UCKEY=...
Config.UC_CLIENTID=...
Config.UC_API_URL=...
```

使用api

``` python
from ucenter_api import UserApi
api=UserApi()
api.uc_get_user('username')
```



**项目依赖**

- xmltodict



# 关于开发

ucenter 接口开发要用到的资料都在ucenter安装包中(开发文档,php版的ucenter api)

开发难点在于uc传输的加密算法,其实只要认真搬运也能轻松完成。

目前本项目，只完成了baseapi，和userapi，如果要添加其他的api可模仿着写。



ucenter的应用模块是先分`module` 再分`action` ,在对ucenter的请求中就有这两个参数,而且官方文档的函数名基本是按这样的规律组成的,比如`def uc_user_synlogin(self,uid)` 这个方法调用时会向ucenter发送一个请求,该请求带参数`module`,`action`,当然还有`uid`.大部分接口都是这样的规律



所以我在baseapi中写了个装饰器`def decorator(is_parse=True)`,使用举例:

``` python
@baseapi.decorator(False)
def uc_user_synlogin(self,uid):
    """
    同步登入,确保在后台设置该应用允许同步登入
    :param uid: 要同步登入的用户的uid
    :return:返回同步登入html代码,该代码需要在页面中渲染出来
    """
    pass
```

装饰器的参数表示是否解析响应为dict格式(有些响应结果只是个整数).就这样就完成了一个简单的接口.

但用这种方式写的接口返回数据格式并不好看,所以通常用在响应结果是个整数或偷懒的时候.





# 资料

该项目借鉴

- https://github.com/ghoulr/ucenter
- https://github.com/dozer47528/UCenter-API-For-DotNet (这里有几篇博文)
- 官方php代码







