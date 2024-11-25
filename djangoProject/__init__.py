import pymysql
pymysql.version_info = (2, 2, 6, "final", 0)  # 模拟更高版本
pymysql.install_as_MySQLdb()
