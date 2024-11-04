import click
from .qr_processor import QRHashCombiner

@click.group()
def main():
    """DecentryK QR - A tool for combining and verifying QR codes."""
    pass

@main.command()
@click.option('--files', nargs=2, required=True, help='Two QR code files to process')
@click.option('--output', default='combined_qr.png', help='Output file for combined QR code')
def combine(files, output):
    """Combine two QR codes into a new QR code with combined hash."""
    try:
        qr1_path, qr2_path = files
        processor = QRHashCombiner()
        
        # Process QR codes
        combined_hash, hash_data = processor.process_qr_codes(qr1_path, qr2_path, output)
        
        click.echo(click.style("✓ QR codes combined successfully!", fg='green'))
        click.echo(f"Combined QR code created: {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()