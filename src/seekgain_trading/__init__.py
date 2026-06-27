"""SeekGain Workflow seekgain_trading package"""
import os
from seekgain_backtest.util.log.remote_log_factory import RemoteLogFactory

project_dir = os.path.dirname(os.path.abspath(__file__))
SRLogger = RemoteLogFactory.get_sr_logger()