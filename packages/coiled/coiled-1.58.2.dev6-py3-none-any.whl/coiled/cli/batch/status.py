import click
from rich import print

from coiled.cli.curl import sync_request

from ..utils import CONTEXT_SETTINGS


@click.command(context_settings={**CONTEXT_SETTINGS, "ignore_unknown_options": True})
@click.option("--workspace", default=None, type=str)
@click.argument("job_id", nargs=1)
def batch_status(**kwargs):
    job_id = kwargs["job_id"]

    import coiled

    with coiled.Cloud(workspace=kwargs["workspace"]) as cloud:
        url = f"{cloud.server}/api/v2/jobs/{job_id}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            # json=True,
            json_output=True,
        )

        print(response)
