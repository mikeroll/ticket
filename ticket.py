import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('summary')
@click.argument('description')
@click.option('--start', '-s', is_flag=True,
              help="Move the new ticket to \"in progress\" state.")
def new(summary, description):
    """Open a new ticket"""
    pass


@cli.command()
@click.argument('ticket_id')
@click.option('--body', '-b', help="Include ticket body", is_flag=True)
@click.option('--comments', '-c', help="Include comments", is_flag=True)
def show(ticket_id):
    """Show ticket details"""
    pass


@cli.command()
@click.argument('ticket_id')
@click.argument('time')
def log(ticket_id, time):
    """Log work on an ticket"""
    pass


@cli.command()
@click.argument('ticket_id')
@click.argument('message')
def say(ticket_id, message):
    """Comment on an ticket"""
    pass


@cli.command()
@click.argument('ticket_id')
@click.argument('message')
@click.option('--resolution', '-r', default='done')
def close(ticket_id, message):
    """Close a ticket providing a comment"""
    pass


@cli.command()
def mine(state):
    """Show my open tickets"""
    pass
