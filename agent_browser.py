#!/usr/bin/env python3
"""
Agent Browser - Browser automation CLI for AI agents

Fast, Python-based browser automation using Playwright.
"""

import click
import sys
from src.browser import BrowserAgent


@click.group()
@click.option('--headless/--headed', default=True, help='Run browser in headless mode')
@click.option('--viewport', default='1280x720', help='Viewport size (e.g., 1920x1080)')
@click.option('--device', help='Emulate device (e.g., "iPhone 14")')
@click.pass_context
def cli(ctx, headless, viewport, device):
    """Agent Browser - Browser automation for AI agents
    
    Fast, Python-based browser automation using Playwright.
    
    Examples:
    
    \b
        # Open a URL
        agent-browser open https://example.com
        
        # Get accessibility snapshot
        agent-browser snapshot -i
        
        # Click element
        agent-browser click "#submit"
        
        # Fill form
        agent-browser fill "#email" "test@example.com"
        
        # Take screenshot
        agent-browser screenshot page.png
    """
    ctx.ensure_object(dict)
    ctx.obj['headless'] = headless
    ctx.obj['viewport'] = viewport
    ctx.obj['device'] = device


@cli.command()
@click.argument('url')
@click.pass_context
def open(ctx, url):
    """Open a URL in the browser
    
    URL: URL to navigate to
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.open(url)
        click.echo(f"✓ Opened: {url}")
    finally:
        agent.close()


@cli.command()
@click.option('-i', '--interactive', is_flag=True, help='Interactive elements only')
@click.option('-c', '--compact', is_flag=True, help='Compact output')
@click.option('-d', '--depth', type=int, help='Limit tree depth')
@click.option('-s', '--selector', help='Scope to CSS selector')
@click.pass_context
def snapshot(ctx, interactive, compact, depth, selector):
    """Get accessibility tree snapshot
    
    Options:
    
    \b
        -i, --interactive  Only show interactive elements
        -c, --compact      Remove empty structural elements
        -d, --depth        Limit tree depth
        -s, --selector     Scope to CSS selector
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        tree = agent.snapshot(interactive=interactive, compact=compact, depth=depth)
        click.echo(tree)
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.option('--new-tab', is_flag=True, help='Open in new tab')
@click.pass_context
def click(ctx, selector, new_tab):
    """Click an element
    
    SELECTOR: CSS selector or element ref (e.g., @e1)
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.click(selector)
        click.echo(f"✓ Clicked: {selector}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.argument('text')
@click.pass_context
def fill(ctx, selector, text):
    """Fill an input field
    
    SELECTOR: CSS selector for input field
    
    TEXT: Text to fill
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.fill(selector, text)
        click.echo(f"✓ Filled: {selector}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.argument('text')
@click.pass_context
def type(ctx, selector, text):
    """Type into an element (with key events)
    
    SELECTOR: CSS selector for input field
    
    TEXT: Text to type
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.fill(selector, text)  # Using fill for now
        click.echo(f"✓ Typed: {text} into {selector}")
    finally:
        agent.close()


@cli.command()
@click.argument('path', default='screenshot.png')
@click.option('--full', is_flag=True, help='Full page screenshot')
@click.option('--annotate', is_flag=True, help='Annotate with element labels')
@click.pass_context
def screenshot(ctx, path, full, annotate):
    """Take a screenshot
    
    PATH: Output file path (default: screenshot.png)
    
    Options:
    
    \b
        --full       Full page screenshot
        --annotate   Annotate with element labels
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.screenshot(path, full_page=full)
        click.echo(f"✓ Screenshot saved: {path}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def get_text(ctx, selector):
    """Get text content of an element
    
    SELECTOR: CSS selector
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        text = agent.get_text(selector)
        click.echo(text)
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def get_html(ctx, selector):
    """Get innerHTML of an element
    
    SELECTOR: CSS selector
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        html = agent.get_html(selector)
        click.echo(html)
    finally:
        agent.close()


@cli.command()
@click.pass_context
def get_url(ctx):
    """Get current URL"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent._ensure_browser()
        click.echo(agent.page.url)
    finally:
        agent.close()


@cli.command()
@click.pass_context
def get_title(ctx):
    """Get page title"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent._ensure_browser()
        click.echo(agent.page.title())
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def is_visible(ctx, selector):
    """Check if element is visible
    
    SELECTOR: CSS selector
    """
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        visible = agent.is_visible(selector)
        click.echo(f"{'✓ Visible' if visible else '✗ Hidden'}")
    finally:
        agent.close()


@cli.command()
@click.pass_context
def close(ctx):
    """Close the browser"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    agent.close()
    click.echo("✓ Browser closed")


@cli.command()
@click.argument('selector', required=False)
@click.option('--timeout', type=int, default=30000, help='Timeout in ms')
@click.option('--state', default='visible', help='Wait state')
@click.option('--text', help='Wait for text')
@click.option('--url', help='Wait for URL')
@click.option('--load', help='Wait for load state')
@click.pass_context
def wait(ctx, selector, timeout, state, text, url, load):
    """Wait for element, text, URL, or network idle"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.wait(selector=selector, timeout=timeout, state=state, text=text, url=url, load=load)
        click.echo("✓ Wait completed")
    finally:
        agent.close()


@cli.command()
@click.option('--role', help='ARIA role')
@click.option('--text', help='Text content')
@click.option('--label', help='Label text')
@click.option('--placeholder', help='Placeholder text')
@click.option('--testid', help='data-testid value')
@click.option('--action', help='Action to perform')
@click.option('--name', help='Accessible name')
@click.option('--exact', is_flag=True, help='Exact match')
@click.pass_context
def find(ctx, role, text, label, placeholder, testid, action, name, exact):
    """Find elements using semantic locators"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        result = agent.find(role=role, text=text, label=label, placeholder=placeholder,
                          testid=testid, action=action, name=name, exact=exact)
        click.echo(f"✓ Found: {result}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.argument('key')
@click.pass_context
def press(ctx, selector, key):
    """Press a key on an element"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.press(selector, key)
        click.echo(f"✓ Pressed: {key}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def hover(ctx, selector):
    """Hover over an element"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.hover(selector)
        click.echo(f"✓ Hovered: {selector}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def check(ctx, selector):
    """Check a checkbox"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.check(selector)
        click.echo(f"✓ Checked: {selector}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def uncheck(ctx, selector):
    """Uncheck a checkbox"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.uncheck(selector)
        click.echo(f"✓ Unchecked: {selector}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.argument('value')
@click.pass_context
def select(ctx, selector, value):
    """Select dropdown option"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.select(selector, value)
        click.echo(f"✓ Selected: {value}")
    finally:
        agent.close()


@cli.command()
@click.argument('direction', default='down')
@click.argument('pixels', type=int, default=100)
@click.option('--selector', help='Element selector')
@click.pass_context
def scroll(ctx, direction, pixels, selector):
    """Scroll page or element"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.scroll(selector=selector, direction=direction, pixels=pixels)
        click.echo(f"✓ Scrolled {direction} {pixels}px")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.argument('files', nargs=-1)
@click.pass_context
def upload(ctx, selector, files):
    """Upload files"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        agent.upload(selector, list(files))
        click.echo(f"✓ Uploaded: {len(files)} files")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def get_value(ctx, selector):
    """Get input value"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        value = agent.get_value(selector)
        click.echo(value)
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.argument('attribute')
@click.pass_context
def get_attr(ctx, selector, attribute):
    """Get element attribute"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        attr = agent.get_attribute(selector, attribute)
        click.echo(attr)
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def get_box(ctx, selector):
    """Get element bounding box"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        box = agent.get_box(selector)
        click.echo(f"X: {box.get('x', 0)}, Y: {box.get('y', 0)}, Width: {box.get('width', 0)}, Height: {box.get('height', 0)}")
    finally:
        agent.close()


@cli.command()
@click.argument('selector')
@click.pass_context
def count(ctx, selector):
    """Count matching elements"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        cnt = agent.count(selector)
        click.echo(f"Count: {cnt}")
    finally:
        agent.close()


@cli.command()
@click.argument('javascript')
@click.pass_context
def eval(ctx, javascript):
    """Execute JavaScript"""
    agent = BrowserAgent(headless=ctx.obj['headless'])
    try:
        result = agent.eval(javascript)
        click.echo(result)
    finally:
        agent.close()


@cli.command()
@click.pass_context
def install(ctx):
    """Install Playwright browsers"""
    click.echo("Installing Playwright browsers...")
    import subprocess
    result = subprocess.run([sys.executable, '-m', 'playwright', 'install'], capture_output=True, text=True)
    if result.returncode == 0:
        click.echo("✓ Playwright browsers installed successfully")
    else:
        click.echo(f"✗ Installation failed: {result.stderr}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
