

def ohlcv_to_df(ohlcv_data: list[dict], time_col: str = "time", 
                            rename_cols: dict[str, str] = {"openPrice": "open", 
                                                           "highPrice": "high",
                                                           "lowPrice": "low", 
                                                           "closePrice": "close"},
                            drop_time_col:bool = True) -> "pd.DataFrame":
    import pandas as pd
    df = pd.DataFrame(ohlcv_data)
    ## changing df col names
    df.rename(columns=rename_cols, inplace=True)
    ## formatting datetime col and make as index
    df[time_col] = pd.to_datetime(df[time_col])
    df.set_index(time_col, drop=drop_time_col, inplace=True)
    return df