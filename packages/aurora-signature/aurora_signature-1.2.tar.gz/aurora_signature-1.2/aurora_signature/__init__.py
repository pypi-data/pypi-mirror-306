import click
from .main import sign

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-to', '--api_token', type=str, help='API Token', required=True)
@click.option('-te', '--tenant_id', type=str, help='TenantID', required=True)
@click.option('-p', '--pki', type=str, help='Certificate Type', required=True)

def sign(input_file, output_file, api_token, tenant_id, pki):
    """Sign document"""
    logo = """
    +------------------------------+
    | Sign document by Paperlogic  |
    +------------------------------+
    """
    click.echo(f"Start Signing")
    sign(input_file, output_file, api_token, tenant_id, pki)
    click.echo(f"Complete Signing")
    
    click.echo(logo)
