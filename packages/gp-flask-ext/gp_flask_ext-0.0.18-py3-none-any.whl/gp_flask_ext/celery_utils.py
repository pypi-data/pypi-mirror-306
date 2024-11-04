import inspect
from celery import Celery, current_app

def get_default_value(param_type):
    """根据参数类型生成默认值"""
    if param_type == 'int':
        return 0
    elif param_type == 'float':
        return 0.0
    elif param_type == 'str':
        return ''
    elif param_type == 'bool':
        return False
    elif param_type == 'list':
        return []
    elif param_type == 'dict':
        return {}
    else:
        return None  # 无法识别的类型，设为 None

def get_task_signature(task):
    sig = inspect.signature(task)
    params = {}
    default_kwargs = {}

    for name, param in sig.parameters.items():
        # 获取参数类型
        if param.annotation != inspect.Parameter.empty:
            if hasattr(param.annotation, '__name__'):
                param_type = param.annotation.__name__
            else:
                param_type = str(param.annotation)
        else:
            param_type = None

        # 根据类型生成默认值，如果没有默认值，则使用类型推断的默认值
        if param.default != inspect.Parameter.empty:
            default_value = param.default
        else:
            default_value = get_default_value(param_type)

        params[name] = {
            'default': default_value,
            'kind': str(param.kind),
            'type': param_type
        }
        
        # 将默认值放入 kwargs
        default_kwargs[name] = default_value

    return {'signature': params, 'kwargs': default_kwargs}

def get_tasks_info():
    """获取所有任务的信息，包括参数、默认值等"""
    tasks_info = []
    for task_name, task in current_app.tasks.items():
        if task_name.startswith('celery.'):  # 跳过系统任务
            continue
        # 获取任务签名
        task_signature = get_task_signature(task)
        tasks_info.append({
            'name': task_name,
            'signature': task_signature["signature"],
            'kwargs': task_signature["kwargs"],
            'doc': task.__doc__,
            'task_name': task.__name__,
        })
    return tasks_info