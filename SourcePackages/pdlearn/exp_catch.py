from functools import wraps
def exception_catcher(reserve_value=None,reserve_fun=None,fun_args=None,args_push=False):
    """ 
    用于捕捉异常的装饰器

    @param reserve_value: 出现异常时该方法的返回值
    @param reserve_fun: 出现异常时，执行备用方法
    @param fun_args: 备用方法的参数列表
    @param args_push: 是否合并 原方法参数 和 备用方法参数，如果为 TRUE 原方法参数在前，合并后传给备用方法
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                print("An exception occurred on "+func.__module__+"."+func.__name__+":"+str(e))
                if reserve_fun!=None:
                    if args_push==True:
                        new_args=args if args is not None else None
                        if new_args is None:
                            new_args=fun_args
                        elif fun_args is not None:
                            new_args+=fun_args
                        if new_args is not None:
                            return reserve_fun(*new_args)
                    if fun_args!=None:
                        return reserve_fun(*fun_args)
                    else:
                        return reserve_fun()
                if reserve_value!=None:
                    return reserve_value
        return wrapper
    return decorate