from appdirs import user_config_dir
from click import echo
from jira import JIRA, JIRAError
from tabulate import tabulate
import click
import os
import yaml


HEAD_FMT = "{0} | {1} | {2:.1f}h | {3}"
COMMENT_FMT = "{0} ({1}) @ {2}\n{3}"
ERROR_FMT = '[{0}] {1}'


def load_config():
    cfgfile = os.path.join(user_config_dir('ticket', 'mikeroll'), 'config.yml')
    with open(cfgfile, 'r') as cfg:
        return yaml.load(cfg)


def jira():
    global _jira
    if not _jira:
        _jira = JIRA(config['jira_url'],
                     basic_auth=(config['username'], config['password']))
    return _jira

_jira = None
config = load_config()


def ticket_key(ticket_id):
    if ticket_id.startswith(config['project'] + '-'):
        return ticket_id
    else:
        return config['project'] + '-' + ticket_id


def show_comment(c):
    echo(COMMENT_FMT.format(c.author.displayName, c.author.name, c.created,
                            c.body))


def show_ticket(ticket, head=True, url=True, body=True, comments=False):
    if head:
        echo(HEAD_FMT.format(
                ticket.key, ticket.fields.status.name,
                (ticket.fields.timespent or 0.0) / 3600.0,
                ticket.fields.summary))
    if url:
        echo(ticket.permalink())
    if body:
        echo("\n" + ticket.fields.description)
    if comments:
        echo("\n" + '-' * 16)
        for c in ticket.fields.comment.comments:
            show_comment(c)


class JiraAction(click.Command):
    def invoke(self, ctx):
        try:
            super(JiraAction, self).invoke(ctx)
        except JIRAError as je:
            echo(ERROR_FMT.format(je.status_code, je.text or ''), err=True)
            return 1


@click.group()
def cli():
    pass


@cli.command(cls=JiraAction)
@click.argument('summary')
@click.argument('description')
@click.option('--start', '-s', is_flag=True,
              help="Move the new ticket to \"in progress\" state.")
def new(summary, description, start):
    """Create a new ticket"""
    ticket = jira().create_issue(fields={
        'project': {'key': config['project']},
        'summary': summary,
        'description': description,
        'issuetype': {'name': config['default_type']},
        'assignee': {'name': jira().current_user()}
    })
    if start:
        jira().transition_issue(ticket, config['transition_start'])
    show_ticket(ticket)


@cli.command(cls=JiraAction)
@click.argument('ticket_id', required=False)
@click.option('--body', '-b', help="Include ticket body", is_flag=True)
@click.option('--comments', '-c', help="Include comments", is_flag=True)
def show(ticket_id, body, comments):
    """Show open tickets or ticket details"""
    if ticket_id:
        ticket = jira().issue(ticket_key(ticket_id))
        if not body and not comments:
            body = config.get('show_body', True)
            comments = config.get('show_comments', False)
        show_ticket(ticket, body=body, comments=comments)
    else:
        query = ('project = {0} AND '.format(config['project']) +
                 'assignee in (currentUser()) AND ' +
                 'status in ({0})'.format(
                    ','.join('"' + t + '"' for t in config['open_types'])))
        issues = jira().search_issues(query)
        if issues:
            echo(tabulate([(i.key, i.fields.status.name, i.fields.summary)
                           for i in issues], tablefmt='plain'))


@cli.command(cls=JiraAction)
@click.argument('ticket_id')
def start(ticket_id):
    """Start working on a ticket"""
    jira().transition_issue(ticket_key(ticket_id), config['transition_start'])
    show_ticket(jira().issue(ticket_key(ticket_id)),
                head=True, body=False, comments=False, url=False)


@cli.command(cls=JiraAction)
@click.argument('ticket_id')
def stop(ticket_id):
    """Stop working on a ticket"""
    jira().transition_issue(ticket_key(ticket_id), config['transition_stop'])
    show_ticket(jira().issue(ticket_key(ticket_id)),
                head=True, body=False, comments=False, url=False)


@cli.command(cls=JiraAction)
@click.argument('ticket_id')
@click.argument('message', required=False)
def close(ticket_id, message):
    """Close a ticket"""
    jira().transition_issue(ticket_key(ticket_id), config['transition_close'])
    show_ticket(jira().issue(ticket_key(ticket_id)),
                head=True, body=False, comments=False, url=False)
    if message:
        comment = jira().add_comment(ticket_key(ticket_id), message)
        show_comment(comment)


@cli.command(cls=JiraAction)
@click.argument('ticket_id')
@click.argument('time')
def log(ticket_id, time):
    """Log work on a ticket"""
    jira().add_worklog(ticket_key(ticket_id), time)
    show_ticket(jira().issue(ticket_key(ticket_id)),
                head=True, body=False, comments=False, url=False)


@cli.command(cls=JiraAction)
@click.argument('ticket_id')
@click.argument('message')
def say(ticket_id, message):
    """Comment on a ticket"""
    comment = jira().add_comment(ticket_key(ticket_id), message)
    show_comment(comment)
