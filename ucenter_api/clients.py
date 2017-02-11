import inspect
import json
import sys
from functools import wraps
from urllib import parse,request
from urllib.parse import urljoin

import xmltodict

from ucenter_api.util import *
from .enums import *

class UcenterError(Exception):
    def __init__(self,msg):
        self.msg=msg
        pass
    errors = ('Access denied for agent changed',
            'Module not found!',
            'Action not found!')

class BaseApi():
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
    def decorator(is_parse=True):
        """
               根据函数名获得请求url,并用传入参数发送请求
               :param is_parse:最后是否解析xml,有些api只返回整数
               :return:
        """
        def wrapfunc(func):
            @wraps(func)
            def _wrapfunc(*args, **kwargs):
                import inspect
                method_name = func.__name__
                splited_method_name = method_name.split('_')
                module = splited_method_name[1]
                action = splited_method_name[2]
                params = {}
                param_names = [i for i in list(func.__code__.co_varnames) \
                               if i not in list(func.__code__.co_names)]

                #获得传入参数
                params = dict(zip(param_names, args))
                params.update(kwargs)
                self = params.pop('self')

                #添加带默认值但未手动设置的参数
                paramspec = inspect.getargspec(func)
                #获得所有默认参数键值对
                update_param={}
                if paramspec.defaults:
                    update_param=dict(zip(paramspec.args[-len(paramspec.defaults):], paramspec.defaults))
                #过滤已经手动赋值的键值对
                for i in params.keys():
                    if i in update_param:
                        del update_param[i]

                params.update(update_param)
                result = self.post(module, action, **params)
                if is_parse:
                    result=self.parse(result)
                return result
            return _wrapfunc
        return wrapfunc
    def parse(self,value):
        return xmltodict.parse(value)["root"]
    def parse_method_name(self,name):
        splited_method_name = name.split('_')
        module = splited_method_name[1]
        action = splited_method_name[2]
        return module,action

class UserApi(BaseApi):

    def uc_get_user(self,username,isuid=0):#特殊的
        """

        :param username:
        :param isuid:
        :return:
            {
                'email': '',
                'uid': '',
                'username': ''
            }
            如果用户不存在返回None
        """
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        param = {k:values[k] for k in args if k!='self'}

        result=self.post('user','get_user', **param)
        if result=='0':
            return None
        return Util.uc_dict2my_dict(['uid','username','email'],self.parse(result))

    def uc_user_register(self,username,password,email,questionid='',answer='',regip=''):
        """
        用户注册
        :param username:
        :param password:
        :param email:
        :param questionid:
        :param answer:
        :param regip:
        :return:
            注册成功:
            (UserEnum.SUCCESS,用户id)
            注册失败:
            (UserEnum,)
        """
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        param = {k: values[k] for k in args if k != 'self'}

        module,action=self.parse_method_name(frame.f_code.co_name)
        result=self.post(module,action,**param)
        if int(result)>0:
            return UserRegisterEnum.SUCCESS, result
        else:
            return (UserRegisterEnum(int(result)),)

    def uc_user_login(self,username,password,isuid=0,checkques=0,questionid=None,answer=None):
        """

        :param username:
        :param password:
        :param isuid:
        :param checkques:
        :param questionid:
        :param answer:
        :return:
        成功:
            (UserEnum.SUCCESS,result)
        失败
            (UserEnum,)


            result:
             {
                'psd': '',
                'email': '',
                'uid': '',
                'username': '',
                'isrepeat': ''//是否重名
            }
        """
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        param = {k: values[k] for k in args if k != 'self'}


        module, action = self.parse_method_name(frame.f_code.co_name)
        result = self.post(module, action, **param)
        parsed_result=Util.uc_dict2my_dict(['uid','username','psd','email','isrepeat'],self.parse(result))
        if int(parsed_result.get('uid'))>0:
            return (UserLoginResult.Success,parsed_result)
        else:
            return (UserLoginResult(int(parsed_result.get('uid'))),)
    @BaseApi.decorator(False)
    def uc_user_synlogin(self,uid):
        """
        同步登入,确保在后台设置该应用允许同步登入
        :param uid: 要同步登入的用户的uid
        :return:返回同步登入html代码,该代码需要在页面中渲染出来
        """
        pass

    @BaseApi.decorator(False)
    def uc_user_synlogout(self):
        pass
    def uc_user_checkemail(self,email):
        """
        检查 Email
        :param email:
        :return: UserEmailCheckResult
        """
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        param = {k: values[k] for k in args if k != 'self'}

        module, action = self.parse_method_name(frame.f_code.co_name)
        action='check_email'
        result = self.post(module, action, **param)
        return UserEmailCheckResult(int(result))
    def uc_user_checkname(self,username):
        """
        检查用户名
        :param username:
        :return: UserNameCheckResult
        """
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        param = {k: values[k] for k in args if k != 'self'}

        module, action = self.parse_method_name(frame.f_code.co_name)
        action='check_username'
        result = self.post(module, action, **param)
        return UserNameCheckResult(int(result))

class PmApi(BaseApi):
    @BaseApi.decorator(is_parse=False)
    def uc_pm_sendpm(self,fromuid ,msgto ,subject , message ,instantly=1,replypmid=0,isusername=0,type=0):
        pass

    @BaseApi.decorator()
    def uc_pm_ls(self, uid, page=1, pagesize=10, folder='inbox', filter='newpm', msglen=0):
        pass