from fudstop.apis.webull.webull_options.webull_options import WebullOptions
from fudstop.apis.webull.webull_option_screener import WebullOptionScreener
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.webull.webull_trading import WebullTrading
from fudstop.apis.occ.occ_sdk import occSDK
trading = WebullTrading()
screen = WebullOptionScreener()
db = PolygonDatabase()
wb = WebullOptions()
occ = occSDK(host='localhost', user='chuck', database='market_data', password='fud', port=5432)
import os
from dotenv import load_dotenv
load_dotenv()


from polygon.websocket import WebSocketClient, Market
from polygon.websocket.models import WebSocketMessage
from typing import List
import asyncio
import pandas as pd
c = WebSocketClient(subscriptions=["T.*"], api_key=os.environ.get('YOUR_POLYGON_KEY'), market=Market.Options)

from collections import deque
# Adjust batch size and flush interval based on system and traffic
BATCH_SIZE = 75
FLUSH_INTERVAL = 0.01  # in seconds

# Queue to hold messages temporarily
message_queue = deque()
# Class to handle Polygon live WebSocket and database operations
class PolygonLIVE:
    def __init__(self, db):
        self.db = db
        self.option_conditions_dict = {
        201: 'Canceled',
        202: 'Late and Out Of Sequence',
        203: 'Last and Canceled',
        204: 'Late',
        205: 'Opening Trade and Canceled',
        206: 'Opening Trade, Late, and Out Of Sequence',
        207: 'Only Trade and Canceled',
        208: 'Opening Trade and Late',
        209: 'Automatic Execution',
        210: 'Reopening Trade',
        219: 'Intermarket Sweep Order',
        227: 'Single Leg Auction Non ISO',
        228: 'Single Leg Auction ISO',
        229: 'Single Leg Cross Non ISO',
        230: 'Single Leg Cross ISO',
        231: 'Single Leg Floor Trade',
        232: 'Multi Leg auto-electronic trade',
        233: 'Multi Leg Auction',
        234: 'Multi Leg Cross',
        235: 'Multi Leg floor trade',
        236: 'Multi Leg auto-electronic trade against single leg(s)',
        237: 'Stock Options Auction',
        238: 'Multi Leg Auction against single leg(s)',
        239: 'Multi Leg floor trade against single leg(s)',
        240: 'Stock Options auto-electronic trade',
        241: 'Stock Options Cross',
        242: 'Stock Options floor trade',
        243: 'Stock Options auto-electronic trade against single leg(s)',
        244: 'Stock Options Auction against single leg(s)',
        245: 'Stock Options floor trade against single leg(s)',
        246: 'Multi Leg Floor Trade of Proprietary Products',
        247: 'Multilateral Compression Trade of Proprietary Products',
        248: 'Extended Hours Trade',
    }
            
    # Helper function to map conditions
    def map_option_conditions(self, conditions):
        return [self.option_conditions_dict.get(condition, "Unknown Condition") for condition in conditions]



    async def handle_msg(self, msgs: List[WebSocketMessage]):
        global message_queue
        for m in msgs:
            conditions = m.conditions[0] if m.conditions else None
            message = {
                'option_symbol': m.symbol,
                'exchange': m.exchange,
                'price': m.price,
                'size': m.size,
                'condition': conditions,
                'sequence': m.sequence_number,
                'timestamp': m.timestamp
            }
            message_queue.append(message)

            if len(message_queue) >= BATCH_SIZE:
                await self.flush_to_db()

    async def flush_to_db(self):
        global message_queue
        if message_queue:
            # Convert queue to a DataFrame
            df = pd.DataFrame(list(message_queue))

            # Clear queue after flushing
            message_queue.clear()

            # Batch upsert to the database
            await self.db.batch_upsert_dataframe(df, table_name='live_options', unique_columns=['option_symbol'])

    async def periodic_flush(self):
        while True:
            await asyncio.sleep(FLUSH_INTERVAL)
            if len(message_queue) > 0:
                await self.flush_to_db()

    async def run(self):
        await self.db.connect()
        await asyncio.gather(c.connect(self.handle_msg), self.periodic_flush())