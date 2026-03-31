import pandas as pd
from sqlalchemy import text
from repositories.sql_service import get_engine


class DoorPriceLookup:
    def __init__(self):
        self.engine = get_engine()

    def get_door_sell_price(self, door_model: str, width: float, height: float):
        query = text("""
            SELECT TOP 1 
                uaeDoorModelID,
                uaeHeight,
                uaeWidth,
                uaeRetailPriceBase
            FROM uSellPriceMatrixs
            WHERE uaeDoorModelID = :door_model
              AND uaeHeight  >= :height
              AND uaeWidth  >= :width
            ORDER BY uaeHeight ASC, uaeWidth ASC
        """)

        df = pd.read_sql(
            query,
            self.engine,
            params={
                "door_model": door_model,
                "height": height,
                "width": width
            }
        )

        if df.empty:
            return None

        return df.iloc[0]["uaeRetailPriceBase"]