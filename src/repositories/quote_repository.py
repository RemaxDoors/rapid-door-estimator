import pandas as pd
from sqlalchemy import text
from repositories.sql_service import get_engine


def search_records(search_text: str) -> pd.DataFrame:
    wildcard_term = f"%{search_text}%"
    engine = get_engine()

    query = text("""
        SELECT
            qmlQuoteID,
            qmlQuoteLineID,
            uqmlDoorModelID,
            qmpQuoteDate,
            O.cmoname AS CUSTOMERNAME,
            S.cmoName AS SHIPCUSTOMERNAME,
            qmlPartID,
            qmlPartShortDescription,
            qmqQuoteQuantity,
            qmqRevisedUnitPriceBase AS UNITSELLPRICE,
            qmqUnitDiscountBase AS DISCOUNT,
            uqmqResellerDiscount AS RESELLERDISCOUNT,
            qmqTotalUnitCost,
            uqmqMargin
        FROM QuoteLines AS QL
        LEFT JOIN QUOTES Q ON Q.qmpQuoteID = QL.qmlQuoteID
        LEFT JOIN Organizations O ON O.cmoOrganizationID = Q.qmpCustomerOrganizationID
        LEFT JOIN Organizations S ON S.cmoOrganizationID = Q.qmpShipOrganizationID
        LEFT JOIN QuoteQuantities AS QQ 
            ON QL.qmlQuoteID = QQ.qmqQuoteID 
           AND QL.qmlQuoteLineID = QQ.qmqQuoteLineID
        WHERE 
            (
                CAST(O.cmoname AS VARCHAR(50)) LIKE :term
                OR CAST(S.cmoname AS VARCHAR(50)) LIKE :term
                OR CAST(qmlQuoteID AS VARCHAR(50)) LIKE :term
                OR CAST(qmlQuoteLineID AS VARCHAR(50)) LIKE :term
                OR CAST(qmlPartID AS VARCHAR(50)) LIKE :term  
                OR CAST(qmlPartShortDescription AS VARCHAR(50)) LIKE :term
            )
            AND CAST(qmlPartID AS VARCHAR(50)) IN (
                'RRD-ES40','RRD-HS35','RRD-EX35','RRD-HS50',
                'RRD-HS50-THERMIC','RRD-EX45','RRD-CONCERTINA',
                'RRD-MOVIFOLD','RRD-MOVICHILL','RRD-HS35-THERMIC',
                'RRD-HS65','RRD-HS25','RRD-BUGSTOP',
                'RRD-MOVICHILL-XL','RRD-MS40-THERMIC'
            )
            AND qmqTotalUnitCost IS NOT NULL
        ORDER BY qmpQuoteDate DESC
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"term": wildcard_term})

    return df


def load_record_controls(
    quote_id: int,
    quote_line_id: int,
    part_id: str | None = None
) -> pd.DataFrame:

    engine = get_engine()
    unique_id = f"{quote_id}-{quote_line_id}"

    query = text("""
        SELECT
            [Unique_ID],
            [Part-ID],
            [DoorModelID],
            [DoorSellPrice],
            [xaiControlName],
            [xaiValue],
            [UNIT SELL PRICE],
            [QTY]
        FROM [uTraining_SalesPricingView]
        WHERE [Unique_ID] = :unique_id
          AND (:part_id IS NULL OR [Part-ID] = :part_id)
        ORDER BY [xaiControlName]
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "unique_id": unique_id,
                "part_id": part_id,
            }
        )

    return df