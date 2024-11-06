import json
import time
import uuid
from enum import Enum

import typer

from .backend_client.gen.models import Report, Status
from .backend_client.client import TheCVESBackend
from .settings import TheCvesSettings

app = typer.Typer()


class OutputType(Enum):
    json: str = 'json'
    plaintext: str = 'plain'


@app.command("run_report")
def run_report(product_id: int, release_id: int, confluence_space_key: str, image_id: int = None,
               cves: str = "",
               confluent_parent_page_title: str = None,
               github_working_dir: str = None,
               output_format: OutputType = OutputType.json.value):
    """
    Generate a report for a given product and release.

    Args:
        :param cves: comma separated CVEs
        :param use_agent: run flow with agent
        :param github_working_dir:
        :param product_id: The product ID (mandatory).
        :param release_id: The release ID (mandatory).
        :param image_id: The image ID.
        :param confluence_space_key: the confluence space key
        :param confluent_parent_page_title:
        :param output_format:
        :param github_token:
        :param github_repo_url:
    """
    cves_list = []
    if cves:
        cves_list = cves.split(',')
    the_cves_cli_settings = TheCvesSettings()
    backend_client = TheCVESBackend(the_cves_cli_settings)
    res: Report = backend_client.start_job(
        report_id=Report(productID=product_id, releaseID=release_id,
                         imageID=image_id, cves=cves_list,
                         confluenceSpaceKey=confluence_space_key,
                         confluenceKey=the_cves_cli_settings.confluence_token,
                         confluenceDomain=the_cves_cli_settings.confluence_domain,
                         confluenceUser=the_cves_cli_settings.confluence_user,
                         confluenceParentPageTitle=confluent_parent_page_title,
                         gitHubToken=the_cves_cli_settings.github_token,
                         gitHubRepoURL=the_cves_cli_settings.github_repo_url,
                         gitHubWorkingDir=github_working_dir))
    if output_format == OutputType.json:
        typer.echo(json.dumps({'job_id': str(res.id), 'confluence_page_url': res.docURL}))
    else:
        typer.echo(f"Job ID: {res.id}, Confluence page URL: {res.docURL}")


@app.command("status")
def status(job_id: uuid.UUID, output_format: OutputType = OutputType.json.value, follow: bool = False):
    """
    Generate a report for a given product and release.

    Args:
        job_id (str): The job_id ID (mandatory).
        :param follow:
        :param job_id:
        :param output_format:
    """
    the_cves_cli_settings = TheCvesSettings()
    backend_client = TheCVESBackend(the_cves_cli_settings)
    report_status = None
    while report_status not in [Status.success, Status.failed]:
        report_status = _print_status(backend_client, job_id, output_format)
        if not follow:
            break
        time.sleep(5)


def _print_status(backend_client: TheCVESBackend, job_id: uuid.UUID, output_format: OutputType) -> Status:
    report: Report = backend_client.get_status(job_id)
    if output_format == OutputType.json:
        typer.echo(json.dumps({'status': report.status.value, 'confluence_page_url': report.docURL}))
    else:
        typer.echo(f"Status: {report.status}, Confluence page URL: {report.docURL}")
    return report.status


if __name__ == "__main__":
    app()
