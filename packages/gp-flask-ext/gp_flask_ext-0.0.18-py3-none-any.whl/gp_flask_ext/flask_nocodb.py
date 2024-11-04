from flask import Flask, Blueprint, request, render_template
from loguru import logger
from .nocodb import NocodbClient

full_table_fields = {'id', 'source_id', 'base_id', 'table_name', 'title', 'type', 'meta', 'schema', 'enabled', 'mm', 'tags', 'pinned', 'deleted', 'order', 'created_at', 'updated_at', 'description', 'fk_workspace_id', 'views', 'columns', 'columnsById'}
create_table_fields = {'table_name', 'title', 'description', 'columns'}

full_column_fields = {'id', 'source_id', 'base_id', 'fk_model_id', 'title', 'column_name', 'uidt', 'dt', 'np', 'ns', 'clen', 'cop', 'pk', 'pv', 'rqd', 'un', 'ct', 'ai', 'unique', 'cdf', 'cc', 'csn', 'dtx', 'dtxp', 'dtxs', 'au', 'validate', 'virtual', 'deleted', 'system', 'order', 'created_at', 'updated_at', 'meta', 'description', 'fk_workspace_id'}
create_column_fields = {'title', 'uidt', 'description', 'cdf', 'pv', 'rqd', 'column_name'}

def init_app(app: Flask, config=None):
    # Check if the provided config is valid
    if not (config is None or isinstance(config, dict)):
        raise ValueError("`config` must be an instance of dict or None")

    # Merge the default config with the provided config
    base_config = app.config.get("NOCODB_CONFIG", {})
    if config:
        base_config.update(config)
    config = base_config

    # Initialize the NocodbClient
    nocodb_client = NocodbClient(
        **config
    )

    # Add the NocodbClient to the app context
    ext_name = config.get("ext_name", "nocodb")
    app.extensions[ext_name] = nocodb_client
    logger.info("Initialized the NocodbClient")

    if config.pop("blueprint", True):
        # Register the blueprint
        bp_name = base_config.pop("blueprint_name", "nocodb")
        bp_url_prefix = base_config.pop("blueprint_url_prefix", "/nocodb")
        nocodb_bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix, template_folder="templates")

        @nocodb_bp.route("/projects")
        def projects():
            return nocodb_client.get_projects()

        @nocodb_bp.route("/tables")
        def tables():
            return nocodb_client.get_tables()
        
        @nocodb_bp.route("/tables/<table_id>")
        def get(table_id):
            return nocodb_client.get(table_id)
        
        @nocodb_bp.route("/")
        def index():
            return render_template("nocodb/index.html")
        
        @nocodb_bp.route("/table/create", methods=["POST"])
        def table_create():
            meta = request.json.get("meta")
            new_columns = []
            for column in meta["columns"]:
                uidt = column.get("uidt")
                if uidt in ["Links", "LinkToAnotherRecord"]:
                    continue
                # if uidt == "Formula":
                #     continue
                if uidt == "ForeignKey":
                    continue
                new_columns.append(column)
            meta["columns"] = new_columns
            return nocodb_client.create_table(meta)
        
        @nocodb_bp.route("/table/dump", methods=["POST"])
        def table_dump():
            table_id = request.json.get("table_id")
            meta = nocodb_client.get_table_metadata(table_id)
           
            # clear table fields
            for field in full_table_fields - create_table_fields:
                if field in meta: meta.pop(field)
            new_columns = []
            for column in meta["columns"]:
                is_system = column.get("system", False)
                if is_system:
                    continue
                uidt = column.get("uidt")
                if uidt in ["Links", "LinkToAnotherRecord"]:
                    # 处理 Links 类型
                    colOptions = column.get("colOptions")
                    new_colOptions = {
                        "type" : colOptions.get("type"),
                        "fk_child_column_id": colOptions.get("fk_child_column_id"),
                        "fk_parent_column_id": colOptions.get("fk_parent_column_id"),
                    }
                    column["colOptions"] = new_colOptions
                    
                if uidt == "Formula":
                    # 处理 Formula 类型
                    formula_raw = column["colOptions"]["formula_raw"]
                    column['formula_raw'] = formula_raw
                    column['formula'] = formula_raw
                    column.pop("colOptions")

                if uidt == "ForeignKey":
                    # 处理 ForeignKey 类型, 直接跳过
                    pass 
                
                for field in full_column_fields - create_column_fields:
                    if field in column: column.pop(field)
                    
                new_columns.append(column)
            meta["columns"] = new_columns
            return meta

        app.register_blueprint(nocodb_bp)
        logger.info("Registered the Nocodb blueprint")

