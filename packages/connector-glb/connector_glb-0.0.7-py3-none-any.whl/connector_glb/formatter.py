from pandas import DataFrame, to_datetime

class FormatterConsumo:

    def comgas2sulgas(df: DataFrame) -> None:
        df.rename(columns={"ds_numero_instalacao": "id_cliente",
                           "dt_transmissao": "id_calendario",
                           "val_consumo": "val_consumo_diario"},
                   inplace=True)
        
        df["id_cliente"] = df["id_cliente"].astype("int32")
        df['id_calendario'] = to_datetime(df['id_calendario'], format="%Y%m%d")
        df["val_consumo_diario"] = df["val_consumo_diario"].astype("float")

        # return df

    def sulgas2comgas(df: DataFrame) -> None:

        df.rename(columns={"id_cliente": "ds_numero_instalacao",
                           "id_calendario": "dt_transmissao",
                           "val_consumo_diario": "val_consumo"},
                   inplace=True)
        
        df["ds_numero_instalacao"] = df["ds_numero_instalacao"].astype("int32")
        df['dt_transmissao'] = to_datetime(df['dt_transmissao'], format="%Y%m%d")
        df["val_consumo"] = df["val_consumo"].astype("float")

class FormatterCadastro:

    def comgas2sulgas(df: DataFrame) -> None:

        df.rename(columns={"instalacao": "id_cliente",
                           "latitude": "val_latitude",
                           "longitude": "val_longitude"},
                   inplace=True)
        
        df["id_cliente"] = df["id_cliente"].astype("int32")


        # df['val_latitude'] = df['val_latitude'].astype("float")
        # df["val_longitude"] = df["val_longitude"].astype("float")


    def sulgas2comgas(df: DataFrame) -> None:

        df.rename(columns={"id_cliente": "instalacao",
                           "val_latitude": "latitude",
                           "val_longitude": "longitude"},
                   inplace=True)
        
        df["instalacao"] = df["instalacao"].astype("int32")
