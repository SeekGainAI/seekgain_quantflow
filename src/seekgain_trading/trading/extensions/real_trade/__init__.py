def load_extension():
    from seekgain_trading.trading.extensions.real_trade.main import TradingExtension
    return TradingExtension()