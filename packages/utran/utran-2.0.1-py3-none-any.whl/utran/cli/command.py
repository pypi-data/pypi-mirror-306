import os
import click

from .utils import get_local_utran
import utran
from utran.log import logger

@click.group(help="utran [COMMAND] [OPTIONS].")
def cli():
    """Main command group."""


#  tots command
@cli.command(help="Execute the TOTS command with required arguments.")
@click.argument("entry", required=True, type=click.Path(exists=True))
@click.argument("output", required=False, type=click.Path())
@click.option("--module_name", default="UtranClient", help="Module name of the entry file.")
def tots(entry: str, output: str | None = None,module_name: str | None = "UtranClient"):
    """Execute a command with options."""
    try:
        _utran = get_local_utran(entry)
        if _utran:
            # 执行 utran.tots()
            all_actions = _utran._get_all_actions()
            [utran.PyTs.convert_to_ts(a._source_fn) for a in all_actions]
            res = utran.PyTs.get_output_ts_str(module_name)
            file_name = 'type.d.ts' if output is None else os.path.basename(output) if os.path.basename(output).endswith('.ts') else os.path.basename(output) + '.ts'
            output_dir = os.path.dirname(output) if output else os.getcwd()
            output_file = os.path.join(output_dir, file_name)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(res)

    except Exception as e:     
        logger.exception(e)   
        click.secho(f"Internal error: {e}", err=True, fg="red")
        


# run command
@cli.command(help="Run the server with the specified entry file and options.")
@click.argument("entry", required=True, type=click.Path(exists=True))
@click.option("--host", default="localhost", help="Host to bind to.")
@click.option("--port", default=2525, help="Port to bind to.")
def run(entry: str, host: str, port: int):
    """Execute a command with options."""
    try:
        _utran = get_local_utran(entry)
        if _utran:
            _utran.run(host=host, port=port)
    except Exception as e:
        logger.exception(e)
        click.secho(f"Internal error: {e}", err=True, fg="red")