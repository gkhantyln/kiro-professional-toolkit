---
name: create-python-cli-tool
description: Production Python CLI with Typer, Rich TUI, async commands, plugin architecture, config management, shell completion, and PyPI packaging
---

# Create Python CLI Tool

Production-ready Python CLI aracı oluşturur:
- Typer + Rich (beautiful TUI)
- Async command execution
- Plugin architecture
- Config management (dynaconf)
- Shell completion (bash/zsh/fish)
- Progress bars + spinners
- PyPI packaging (hatch)

## Usage
```
#create-python-cli-tool <tool-name>
```

## cli/main.py
```python
import typer
from rich.console import Console
from rich.theme import Theme
import asyncio
from typing import Annotated
from pathlib import Path

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
})

app = typer.Typer(
    name="mytool",
    help="[bold cyan]MyTool[/] — Production CLI",
    rich_markup_mode="rich",
    no_args_is_help=True,
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=False,
)
console = Console(theme=custom_theme)

# Sub-command groups
from cli.commands import deploy, db, config as config_cmd
app.add_typer(deploy.app, name="deploy", help="Deployment commands")
app.add_typer(db.app, name="db", help="Database commands")
app.add_typer(config_cmd.app, name="config", help="Configuration commands")

def version_callback(value: bool):
    if value:
        from cli import __version__
        console.print(f"[bold]mytool[/] version [cyan]{__version__}[/]")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[bool, typer.Option("--version", "-v", callback=version_callback, is_eager=True)] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-V", help="Enable verbose output")] = False,
    config_file: Annotated[Path | None, typer.Option("--config", "-c", help="Config file path")] = None,
):
    """[bold cyan]MyTool[/] — A professional CLI tool."""
    from cli.context import ctx
    ctx.verbose = verbose
    if config_file:
        ctx.load_config(config_file)

if __name__ == "__main__":
    app()
```

## cli/commands/deploy.py
```python
import typer
import asyncio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from typing import Annotated

app = typer.Typer()
console = Console()

@app.command()
def run(
    environment: Annotated[str, typer.Argument(help="Target environment")] = "staging",
    image: Annotated[str, typer.Option("--image", "-i", help="Docker image tag")] = "latest",
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Preview without executing")] = False,
    wait: Annotated[bool, typer.Option("--wait/--no-wait", help="Wait for completion")] = True,
):
    """Deploy application to target environment."""
    asyncio.run(_deploy(environment, image, dry_run, wait))

async def _deploy(env: str, image: str, dry_run: bool, wait: bool):
    console.print(Panel(
        f"[bold]Deploying[/] [cyan]{image}[/] → [green]{env}[/]",
        title="🚀 Deployment",
        border_style="cyan",
    ))

    if dry_run:
        console.print("[warning]DRY RUN — no changes will be made[/]")
        return

    steps = [
        ("Validating config", _validate_config),
        ("Building image", _build_image),
        ("Pushing to registry", _push_image),
        ("Updating deployment", _update_deployment),
        ("Running health checks", _health_check),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Deploying...", total=len(steps))
        for description, step_fn in steps:
            progress.update(task, description=description)
            await step_fn(env, image)
            progress.advance(task)

    console.print("[success]✓ Deployment complete![/]")

async def _validate_config(env: str, image: str): await asyncio.sleep(0.5)
async def _build_image(env: str, image: str): await asyncio.sleep(1.0)
async def _push_image(env: str, image: str): await asyncio.sleep(0.8)
async def _update_deployment(env: str, image: str): await asyncio.sleep(1.2)
async def _health_check(env: str, image: str): await asyncio.sleep(0.6)

@app.command()
def status(
    environment: Annotated[str, typer.Argument()] = "production",
    output: Annotated[str, typer.Option("--output", "-o")] = "table",
):
    """Show deployment status."""
    asyncio.run(_show_status(environment, output))

async def _show_status(env: str, output_fmt: str):
    # Fetch status from API
    deployments = [
        {"service": "api", "version": "v1.2.3", "replicas": "3/3", "status": "✓ Running"},
        {"service": "worker", "version": "v1.2.3", "replicas": "2/2", "status": "✓ Running"},
        {"service": "scheduler", "version": "v1.2.2", "replicas": "1/1", "status": "⚠ Outdated"},
    ]

    if output_fmt == "json":
        import json
        console.print_json(json.dumps(deployments))
        return

    table = Table(title=f"Deployments — {env}", border_style="cyan")
    table.add_column("Service", style="bold")
    table.add_column("Version", style="cyan")
    table.add_column("Replicas")
    table.add_column("Status")

    for d in deployments:
        table.add_row(d["service"], d["version"], d["replicas"], d["status"])

    console.print(table)
```

## cli/context.py
```python
from dataclasses import dataclass, field
from pathlib import Path
from dynaconf import Dynaconf

@dataclass
class AppContext:
    verbose: bool = False
    _settings: Dynaconf | None = None

    def load_config(self, config_file: Path):
        self._settings = Dynaconf(
            settings_files=[str(config_file)],
            environments=True,
            load_dotenv=True,
        )

    @property
    def settings(self) -> Dynaconf:
        if not self._settings:
            self._settings = Dynaconf(
                settings_files=["settings.toml", ".secrets.toml"],
                environments=True,
                load_dotenv=True,
            )
        return self._settings

ctx = AppContext()
```

## pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mytool"
version = "0.1.0"
description = "A professional CLI tool"
requires-python = ">=3.11"
dependencies = [
    "typer[all]>=0.12",
    "rich>=13",
    "httpx>=0.27",
    "dynaconf>=3.2",
    "anyio>=4",
]

[project.scripts]
mytool = "cli.main:app"

[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio", "mypy", "ruff"]

[tool.hatch.envs.default]
dependencies = ["pytest", "pytest-asyncio", "coverage"]

[tool.hatch.envs.default.scripts]
test = "pytest {args:tests}"
lint = "ruff check . && mypy cli/"
```
