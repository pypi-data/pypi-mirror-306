# -*- coding: UTF-8 -*-
import os
from typing import Annotated

from typer import Typer, Option, Argument

from .blog import Blog
from .config import Config
from .config_commands import app as config_app
from .item import Item, BlogType
from .prompt import *
from .utils import complete_items

app = Typer(
    no_args_is_help=True,
    help='Jekyll Blog CLI Tool.',
    rich_markup_mode='rich'
)

app.add_typer(config_app, rich_help_panel='Configuration')


@app.command(rich_help_panel='Deployment')
def serve(
    draft: Annotated[bool, Option(help='Start blog server with drafts.')] = Config.select('deploy.draft'),
    port: Annotated[int, Option(help='Listen on the given port.')] = Config.select('deploy.port')
):
    """Start blog server locally through jekyll."""
    if Config.root is not None:
        os.chdir(Config.root)
    command = 'bundle exec jekyll serve'
    # draft option
    if draft:
        command += ' --drafts'
    if port is not None:
        command += f' --port {port}'
    os.system(command)


@app.command(rich_help_panel='Deployment')
def build(draft: Annotated[bool, Option(help='Build including drafts.')] = Config.select('deploy.draft')):
    """Build jekyll site."""
    if Config.root is not None:
        os.chdir(Config.root)
    command = 'bundle exec jekyll build'
    if draft:
        command += ' --drafts'
    os.system(command)


@app.command(rich_help_panel='Operation')
def info(name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))]):
    """Show info about post or draft."""
    items = Blog.find(name)
    if len(items) == 0:
        print('[bold red]No such item.')
        return

    item = items[0] if len(items) == 1 else select(
        message=f'Found {len(items)} matches, select one to check:',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )
    rule('[bold green]Info')
    print_info(item.info())


@app.command(name='list', rich_help_panel='Operation')
def list_items(
    name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))] = None,
    draft: Annotated[bool, Option('--draft', '-d', help='List only all drafts.')] = False,
    post: Annotated[bool, Option('--post', '-p', help='List only all posts.')] = False,
):
    """List all posts and drafts or find items by name."""
    match (draft, post):
        case (True, False):
            drafts, posts = (Blog.find(name, BlogType.Draft) if name is not None else Blog.drafts, None)
        case (False, True):
            drafts, posts = (None, Blog.find(name, BlogType.Post) if name is not None else Blog.posts)
        case _:
            if name is not None:
                items = Blog.find(name)
                drafts = [item for item in items if item.type == BlogType.Draft]
                posts = [item for item in items if item.type == BlogType.Post]
            else:
                drafts, posts = (Blog.drafts, Blog.posts)
    if posts is not None:
        print_table(posts, title='[bold green]Posts', show_header=False)
    if drafts is not None:
        print_table(drafts, title='[bold green]Drafts', show_header=False)


@app.command(name='open', rich_help_panel='Operation')
def open_item(
    name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))]
):
    """Open post or draft in editor."""
    items = Blog.find(name)
    if len(items) == 0:
        print(f'[bold red]No such item.')
        return

    item = items[0] if len(items) == 1 else select(
        message=f'Found {len(items)} matches, select one to open:',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )
    with Progress(f'Opening {item.file_path}'):
        item.open()


@app.command(rich_help_panel='Operation')
def draft(
    name: Annotated[str, Argument(help='Name of draft item.')],
    title: Annotated[str, Option('--title', '-t', help='Title of draft.')] = None,
    class_: Annotated[List[str], Option('--class', '-c', help='Categories of draft.')] = None,
    tag: Annotated[List[str], Option('--tag', '-g', help='Tags of draft.')] = None,
    open_: Annotated[bool, Option('--open', '-o', help='Open draft after creation.')] = False
):
    """Create a draft."""
    item = Item(name, BlogType.Draft)
    if item in Blog:
        print(f'[bold red]Draft "{item.name}" already exists.')
        return
    item.create(title, class_, tag)
    print(f'[bold]{item.file_path} [green]created as draft successfully.')
    if open_:
        with Progress('Opening draft...'):
            item.open()


@app.command(rich_help_panel='Operation')
def post(
    name: Annotated[str, Argument(help='Name of post item.')],
    title: Annotated[str, Option('--title', '-t', help='Title of post.')] = None,
    class_: Annotated[List[str], Option('--class', '-c', help='Categories of post.')] = None,
    tag: Annotated[List[str], Option('--tag', '-g', help='Tags of post.')] = None,
    open_: Annotated[bool, Option('--open', '-o', help='Open post after creation.')] = False
):
    """Create a post."""
    item = Item(name, BlogType.Post)
    if item in Blog:
        print(f'[bold red]Post "{item.name}" already exists.')
        return
    item.create(title, class_, tag)
    print(f'[bold]{item.file_path} [green]created as post successfully.')
    if open_:
        with Progress('Opening post...'):
            item.open()


@app.command(rich_help_panel='Operation')
def remove(name: Annotated[str, Argument(help='Name of post or draft.', autocompletion=complete_items(Blog.articles))]):
    """Remove a post or draft."""
    items = Blog.find(name)
    if len(items) == 0:
        print(f'[bold red]No such item.')
        return

    selected_items = items[0] if len(items) == 1 else check(
        message=f'Found {len(items)} matches, select items to remove (Ctrl+A to select all, Ctrl+R to toggle selection):',
        choices={f'[{item.type.name}] {item.name}': item for item in items}
    )
    for i, item in enumerate(selected_items):
        print(f'{i + 1}. {item}')
    if confirm(f'Found {len(items)} matches, remove above items?'):
        for item in items:
            item.remove()
        print('[bold green]Remove successfully.')


@app.command(rich_help_panel='Operation')
def publish(name: Annotated[str, Argument(help='Name of draft.', autocompletion=complete_items(Blog.drafts))]):
    """Publish a draft."""
    items = Blog.find(name, BlogType.Draft)

    if len(items) == 0:
        print_table(Blog.drafts, title='[bold green]Drafts', show_header=False)
        print('[bold red]No such item in _drafts.')
        return

    if len(items) != 1:
        items = check(
            message=f'Found {len(items)} matches, select items to publish (Ctrl+A to select all, Ctrl+R to toggle selection):',
            choices={f'[{item.type.name}] {item.name}': item for item in items}
        )
    for item in items:
        item.publish()
        print(f'Draft "{item.name}" published as "{item.file_path}"')


@app.command(rich_help_panel='Operation')
def unpublish(name: Annotated[str, Argument(help='Name of post.', autocompletion=complete_items(Blog.posts))]):
    """Unpublish a post."""
    items = Blog.find(name, BlogType.Post)

    if len(items) == 0:
        print_table(Blog.posts, title='[bold green]Posts', show_header=False)
        print('[bold red]No such item in _posts.')
        return

    if len(items) != 1:
        items = check(
            message=f'Found {len(items)} matches, select items to unpublish (Ctrl+A to select all, Ctrl+R to toggle selection):',
            choices={f'[{item.type.name}] {item.name}': item for item in items}
        )
    for item in items:
        item.unpublish()
        print(f'Post "{item.name}" unpublished as "{item.file_path}"')


@app.command(rich_help_panel='Configuration')
def init():
    """Initialize the application interactively."""
    print('[bold green]Welcome to the Jekyll CLI application!:wave::wave::wave:')
    print("Let's set up your basic configuration.:wink:")
    root = input_directory_path('Please enter the root path of your blog:')
    mode = select(
        message='Please choose the management mode (single or item):',
        choices={
            'single (A single markdown file denotes a blog item.)': 'single',
            'item (A directory containing a markdown file and an assets directory denotes a blog item.)': 'item'
        }
    )

    rule()
    print('You have entered the following configurations:')
    print_info({'Blog root path': str(root), 'Management mode': mode})

    if confirm('Confirm your basic configurations?', default=True):
        Config.merge({'root': str(root), 'mode': mode})
        print('[bold green]Basic configuration set up successfully!')
        print('[bold]Type "--help" for more information.')
    else:
        print('[bold red]Aborted.')
