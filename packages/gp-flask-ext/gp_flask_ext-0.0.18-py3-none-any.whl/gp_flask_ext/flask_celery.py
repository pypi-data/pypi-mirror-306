import time
import json
from queue import Queue
from flask import Flask, Blueprint, request, render_template, Response
from celery import Celery, Task, shared_task, states
from celery.result import AsyncResult
from loguru import logger
from .celery_events import Monitor
from .nocodb import NocodbClient
from .celery_nocodb import NocodbStorage
from . import utils

def init_app(app: Flask, config=None) -> Celery:
    # Check if the provided config is valid
    if not (config is None or isinstance(config, dict)):
        raise ValueError("`config` must be an instance of dict or None")

    # Merge the default config with the provided config
    base_config = app.config.get("CELERY_CONFIG", {})
    if config:
        base_config.update(config)
    config = base_config

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(config)
    celery_app.set_default()
    
    ext_name = config.get("ext_name", "celery")
    app.extensions[ext_name] = celery_app
    logger.info("Initialized the Celery app")
    monitor = None
    nocodb = None

    nocodb_config = config.get("nocodb")
    storage = None
    if nocodb_config:
        nocodb = NocodbClient(**nocodb_config)
        storage = NocodbStorage(nocodb)
        app.extensions[f"{ext_name}_nocodb"] = storage


    # 监听事件
    if config.get("enable_events", True):
        nocodb = NocodbClient(**nocodb_config)
        monitor = Monitor(celery_app, nocodb)
        monitor.start()
        app.extensions[f"{ext_name}_monitor"] = monitor

    if config.pop("blueprint", True):
        # Register the blueprint
        bp_name = config.pop("blueprint_name", "celery")
        bp_url_prefix = config.pop("blueprint_url_prefix", "/celery")
        bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix, template_folder="templates")
        ins = celery_app.control.inspect()

        def safe_result(result):
            "returns json encodable result"
            try:
                json.dumps(result)
            except TypeError:
                return repr(result)
            return result
        
        def _inspect_object_2_list(o):
            ret = []
            if o:
                _id = 0
                for key, value in o.items():
                    ret.append({
                        "id": _id,
                        "worker": key,
                        "value" : value
                    })
                    _id += 1
            return ret
        
        @bp.route("/")
        def index():
            return render_template("celery/index.html")
        
        @bp.route("/inspect")
        def inspect():
            return render_template("celery/inspect.html")
        
        @bp.route("/tasks/results")
        def tasks_results():
            return render_template("celery/result.html")
        
        @bp.route("/inspect/stats")
        def inspect_stats():
            o = ins.stats()      # 返回值是字典，键是worker名字，值是状态, dict类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/active")
        def inspect_active():
            o = ins.active()            # 返回值是字典，键是worker名字，值是当前活动任务列表, list类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/queues")
        def inspect_queues():
            o = ins.active_queues()     # 返回值是字典，键是worker名字，值是队列列表, list类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/memsample")
        def inspect_memsample():
            o = ins.memsample()         # 返回值是字典，键是worker名字，值是内存占用情况, dict类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/conf")
        def inspect_conf():
            o = ins.conf()              # 返回值是字典，键是worker名字，值是配置信息, dict类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/clock")
        def inspect_clock():
            o = ins.clock()             # 返回值是字典，键是worker名字，值是时钟信息, dict类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/registered")
        def inspect_registered():
            o = ins.registered()        # 返回值是字典，键是worker名字，值是已注册的任务列表, list类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/report")
        def inspect_report():
            o = ins.report()            # 返回值是字典，键是worker名字，值是报告信息, dict类型
            return _inspect_object_2_list(o)
        
        @bp.route("/inspect/ping")
        def inspect_ping():
            o = ins.ping()              # 返回值是字典，键是worker名字，值是PING响应信息, dict类型
            return _inspect_object_2_list(o)

        @bp.route("/tasks")
        def tasks():
            if not storage: return "No storage", 500
            limit = int(request.args.get("limit", 1000))
            view_id = request.args.get("view_id")
            return storage.list_tasks(limit=limit, view_id=view_id)
            # return {"tasks": [task.name for task in celery_app.tasks.values() if not task.name.startswith("celery.")]}

        @bp.route("/tasks/states")
        def state():
            return [state for state in states.__all__]


        @bp.route("/tasks/send", methods=["POST"])
        def send():
            data = request.json
            if not data:
                return {"error": "No data provided"}, 400

            taskname = data.get("name")
            if not taskname:
                return {"error": "No task name provided"}, 400
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            queue = data.get("queue")
            countdown = int(data.get("countdown", 0))
            eta = data.get("eta")

            options = {}        # celery send_task 调用可选项
            if queue: options['queue'] = queue
            if countdown: options['countdown'] = countdown
            if eta: 
                options['eta'] = eta
                options.pop('countdown')    # eta 优先级高于 countdown, 
                
            result:AsyncResult = celery_app.send_task(
                taskname, args=args, kwargs=kwargs, **options)
            task_info = {
                "task_id": result.task_id, 
                "name": taskname, 
                "state": result.state,
                "args": args,
                "kwargs": kwargs,
                "queue": queue,
                "timestamp": time.time(),
            }
            if monitor:
                monitor.add_new_result_to_nocodb(task_info)
            return task_info
        
        @bp.route("/results")
        def results():
            if not storage: return "No storage", 500
            name = request.args.get("name")
            state = request.args.get("state")
            offset = int(request.args.get("offset", 0))
            limit = int(request.args.get("limit", 25))
            view_id = request.args.get("view_id")
            return storage.list_results(name=name, state=state, offset=offset, limit=limit, view_id=view_id)

        @bp.route("/results/<task_id>")
        def result(task_id:str):
            if not storage: return "No storage", 500
            resp = storage.get_result(task_id)
            if not resp: return "Not found", 404
            return resp

        @bp.route("/queues")
        def queues():
            if not storage: return "No storage", 500
            limit = int(request.args.get("limit", 1000))
            view_id = request.args.get("view_id")
            return storage.list_queues(limit=limit, view_id=view_id)        
        
        @bp.route("/workers")
        def workers():
            if not storage: return "No storage", 500
            limit = int(request.args.get("limit", 1000))
            view_id = request.args.get("view_id")
            return storage.list_workers(limit=limit, view_id=view_id)
        
        @bp.route("/upload.html", methods=["GET"])
        def upload_html():
            return render_template("celery/upload.html")
        
        @bp.route("/upload", methods=["POST"])
        def upload():
            if not storage: return "No storage", 500
            files_to_upload  = []
            for key, values in request.files.to_dict(flat=False).items():
                tuples = [('files', (v.filename, v.stream, v.mimetype)) for v in values]
                files_to_upload.extend(tuples)

            logger.info("Upload files_to_upload {}", len(files_to_upload))
            if len(files_to_upload) == 0: return "No files to upload", 400
            resp = storage.upload(files_to_upload)
            return resp
        
        @bp.route('/logs', methods=["GET"])
        def logs():
            task_id = request.args.get("task_id")
            if task_id is None: return "task_id is required", 400
            if monitor is None: return "No monitor", 500
            def generate(task_id, monitor: Monitor):
                try:
                    while True:
                        queue : Queue = monitor.get_log_queue(task_id)
                        if queue is None:
                            raise Exception("No queue")
                        while not queue.empty():
                            message = queue.get()
                            if message is None:
                                yield "\n\n"
                                raise Exception("Cache Done")
                            yield f"data: {message}"
                        yield "\n\n"
                        message = queue.get()
                        if message is None:
                            raise Exception("Done")
                        yield f"data: {message}\n\n"
                except Exception as e:
                    logger.warning(e)
                    yield "data: [DONE]\n\n"
                    time.sleep(1)   # 给客户端一个收到[DONE]的处理时间后再返回
                    return

            cors = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'x-requested-with'
            }
            return Response(generate(task_id, monitor), content_type='text/event-stream', headers=cors)

        @bp.route("/test")
        def test():
            return {
                "broker": celery_app.conf.broker_url,
                "result_backend": celery_app.conf.result_backend,
            }
        
        @bp.route("/test/debounce")
        def test_debounce():
            return utils.debounce_info()

        app.register_blueprint(bp)
        logger.info("Registered the Celery blueprint")

    return celery_app
