import psycopg2

def get_db_connection(host: str, user: str, password: str, database: str) -> psycopg2.extensions.connection:
    """获取数据库连接"""
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def close_db_connection(conn: psycopg2.extensions.connection):
    """关闭数据库连接"""
    conn.close()