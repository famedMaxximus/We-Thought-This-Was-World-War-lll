#!/usr/bin/env python3
"""
Live LCA Scoreboard Monitor for Finals
Real-time scoreboard polling with rich terminal UI.
"""
import asyncio
import aiohttp
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box

# Configuration
LCA_API_URL = os.getenv("LCA_API_URL", "https://lca.labs.ctfroom.com/api/scoreboard")
TEAM_NAME = os.getenv("TEAM_NAME", "We Thought This Was World War III")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "10"))
OUR_TEAM_HIGHLIGHT = True

console = Console()


class ScoreboardMonitor:
    def __init__(self, api_url: str, team_name: str, refresh: int = 10):
        self.api_url = api_url
        self.team_name = team_name
        self.refresh = refresh
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_data: Optional[Dict] = None
        self.start_time = datetime.now()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_scoreboard(self) -> Optional[Dict]:
        """Fetch scoreboard from LCA API."""
        if not self.session:
            return None
        try:
            async with self.session.get(self.api_url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": f"HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"error": "Timeout"}
        except Exception as e:
            return {"error": str(e)}

    def find_our_rank(self, teams: List[Dict]) -> Optional[int]:
        """Find our team's rank."""
        for i, team in enumerate(teams, 1):
            if self.team_name.lower() in team.get("name", "").lower():
                return i
        return None

    def render_scoreboard(self, data: Dict) -> Panel:
        """Render scoreboard as rich panel."""
        if "error" in data:
            return Panel(
                f"[red]Error:[/red] {data['error']}",
                title="Scoreboard Error",
                border_style="red"
            )

        teams = data.get("teams", [])
        if not teams:
            return Panel(
                "[yellow]No teams data[/yellow]",
                title="Empty Scoreboard",
                border_style="yellow"
            )

        # Main scoreboard table
        table = Table(
            title="LCA SCOREBOARD - LIVE",
            box=box.ROUNDED,
            border_style="bright_blue",
            header_style="bold bright_white on blue",
            show_lines=True
        )
        table.add_column("#", style="bold gold1", width=4, justify="right")
        table.add_column("Team", style="cyan", min_width=30)
        table.add_column("Points", style="bold green", justify="right", width=12)
        table.add_column("Last Solve", style="yellow", width=28)
        table.add_column("Delta", style="magenta", justify="right", width=8)

        our_rank = self.find_our_rank(teams)
        prev_points = {}
        if self.last_data:
            for t in self.last_data.get("teams", []):
                prev_points[t.get("name", "")] = t.get("points", 0)

        for i, team in enumerate(teams[:20], 1):  # Top 20
            name = team.get("name", "Unknown")
            points = team.get("points", 0)
            last_solve = team.get("latest_solve", team.get("last_activity", "-"))

            # Calculate point delta
            delta = ""
            if name in prev_points:
                diff = points - prev_points[name]
                if diff > 0:
                    delta = f"+{diff}"
                elif diff < 0:
                    delta = str(diff)

            # Highlight our team
            if OUR_TEAM_HIGHLIGHT and self.team_name.lower() in name.lower():
                name_display = f"[bold black on gold1] {name} [/]"
                points_display = f"[bold black on gold1] {points:,} [/]"
                rank_display = f"[bold black on gold1] {i} [/]"
            else:
                name_display = name
                points_display = f"{points:,}"
                rank_display = str(i)

            # Truncate long names
            if len(name_display) > 35:
                name_display = name_display[:32] + "..."

            table.add_row(rank_display, name_display, points_display, str(last_solve), delta)

        # Our team status panel
        our_team = None
        if our_rank:
            our_team = teams[our_rank - 1]
        
        status_lines = []
        if our_team:
            gap = ""
            if our_rank > 1:
                leader = teams[0]
                gap_pts = leader.get("points", 0) - our_team.get("points", 0)
                gap = f"[red]Gap to 1st: {gap_pts:,} pts[/red]"
            else:
                gap = "[bold green]LEADING[/bold green]"
            
            status_lines = [
                f"[bold]Our Rank:[/bold] #{our_rank} / {len(data.get('teams', []))}",
                f"[bold]Our Score:[/bold] {our_team.get('points', 0):,} pts",
                gap,
                f"[dim]Last Solve: {our_team.get('latest_solve', 'N/A')}[/dim]",
            ]

        status_panel = Panel(
            "\n".join(status_lines) if status_lines else "[dim]Not ranked yet[/dim]",
            title="[bold]OUR TEAM[/bold]",
            border_style="gold1",
            padding=(1, 2)
        )

        # Header info
        header = Text.assemble(
            ("LCA Live Scoreboard", "bold bright_white"),
            (" | ", "dim"),
            (f"Team: {self.team_name}", "cyan"),
            (" | ", "dim"),
            (f"Refresh: {self.refresh}s", "yellow"),
            (" | ", "dim"),
            (f"Uptime: {datetime.now() - self.start_time}", "dim"),
        )

        # Layout
        layout = Layout()
        layout.split_column(
            Layout(Panel(header, border_style="blue", padding=(0, 1)), size=3),
            Layout(
                Table.grid()
                .add_column(ratio=3)
                .add_column(ratio=1)
                .add_row(
                    Panel(table, border_style="bright_blue"),
                    status_panel
                )
            )
        )

        return Panel(layout, title="[bold]LCA SCOREBOARD MONITOR[/bold]", border_style="bright_green", padding=1)

    async def run(self):
        """Main monitoring loop."""
        with Live(console=console, refresh_per_second=4, screen=True) as live:
            while True:
                data = await self.fetch_scoreboard()
                if data:
                    self.last_data = data
                    panel = self.render_scoreboard(data)
                    live.update(panel)
                else:
                    live.update(Panel("[red]Failed to fetch scoreboard[/red]", border_style="red"))
                await asyncio.sleep(self.refresh)


async def main():
    api_url = os.getenv("LCA_API_URL", "https://lca.labs.ctfroom.com/api/scoreboard")
    team_name = os.getenv("TEAM_NAME", "We Thought This Was World War III")
    refresh = int(os.getenv("REFRESH_INTERVAL", "10"))

    console.print(Panel.fit(
        f"[bold]LCA Scoreboard Monitor[/bold]\n"
        f"Team: [cyan]{team_name}[/cyan]\n"
        f"API: [dim]{api_url}[/dim]\n"
        f"Refresh: [yellow]{refresh}s[/yellow]",
        title="Starting Monitor",
        border_style="green"
    ))

    async with ScoreboardMonitor(api_url, team_name, refresh) as monitor:
        try:
            await monitor.run()
        except KeyboardInterrupt:
            console.print("\n[dim]Monitor stopped.[/dim]")


if __name__ == "__main__":
    asyncio.run(main())