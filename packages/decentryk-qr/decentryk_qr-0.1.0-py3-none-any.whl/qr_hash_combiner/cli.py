import click
import json
import os
from .qr_processor import QRHashCombiner
from datetime import datetime

@click.group()
def main():
    """DecentryK QR - A tool for combining and verifying QR codes."""
    pass

@main.command()
@click.option('--files', nargs=2, required=True, help='Two QR code files to process')
@click.option('--output', default='combined_qr.png', help='Output file for combined QR code')
@click.option('--store-hash/--no-store-hash', default=True, help='Store hash information in JSON file')
def combine(files, output, store_hash):
    """Combine two QR codes into a new QR code with combined hash."""
    try:
        qr1_path, qr2_path = files
        processor = QRHashCombiner()
        
        # Process QR codes
        combined_hash, hash1, hash2 = processor.process_qr_codes(qr1_path, qr2_path, output)
        
        # Store hash information
        if store_hash:
            hash_data = {
                'timestamp': datetime.now().isoformat(),
                'combined_hash': combined_hash,
                'qr1': {
                    'path': qr1_path,
                    'hash': hash1
                },
                'qr2': {
                    'path': qr2_path,
                    'hash': hash2
                }
            }
            
            hash_file = 'combined_hash.json'
            with open(hash_file, 'w') as f:
                json.dump(hash_data, f, indent=2)
            
            click.echo(f"Hash information stored in {hash_file}")
        
        click.echo(f"Combined QR code created: {output}")
        click.echo(f"Combined Hash: {combined_hash}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@main.command()
@click.option('--files', nargs=2, required=True, help='Two QR code files to verify')
@click.option('--hash-file', default='combined_hash.json', help='JSON file containing stored hash information')
def verify(files, hash_file):
    """Verify two QR codes against a previously stored combined hash."""
    try:
        if not os.path.exists(hash_file):
            raise click.ClickException(f"Hash file not found: {hash_file}")
            
        # Load stored hash
        with open(hash_file, 'r') as f:
            stored_data = json.load(f)
        
        qr1_path, qr2_path = files
        processor = QRHashCombiner()
        
        # Verify QR codes
        is_valid, current_hash, expected_hash = processor.verify_qr_codes(
            qr1_path,
            qr2_path,
            stored_data['combined_hash']
        )
        
        if is_valid:
            click.echo(click.style("✓ QR codes verified successfully!", fg='green'))
        else:
            click.echo(click.style("✗ QR code verification failed!", fg='red'))
            click.echo(f"Current hash:   {current_hash}")
            click.echo(f"Expected hash:  {expected_hash}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()