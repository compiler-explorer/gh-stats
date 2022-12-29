from pathlib import Path
from collections import defaultdict
import click
import json
import datetime
from github import Github
import os
from dataclasses import dataclass
import typing


@dataclass
class Context:
    github: Github


@click.group()
@click.pass_context
@click.option(
    "--access-token", default=os.getenv("GITHUB_TOKEN"), help="token to use (defaults to env var GITHUB_TOKEN)"
)
def cli(ctx, access_token: str):
    ctx.obj = Context(github=Github(access_token))


@cli.command()
@click.option("--organization", default="compiler-explorer")
@click.option("--project", default="compiler-explorer")
@click.argument("output", type=click.File(mode="a", encoding="utf8"))
@click.pass_obj
def stats(ctx: Context, output: typing.TextIO, organization: str, project: str) -> None:
    """Append JSON information to OUTPUT."""
    org = ctx.github.get_organization(organization)
    repo = org.get_repo(project)
    open = defaultdict(int)
    closed = defaultdict(int)
    with click.progressbar(repo.get_issues(state="all"), label="Reading issues") as issue_list:
        for issue in issue_list:
            to_update = open if issue.state == "open" else closed
            for label in issue.labels:
                to_update[label.name] += 1
    head_revision = repo.get_branch(repo.default_branch).commit.sha
    result = dict(
        as_of=datetime.datetime.now().isoformat(),
        head_revision=head_revision,
        languages=repo.get_languages(),
        issues=dict(open=open, closed=closed),
        open_issues_count=repo.open_issues_count,
        watchers_count=repo.watchers_count,
        stargazers_count=repo.stargazers_count,
        forks_count=repo.forks_count,
    )
    json.dump(result, output)
    output.write("\n")


if __name__ == "__main__":
    cli()
