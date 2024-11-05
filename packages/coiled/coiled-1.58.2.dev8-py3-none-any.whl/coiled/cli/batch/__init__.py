import click

from ..utils import CONTEXT_SETTINGS
from .run import batch_run
from .status import batch_status


@click.group(name="batch", context_settings=CONTEXT_SETTINGS)
def batch_group():
    """Commands for managing Coiled batch jobs"""


batch_group.add_command(batch_run, "run")
batch_group.add_command(batch_status, "status")
