import sqlite3


def init_db(table_definitions,DATABASE):
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
        with sqlite3.connect(DATABASE) as conn:
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