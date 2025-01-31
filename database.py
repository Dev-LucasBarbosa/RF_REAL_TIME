import psycopg2

class ConexaoDB():
    def __init__(self, 
                 database = "postgres", 
                 user = "postgres", 
                 host = "localhost", 
                 password = "postgres", 
                 port = 5433):
        self.database = database
        self.user = user
        self.host = host
        self.password = password
        self.port = port

    def conectar(self):
        self.con = psycopg2.connect(database = self.database,
                                    user = self.user,
                                    host = self.host,
                                    password = self.password,
                                    port = self.port)
        
        self.cur = self.con.cursor()

    def desconectar(self):
        self.con.close()


# conn = psycopg2.connect(database = "postgres",
#                         user = "postgres",
#                         host = 'localhost',
#                         password = "postgres",
#                         port = 5433)
