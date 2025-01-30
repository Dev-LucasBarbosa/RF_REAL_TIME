import psycopg2

conn = psycopg2.connect(database = "postgres",
                        user = "postgres",
                        host = 'localhost',
                        password = "postgres",
                        port = 5433)
