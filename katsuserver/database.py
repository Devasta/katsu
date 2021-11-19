from contextlib import contextmanager
import psycopg2.pool
import psycopg2.extras
import psycopg2.extensions
import os


class db:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app
        self.dbpool = psycopg2.pool.ThreadedConnectionPool(host    = app.config['DB_HOST'],
                                                           port=app.config['DB_PORT'],
                                                           dbname=app.config['DB_NAME'],
                                                           user=app.config['DB_USER'],
                                                           password=app.config['DB_PASSWORD'],
                                                           maxconn=app.config['DB_MAX_CONNECTIONS'],
                                                           minconn=app.config['DB_MIN_CONNECTIONS'])
        self.schema = app.config['DB_SCHEMA']
        self.create_DB()

    def create_DB(self):
        conn = self.dbpool.getconn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                select exists(select nspname from pg_namespace where nspname = lower(%(schema)s) ) as exists
            """, {'schema': self.schema})
            result = cur.fetchone()
            if result['exists']:
                return
            else:
                cur.execute("""CREATE SCHEMA IF NOT EXISTS %(schema)s """,
                            {'schema': psycopg2.extensions.AsIs(self.schema)}
                            )
                cur.execute("""SET search_path TO %(schema)s """,
                            {'schema': psycopg2.extensions.AsIs(self.schema)}
                            )

                def run_sql_files(directory):
                    for file in os.listdir(directory):
                        with open(file) as f:
                            sql = f.read()
                            cur.execute(sql)

                run_sql_files((os.path.dirname(__file__) + '/../../katsudb/tables/'))
                #run_sql_files((os.path.dirname(__file__) + '/../../katsudb/Views.sql'))
                #run_sql_files((os.path.dirname(__file__) + '/../../katsudb/Functions.sql'))
                #run_sql_files((os.path.dirname(__file__) + '/../../katsudb/Records.sql'))
                #run_sql_files((os.path.dirname(__file__) + '/../../katsudb/SEPABICs.sql'))

        conn.commit()
        return

    def delete_DB(self):
        '''
            Have to be VERY careful with this one! :)
        '''
        conn = self.dbpool.getconn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                        """
                        DROP SCHEMA %(schema)s CASCADE
                        """, {'schema': psycopg2.extensions.AsIs(self.schema)}
                        )
        conn.commit()
        self.dbpool.closeall()

    @contextmanager
    def db_cursor(self):
        # We are returning everything as dictionaries. Less than ideal in some cases, but prefer consistency.
        conn = self.dbpool.getconn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                            SET search_path TO %(schema)s
                            """, {'schema': psycopg2.extensions.AsIs(self.schema)})
                yield cur
                conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            if e.pgcode == '23503':  # Foreign Key Violation
                raise KeyError(e.diag.message_primary)
            elif e.pgcode == '23505':  # Duplicate Key Error
                raise KeyError(e.diag.message_primary)
            elif e.pgcode == '23514': # Check constraint fail
                raise ValueError(e.diag.message_primary)
            elif e.pgcode == 'P0001':  # Missing Key Error
                raise ValueError(e.diag.message_primary)
            elif e.pgcode == 'P0002':  # Missing Key Error
                raise KeyError(e.diag.message_primary)
            else:
                raise Exception(e.pgcode + ' ' + e.diag.message_primary)
        except psycopg2.IntegrityError as e:
            conn.rollback()
            raise ValueError(e.pgcode + ' ' + e.diag.message_primary)
        except Exception:
            conn.rollback()
            raise
        finally:
            self.dbpool.putconn(conn)
