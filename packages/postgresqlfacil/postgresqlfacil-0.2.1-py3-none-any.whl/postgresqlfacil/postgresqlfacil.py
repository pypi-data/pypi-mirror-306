from dataclasses import dataclass
import datetime
import math
import pandas as pd
import psycopg2


@dataclass
class ConectorPostgreSQL:
    """
    Conector do Banco de Dados.

    Exemplo de seu uso em Context Manager:
        >>> with ConectorPostgreSQL(**{...}) as ConectorSQL:
        >>>     ...
    """

    database: str
    user: str
    password: str
    host: str
    port: int

    def __post_init__(self):
        self.con = psycopg2.connect(
            **{
                "database": self.database,
                "user": self.user,
                "password": self.password,
                "host": self.host,
                "port": self.port,
            }
        )
        self.con.autocommit = True

        cursor = self.con.cursor()
        cursor.execute("SET TIME ZONE 'America/Sao_Paulo'")
        cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def executa_query_select(self, query: str) -> pd.DataFrame:
        """
        Executa um Select Statement e retorna o resultado em uma dataframe
        Em caso de erro, retorna uma dataframe vazia.

        Exemplo:
            >>> df_consulta = SQL.executa_query_select(
            >>>     'SELECT {...} FROM {...};'
            >>> )
            >>> df_consulta
                id      data descricao
            0   1 2000-01-01       ...
            1   2 2000-02-01       ...
        """

        cursor = self.con.cursor()

        try:
            cursor.execute(query)

            dados = cursor.fetchall()
            colunas = [campo[0] for campo in cursor.description]
            cursor.close()

            return pd.DataFrame(dados, columns=colunas)

        except Exception as erro:
            print(erro)
            return pd.DataFrame()

    def executa_query_insert(self, query: str, returning=False) -> int:
        """
        Recebe um Insert Statement que retorna ou não um valor solicitado pelo
        usuário, geralmente o último id adicionado.

        Exemplo:
            >>> id_inserido = SQL.executa_query_insert(
            >>>     'INSERT INTO ... (...) VALUES (...) RETURNING id;',
            >>>     returning=True
            >>> )
            >>> id_inserido
            42
        """

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            if returning:
                returning_value = cursor.fetchone()[0]
                cursor.close()
                return returning_value
            else:
                cursor.close()
                return True

        except Exception as erro:
            print(erro)
            if returning:
                return 0
            else:
                return False

    def executa_query_update(self, query: str) -> bool:
        """
        Recebe um Update Statement que retorna um bool

        Em caso de erro, retorna 0

        Exemplo:
            >>> update = SQL.executa_query_update(
            >>>     'UPDATE ... SET ... = ...;'
            >>> )
            >>> update
            True
        """

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            cursor.close()
            return True

        except Exception as erro:
            print(erro)
            return False

    def executa_query_delete(self, query: str) -> bool:
        """
        Recebe um Delete Statement que retorna um bool

        Em caso de erro, retorna 0

        Exemplo:
            >>> delete = SQL.executa_query_update(
            >>>     'DELETE FROM ... WHERE ...;'
            >>> )
            >>> delete
            True
        """

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            cursor.close()
            return True

        except Exception as erro:
            print(erro)
            return False

    @staticmethod
    def transforma_df_em_insert_statement(df: pd.DataFrame, tabela: str) -> str:
        def formata_valor(value):
            if isinstance(value, str):
                return f"""'{value.replace("'", "''")}'"""
            elif isinstance(value, datetime.date):
                return f"'{value.isoformat()}'" if not pd.isna(value) else "NULL"
            elif value is None or (isinstance(value, float) and math.isnan(value)):
                return "NULL"
            else:
                return str(value)

        colunas = ",".join(f'"{col}"' for col in df.columns)
        query = f"INSERT INTO {tabela} ({colunas}) VALUES "

        valores = [
            f"({', '.join(formata_valor(valor) for valor in linha)})"
            for linha in df.itertuples(index=False, name=None)
        ]

        query += ", ".join(valores)
        return query
