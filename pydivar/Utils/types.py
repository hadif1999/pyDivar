from typing import Literal

class mt5rest:
    NEW_ORDER_TYPE = Literal["Buy", "Sell", "BuyLimit", "SellLimit",
                            "BuyStop", "SellStop",
                            "BuyStopLimit", "SellStopLimit", "CloseBy",
                            "Balance", "Credit"]