"""
数据库迁移脚本：为 P2P 模块添加 SettleCore 集成字段
运行方式：cd backend && python -m app.services.migrate_p2p_settlecore
"""
import logging
import sqlite3
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库路径（相对于项目根目录）
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "khmerx.db")


def migrate():
    """为 p2p_offers 和 p2p_trades 表添加新字段"""
    if not os.path.exists(DB_PATH):
        logger.info(f"Database not found at {DB_PATH}, skipping migration")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 获取现有表结构
    cursor.execute("PRAGMA table_info(p2p_offers)")
    offer_columns = [row[1] for row in cursor.fetchall()]
    logger.info(f"p2p_offers existing columns: {offer_columns}")

    cursor.execute("PRAGMA table_info(p2p_trades)")
    trade_columns = [row[1] for row in cursor.fetchall()]
    logger.info(f"p2p_trades existing columns: {trade_columns}")

    # 添加 p2p_offers 新字段
    if "seller_settlecore_user_id" not in offer_columns:
        cursor.execute("ALTER TABLE p2p_offers ADD COLUMN seller_settlecore_user_id INTEGER")
        logger.info("Added column seller_settlecore_user_id to p2p_offers")
    if "seller_pay_address" not in offer_columns:
        cursor.execute("ALTER TABLE p2p_offers ADD COLUMN seller_pay_address TEXT DEFAULT ''")
        logger.info("Added column seller_pay_address to p2p_offers")

    # 添加 p2p_trades 新字段
    if "settlecore_tx_hash" not in trade_columns:
        cursor.execute("ALTER TABLE p2p_trades ADD COLUMN settlecore_tx_hash TEXT")
        logger.info("Added column settlecore_tx_hash to p2p_trades")
    if "settlecore_tx_status" not in trade_columns:
        cursor.execute("ALTER TABLE p2p_trades ADD COLUMN settlecore_tx_status TEXT DEFAULT ''")
        logger.info("Added column settlecore_tx_status to p2p_trades")

    conn.commit()
    conn.close()
    logger.info("Migration complete!")


if __name__ == "__main__":
    migrate()
