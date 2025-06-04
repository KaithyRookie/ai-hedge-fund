from src.back_worker_db.database import get_db_connection
from src.data.models import InsiderTrade

class InsiderTradeDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) 

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def insert_insider_trade(self, trade: InsiderTrade, ticker: str):
        """插入单条内部交易数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tb_insider_trade (
                    ticker, issuer, name, title, is_board_director, transaction_date,
                transaction_shares, transaction_price_per_share, transaction_value,
                shares_owned_before_transaction, shares_owned_after_transaction,
                security_title, filing_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            ticker, trade.issuer, trade.name, trade.title, trade.is_board_director,
            trade.transaction_date, trade.transaction_shares,
            trade.transaction_price_per_share, trade.transaction_value,
            trade.shares_owned_before_transaction, trade.shares_owned_after_transaction,
                trade.security_title, trade.filing_date
            ))
            self.conn.commit()

    def get_insider_trades(self, ticker: str, start_date: str = None, end_date: str = None) -> list[InsiderTrade]:
        """查询内部交易数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    SELECT issuer, name, title, is_board_director, transaction_date,
                        transaction_shares, transaction_price_per_share, transaction_value,
                        shares_owned_before_transaction, shares_owned_after_transaction,
                        security_title, filing_date
                    FROM tb_insider_trade
                    WHERE ticker = %s AND transaction_date BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("""
                    SELECT issuer, name, title, is_board_director, transaction_date,
                        transaction_shares, transaction_price_per_share, transaction_value,
                        shares_owned_before_transaction, shares_owned_after_transaction,
                        security_title, filing_date
                    FROM tb_insider_trade
                    WHERE ticker = %s
                """, (ticker,))

            trades = []
            for row in cur.fetchall():
                trades.append(InsiderTrade(
                    issuer=row[0],
                    name=row[1],
                    title=row[2],
                    is_board_director=row[3],
                    transaction_date=row[4],
                    transaction_shares=row[5],
                    transaction_price_per_share=row[6],
                    transaction_value=row[7],
                    shares_owned_before_transaction=row[8],
                    shares_owned_after_transaction=row[9],
                    security_title=row[10],
                    filing_date=row[11]
                ))
            return trades

    def delete_insider_trades(self, ticker: str, start_date: str = None, end_date: str = None):
        """删除内部交易数据"""
        with self.conn.cursor() as cur:
            if start_date and end_date:
                cur.execute("""
                    DELETE FROM tb_insider_trade
                    WHERE ticker = %s AND transaction_date BETWEEN %s AND %s
                """, (ticker, start_date, end_date))
            else:
                cur.execute("DELETE FROM tb_insider_trade WHERE ticker = %s", (ticker,))
            self.conn.commit()


    def update_insider_trade(self, trade: InsiderTrade, ticker: str):
        """更新单条内部交易数据"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tb_insider_trade
                SET issuer = %s, name = %s, title = %s, is_board_director = %s,
                    transaction_shares = %s, transaction_price_per_share = %s,
                    transaction_value = %s, shares_owned_before_transaction = %s,
                    shares_owned_after_transaction = %s, security_title = %s,
                    filing_date = %s
                WHERE ticker = %s AND transaction_date = %s
            """, (
                trade.issuer, trade.name, trade.title, trade.is_board_director,
                trade.transaction_shares, trade.transaction_price_per_share,
                trade.transaction_value, trade.shares_owned_before_transaction,
                trade.shares_owned_after_transaction, trade.security_title,
                trade.filing_date, ticker, trade.transaction_date
            ))
            self.conn.commit()

