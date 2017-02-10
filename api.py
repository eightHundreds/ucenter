from config import Config
import hashlib
from urllib import parse,request
from urllib.parse import urljoin
from util import *
import sys
import xmltodict
import json
from functools import wraps
class UcenterError(Exception):
    def __init__(self,msg):
        self.msg=msg
        pass
    errors = ('Access denied for agent changed',
            'Module not found!',
            'Action not found!')

class baseapi():
    get_url=urljoin(Config.UC_API_URL,"index.php")
    def get_args(self, model, action,**param):
        """
        生成请求参数,未urlencode
        :param model:
        :param action:
        :param param: 额外参数
        :return:
        """
        param['agent'] = Util.MD5(Config.UC_AGENT)  # hashlib.md5(config.DEFAULT_AGENT.encode(config.UC_CHARSET))
        param['time'] = datetime.now().timestamp()
        encoded_param = parse.urlencode(param)# 转化成查询字符串
        authcode=Util.ucenter_aucode(encoded_param)

        #总的要发送的数据
        request_param = {
            "input": authcode,
            "m":model,
            "a": action,
            "release": Config.UC_CLIENTRELEASE,
            "appid": Config.UC_CLIENTID
        }

        return request_param

    def post(self,model,action,**param):
        """
        返回原生数据
        :param model:
        :param action:
        :param param:
        :return:
        """
        post_data = parse.urlencode(self.get_args(model, action, **param))
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': Config.UC_AGENT,
            'Cache-Control':'no-cache',
            'Cookie': '',
        }

        req=request.Request(self.get_url,headers=headers,data=post_data.encode(Config.UC_CHARSET))
        response = request.urlopen(req)
        result=response.read().decode()
        if result in UcenterError.errors:
            raise UcenterError(result)
        return result
    @staticmethod
    def decorator(func):
        """
        根据函数名获得请求url,并用传入参数发送请求
        :param func:
        :return:
        """
        @wraps(func)
        def wrapfunc(*args, **kwargs):
            method_name = func.__name__
            splited_method_name = method_name.split('_')
            module = splited_method_name[1]
            action = splited_method_name[2]
            params={}
            param_names=[i for i in list(func.__code__.co_varnames) \
                         if i not in list(func.__code__.co_names)]

            params=dict(zip(param_names,args))
            params.update(kwargs)
            self=params.pop('self')
            result=self.post(module, action, **params)
            return json.dumps(xmltodict.parse(result)["root"])
        return wrapfunc

class userapi(baseapi):

    def uc_get_user(self,username,isuid=0):#特殊的
        param = locals()
        param.pop('self')
        return self.post('user','get_user' , **param)

    def uc_user_register(self,username,password,email,questionid='',answer='',regip=''):
        """

        :param username:
        :param password:
        :param email:
        :param questionid:
        :param answer:
        :param regip:
        :return:
            0:返回用户 ID，表示用户注册成功
            -1:用户名不合法
            -2:包含不允许注册的词语
            -3:用户名已经存在
            -4:Email 格式有误
            -5:Email 不允许注册
            -6:该 Email 已经被注册
        """
        param=locals()
        param.pop('self')

        method_name = sys._getframe().f_code.co_name
        splited_method_name = method_name.split('_')
        module = splited_method_name[1]
        action=splited_method_name[2]

        return self.post(module,action,**param)

    @baseapi.decorator
    def uc_user_login(self,username,password,isuid=0,checkques=0,questionid=None,answer=None):
        pass

