"""
          ┌─┐       ┌─┐
       ┌──┘ ┴───────┘ ┴──┐
       │                 │
       │       ───       │
       │  ─┬┘       └┬─  │
       │                 │
       │       ─┴─       │
       │                 │
       └───┐         ┌───┘
           │         │
           │         │
           │         │
           │         └──────────────┐
           │                        │
           │                        ├─┐
           │                        ┌─┘
           │                        │
           └─┐  ┐  ┌───────┬──┐  ┌──┘
             │ ─┤ ─┤       │ ─┤ ─┤
             └──┴──┘       └──┴──┘
                 神兽保佑
                 代码无BUG!
"""
from seekgain_backtest.config.dev_init import DevInit
from importlib import import_module
from seekgain_backtest.backtest_common.system.context.core_context import CoreContext
from seekgain_backtest.backtest_common.system.event.engine import Engine
from seekgain_backtest.backtest_common.system.compile.strategy import Strategy
from seekgain_backtest.backtest_common.system.compile.strategy_utils import FileStrategyLoader
import traceback
from seekgain_backtest.data.context.strategy_context import StrategyContext
from seekgain_backtest.system.seekgain_log import SRLogger


class Run(object):

    @staticmethod
    def start(handle_message):
        # # LogFactory.init_logger() - 已替换为统一日志配置

        # 系统核心上下文 创建q
        strategy_context = StrategyContext()
        _context = CoreContext(strategy_context)

        back_test_id = handle_message['back_test_id']
        DevInit.init_log_env('seekgain')
        DevInit.init_remote_sr_log(back_test_id, handle_message['run_params'], strategy_context)

        # 全局动态字典初始化
        global_args = {}

        run_type = 6

        # 风控相关
        # strategy_risk_control_list = handle_message.get('strategy_risk_control_list', None)
        # risk_control_manager = RiskControlManager(MongoClient.get_mongo_db(), _context.event_bus, strategy_context)
        # risk_control_manager.load_local_risk_control(strategy_risk_control_list)
        # risk_control_manager.init_event()
        # _context.set_risk_control_manager(risk_control_manager)

        global_args = FileStrategyLoader(handle_message['file'], True).load(global_args)
        handle_message['strategy_id'] = 1
        extension_module = import_module("seekgain_backtest.extensions.trade_reverse_future")
        extension = extension_module.load_extension()
        extension.create(_context)
        Strategy(global_args, _context.event_bus)

        # SRLogger.info(str(handle_message))
        # 项目启动
        try:
            Engine(_context).run(handle_message)
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))

        SRLogger.end()



