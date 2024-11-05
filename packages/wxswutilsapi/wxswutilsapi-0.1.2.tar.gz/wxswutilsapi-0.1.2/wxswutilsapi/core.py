import sqlite3

class db:
    def __init__(self, database_name):
        self.database_name = database_name
        

    def init_db(self,table_definitions):
        """
        初始化数据库，根据传入的表定义参数创建表结构。

        :param table_definitions: 包含表定义信息的列表，每个元素是一个字典，格式如下：
            {
                "table": "表名",
                "fields": [
                    {
                        "field": "字段名",
                        "isNULL": 是否允许为空（True/False）
                    },
                   ...
                ],
                "FOREIGNKEY": [
                    {
                        "foreign_table": "关联的外部表名",
                        "local_field": "本表中关联的字段名",
                        "foreign_field": "外部表中关联的字段名"
                    },
                   ...
                ]
            }
        """
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()

                for table_def in table_definitions:
                    table_name = table_def["table"]
                    fields = table_def["fields"]
                    foreign_keys = table_def["FOREIGNKEY"]

                    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

                    for field in fields:
                        field_name = field["field"]
                        is_null = "NULL" if field["isNULL"] else "NOT NULL"
                        create_table_query += f"{field_name} TEXT {is_null}, "

                    if foreign_keys:
                        for fk in foreign_keys:
                            foreign_table = fk["foreign_table"]
                            local_field = fk["local_field"]
                            foreign_field = fk["foreign_field"]
                            create_table_query += f"FOREIGN KEY ({local_field}) REFERENCES {foreign_table}({foreign_field}) ON DELETE CASCADE, "

                    create_table_query = create_table_query.rstrip(", ") + ")"

                    cursor.execute(create_table_query)

                conn.commit()
        except sqlite3.Error as e:
            print(f"数据库初始化出错: {e}")

    def fetch_all_by(table, params, page=None, fields=None, noTotal=False):
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()

            # 提取并处理排序参数
            _order = params.pop('_order', None)
            _by = params.pop('_by', None)
            if isinstance(_order, str):
                _order = [o.strip() for o in _order.split(',')]
            if isinstance(_by, str):
                _by = [b.strip() for b in _by.split(',')]

            if _by and _order and len(_order) != len(_by):
                raise ValueError("Length of _order and _by must be the same.")

            # 构建 WHERE 子句和查询参数
            where_clauses = []
            query_params = []
            _params = params.copy()
            if '_start' in params:
                del _params['_start']
            if '_count' in params:
                del _params['_count']
            for key, value in _params.items():
                if key.startswith('%'):
                    actual_key = key.lstrip('%')
                    where_clauses.append(f'{actual_key} LIKE ?')
                    query_params.append(f'%{value}%')
                elif key == 'startTime':
                    where_clauses.append('time >= ?')
                    query_params.append(value)
                elif key == 'endTime':
                    where_clauses.append('time <= ?')
                    query_params.append(value)
                else:
                    where_clauses.append(f'{key} = ?')
                    query_params.append(value)

            # 如果 noTotal 为 False，则查询总条数
            total = 0  # 默认值为0
            if not noTotal:
                count_query = f'SELECT COUNT(*) as __total FROM {table}'
                if where_clauses:
                    count_query += ' WHERE ' + ' AND '.join(where_clauses)
                print(f"fetch_all_by SQL (count): {count_query}")
                print(f"fetch_all_by VALUE (count): {str(query_params)}")
                cursor.execute(count_query, query_params)
                total = cursor.fetchone()['__total']

            # 构建数据查询
            if fields:
                # 如果提供了字段参数，则只查询指定字段
                fields_str = ', '.join(fields)
            else:
                # 否则查询所有字段
                fields_str = '*'

            query = f'SELECT {fields_str} FROM {table}'
            if where_clauses:
                query += ' WHERE ' + ' AND '.join(where_clauses)

            if _by and _order:
                order_by_clause = ', '.join([f'{field} {order}' for field, order in zip(_by, _order)])
                query += f' ORDER BY {order_by_clause}'

            if page and 'LIMIT' in page and 'OFFSET' in page:
                query += f' LIMIT {page["LIMIT"]} OFFSET {page["OFFSET"]}'

            print(f"fetch_all_by SQL (data): {query}")
            print(f"fetch_all_by VALUE (data): {str(query_params)}")
            cursor.execute(query, query_params)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                row_dict = {field: row[field] for field in row.keys()}
                result.append(row_dict)

            conn.close()

            return result, total
        except Exception as e:
            print(f"Unexpected error in fetch_all_by: {e}")

    def fetch_data_count(self,table, field, conditions=None):
        try:
            """
            从指定的表中查询指定字段的计数信息，并按该字段分组。

            :param table: 表名
            :param field: 字段名
            :param conditions: 一个包含查询条件的字典，键为列名，值为对应的过滤值
            :return: 一个包含字典的列表，每个字典包含 'field' 和 'count' 两个键
            """
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()

            # 构建查询条件
            where_clause = ""
            params = []

            if conditions:
                where_conditions = []
                for key, value in conditions.items():
                    where_conditions.append(f"{key} = ?")
                    params.append(value)
                where_clause = " WHERE " + " AND ".join(where_conditions)

            # 构建查询语句
            query = f'''
                SELECT {field}, COUNT(*) as count
                FROM {table}
                {where_clause}
                GROUP BY {field}
            '''
            print(f"fetch_data_count SQL: {query}")
            print(f"fetch_data_count VALUE: {str(params)}")
            # 执行查询获取数据
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # 将结果转换为列表
            result_list = [{field: row[field], 'count': row['count']} for row in rows]

            # 关闭数据库连接
            conn.close()

            return result_list
        except Exception as e:
            print(f"Unexpected error in fetch_data_count: {e}")