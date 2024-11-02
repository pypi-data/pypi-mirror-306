# pip install psycopg2 pymysql sqlalchemy awswrangler boto3
from sqlalchemy import create_engine
from pandas import read_sql
import boto3
import awswrangler as wr
from os import getenv
import yaml

class Connector:

    tipos_bancos = {0: "rds", 1: "s3"}
    tipos_dados = {0: "consumo", 1: "cadastro"}
    clientes = {0: "sulgas", 1: "comgas"}

    def __init__(self, cliente: int, tipo_banco: int):

        """        
        tipo_banco:
            Deve ser um 'int' para representar os itens: {0: 'rds', 1: 's3'}

        cliente:
            Deve ser um 'int' para representar os itens: {0: 'sulgas', 1: 'comgas'}
        """

        if not isinstance(tipo_banco, int):
            raise Exception(f"""O parâmetro 'tipo_banco' deve ser do tipo 'int'. Porém, foi fornecido um objeto do 
                            tipo {type(tipo_banco)}""")
        
        if not isinstance(cliente, int):
            raise Exception(f"""O parâmetro 'cliente' deve ser do tipo 'int'. Porém, foi fornecido um objeto do 
                            tipo {type(cliente)}""")

        if not 0 <= tipo_banco < len(Connector.tipos_bancos):
            raise Exception(f"""O parâmetro 'tipo_banco' deve ser 'int' maior ou igual que zero e menor que o número 
                            de possibilidades de banco ({len(Connector.tipos_bancos)})""")
        
        if not 0 <= cliente < len(Connector.clientes):
            raise Exception(f"""O parâmetro 'cliente' deve ser 'int' maior ou igual que zero e menor que o número 
                            de clientes ({len(Connector.clientes)})""")

        if getenv("CONECTAR") != None:
            try:
                with open(f"{getenv("CONECTAR")}\\conectar.yaml", "r") as file:
                    dict_conectar = yaml.load(stream=file, Loader=yaml.Loader)
            except FileNotFoundError:
                raise Exception(f"O arquivo 'conectar.yaml' não foi encontrado no diretório especificado: {getenv('CONECTAR')}")
        else:
            raise Exception(f"Deve haver uma variável de Sistema Operacional chamada 'CONECTAR' com o caminho completo para o arquivo 'conectar.yaml'")

        self.tipo_banco: str = Connector.tipos_bancos[tipo_banco]
        self.cliente = Connector.clientes[cliente]
        kwargs = dict_conectar[self.cliente][self.tipo_banco]

        if self.tipo_banco == "rds":
            self.string_connection = f"{kwargs['DB_USER']}:{kwargs['DB_PASS']}@{kwargs['DB_HOST']}:{kwargs['DB_PORT']}/{kwargs['DB_NAME']}"
            self.dict_colunas_consumo = kwargs["colunas_consumo"]
            self.dict_colunas_cadastro = kwargs["colunas_cadastro"]

            self.db_engine = self.build_engine_rds()
        elif self.tipo_banco == "s3":
            self.path_consumo: str = kwargs['caminho_consumos']
            self.path_cadastro: str = kwargs['caminho_cadastros']
            self.s3_profile: str = kwargs["profile"]

            self.dict_colunas_consumo: dict = kwargs["colunas_consumo"]
            self.dict_colunas_cadastro: dict = kwargs["colunas_cadastro"]
            self.build_engine_s3()           

    def build_engine_rds(self):
        if self.tipo_banco == "rds":
            return create_engine(f"postgresql://{self.string_connection}")
    
    def build_engine_s3(self):
        if self.tipo_banco == "s3":
            boto3.setup_default_session(profile_name=self.s3_profile)

    def get_rds_dados(self, nm_tabela: str, tipo_dados: int):

        """
        nm_tabela:
            Deve ser um 'str' para representar o nome do database e da tabela. Por exemplo: db_name.tb_name
        tipo_dados:
            Deve ser um 'int' para representar os itens: {0: 'consumo', 1: 'cadastro'}
        """

        tipo_dados = Connector.tipos_dados[tipo_dados]

        if self.tipo_banco == "rds":
            colunas = self.dict_colunas_consumo if tipo_dados == "consumo" else self.dict_colunas_cadastro

            nm_colunas = ", ".join([coluna for coluna in colunas.keys() if colunas[coluna] == True])
            query = \
                f"""
                    SELECT
                        {nm_colunas}
                    FROM
                        {nm_tabela}
                """
            df = read_sql(query, con=self.db_engine)
            return df
        else:
            raise Exception(f"""Para utilizar o método 'get_rds_dados' o objeto deve possuir o atributo 
                            'tipo_banco' igual a 'rds'. Porém, o atributo está igual a {self.tipo_banco}""")
    
    def get_s3_dados(self, tipo_dados: int):
        """
        tipo_dados:
            Deve ser um 'int' para representar os itens: {0: 'consumo', 1: 'cadastro'}
        """
        tipo_dados = Connector.tipos_dados[tipo_dados]

        if self.tipo_banco == "s3":

            colunas = self.dict_colunas_consumo if tipo_dados == "consumo" else self.dict_colunas_cadastro
            colunas_usar = [coluna for coluna in colunas.keys() if colunas[coluna] == True]
            path = self.path_consumo if tipo_dados == "consumo" else self.path_cadastro

            df_consumo = wr.s3.read_parquet(path=path, columns=colunas_usar)
            return df_consumo
        else:
            raise Exception(f"""Para utilizar o método 'get_s3_dados' o objeto deve possuir o atributo 
                            'tipo_banco' igual a 's3'. Porém, o atributo está igual a {self.tipo_banco}""")
