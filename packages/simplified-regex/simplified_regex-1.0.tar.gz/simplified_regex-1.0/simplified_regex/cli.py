import click

@click.group()
def cli():
    """simplified_regex, CLI Library."""
    pass
    
@cli.command()
def example():
    print("example / simplified_regex")

cli.add_command(example)
