import time
from .nocodb import NocodbClient
from .celery_utils import get_tasks_info
from loguru import logger


class NocodbStorage:
    nocodb : NocodbClient
    
    def __init__(self, nocodb) -> None:
        self.nocodb = nocodb
        self.tables = self.nocodb.get_tables()
        self.task_table = self.tables["Task"]
        self.task_view = self.nocodb.get_views(self.task_table)
        self.worker_table = self.tables["Worker"]
        self.worker_view = self.nocodb.get_views(self.worker_table)
        self.queue_table = self.tables["Queue"]
        self.queue_view = self.nocodb.get_views(self.queue_table)
        self.result_table = self.tables["Result"]
        self.upload_table = self.tables["Upload"]
        self.worker_link_columns = self.nocodb.get_table_links(self.worker_table)
        self._ids_cache = {}    # key: table_id, value: ids
        logger.debug("init worker_link_columns: {}", self.worker_link_columns)

    def worker_link_task(self, worker_id, ids, relink=False):
        woker_task_link_id = self.worker_link_columns.get("Tasks")
        logger.info("woker_task_link_id: {}", woker_task_link_id)
        if relink:
            task_ids = self._ids_cache.get(self.task_table)
            self.nocodb.unlink(self.worker_table, woker_task_link_id, worker_id, task_ids)
        return self.nocodb.link(self.worker_table, woker_task_link_id, worker_id, ids)
    
    def worker_link_queue(self, worker_id, ids, relink=False):
        worker_queue_link_id = self.worker_link_columns.get("Queues")
        logger.info("worker_queue_link_id: {}", worker_queue_link_id)
        if relink:
            queue_ids = self._ids_cache.get(self.queue_table)
            self.nocodb.unlink(self.worker_table, worker_queue_link_id, worker_id, queue_ids)
        return self.nocodb.link(self.worker_table, worker_queue_link_id, worker_id, ids)

    def add_queues(self, row):
        return self.add_or_update(self.queue_table, row, key="name")
        
    def add_task(self, row):
        return self.add_or_update(self.task_table, row, key="name")
    
    def add_worker(self, row):
        return self.add_or_update(self.worker_table, row, key="hostname")
    
    def add_or_update(self, table_id, items, key=None):
        if key is None:
            return self.nocodb.add(table_id, items)
        if len(items) > 1000:
            raise ValueError("items too long")
        r = self.nocodb.get(table_id, fields=["Id", key], limit=1000)
        ids = {row[key]: row["Id"] for row in r["list"]}
        self._ids_cache[table_id] = r["list"]
        to_add = []
        to_update = []
        for item in items:
            item_id = ids.get(item[key])
            if item_id is None:
                logger.debug("add item: {}", item)
                to_add.append(item)
            else:
                logger.debug("update item: {}", item)
                to_update.append({"Id": item_id, **item})
        r = []
        if to_add:
            r1 = self.nocodb.add(table_id, to_add)
            r.extend(r1)
        if to_update:
            r2 = self.nocodb.update(table_id, to_update)
            r.extend(r2)
        return r

    
    def register_tasks(self, worker_id, queues):
        tasks = get_tasks_info()
        # 动态获取当前worker注册的所有任务
        r = self.add_worker([{"hostname": worker_id}])
        worker_row_id = r[0]["Id"]
        logger.debug("add_worker: {}", worker_row_id)
        
        r = self.add_task(tasks)
        logger.debug("add_task: {}", r)
        time.sleep(0.5)

        r = self.worker_link_task(worker_row_id, r, relink=True)
        
        logger.debug("worker_link_task: {}", r)
        time.sleep(0.5)

        r = self.add_queues([ {"name": q} for q in queues])
        logger.info("add_queues: {}", r)

        r = self.worker_link_queue(worker_row_id, r, relink=True)
        logger.info("worker_link_queue: {}", r)

    def list_results(self, name=None, state=None, offset=0, limit=25, view_id=None):
        """
        查询任务列表
        """
        where = []
        if name: where.append(f"(name,eq,{name})")
        if state: where.append(f"(state,eq,{state})")
        # ref: https://data-apis-v2.nocodb.com/#tag/Table-Records/operation/db-data-table-row-list
        params = {
            "where": "~and".join(where),
            "sort": "-timestamp"        # 默认倒序
        } 
        logger.debug("querying {}...", params)
        return self.nocodb.get(self.result_table, params=params, offset=offset, limit=limit, view_id=view_id)
    
    def get_result(self, task_id):
        params = {
            "where": f"(task_id,eq,{task_id})",
        }
        resp = self.nocodb.get(self.result_table, params=params, limit=1)
        if "list" in resp and len(resp["list"]) > 0: return resp["list"][0]
        else: return None

    
    def list_workers(self, limit=1000, view_id=None):
        """
        查询worker列表
        """
        if not view_id: view_id = self.worker_view.get("简单", None)
        workers = self.nocodb.get(self.worker_table, limit=limit, view_id=view_id)
        return workers
    
    def list_tasks(self, limit=1000, view_id=None):
        """
        查询任务列表
        """
        if not view_id: view_id = self.task_view.get("简单", None)
        tasks = self.nocodb.get(self.task_table, limit=limit, view_id=view_id)
        return tasks
    
    def list_queues(self, limit=1000, view_id=None):
        """
        查询队列列表
        """
        if not view_id: view_id = self.queue_view.get("简单", None)
        queues = self.nocodb.get(self.queue_table, limit=limit, view_id=view_id)
        return queues

    def upload(self, files):
        resp = self.nocodb.upload_files(files)
        rows = []
        for item in resp:
            row = {
                "file": [item],     # 附件必须是list
                "size": item["size"],
                "title": item["title"],
                "path": item["path"],
                "mimetype": item["mimetype"],
            }
            rows.append(row)
        self.nocodb.add(self.upload_table, rows)
        return resp
    
    def get_upload_file(self, path):
       return self.nocodb.get_upload_file(path)
    