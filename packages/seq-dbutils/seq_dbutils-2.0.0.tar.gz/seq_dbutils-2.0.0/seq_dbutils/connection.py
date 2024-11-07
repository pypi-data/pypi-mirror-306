import logging

import sqlalchemy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Connection:

    def __init__(self, user, pwd, host, db, connector_type='mysqlconnector'):
        assert isinstance(user, str)
        assert isinstance(pwd, str)
        assert isinstance(host, str)
        assert isinstance(db, str)
        self.user = user
        self.pwd = pwd
        self.host = host
        self.db = db
        self.connector_type = connector_type

    def create_sql_engine(self, sql_logging=False):
        logging.info(f'Connecting to {self.db} on host {self.host}')
        conn_str = f'mysql+{self.connector_type}://{self.user}:{self.pwd}@{self.host}/{self.db}'
        sql_engine = sqlalchemy.create_engine(conn_str, echo=sql_logging)
        return sql_engine
