from pyxxl import PyxxlRunner, JobHandler

import src.rpa_executor_icodefun.cli as cli
from tasks import TaskCollector


def run():
    config = cli.run_cli()

    collector = TaskCollector(config)

    xxl_handler = JobHandler()

    pyxxl_app = PyxxlRunner(config, handler=xxl_handler)
    for task_info in collector.collect():
        collector.register(pyxxl_app, task_info)

    if config.debug:
        pyxxl_app.run_executor()
    else:
        pyxxl_app.run_with_daemon()


if __name__ == "__main__":
    run()
