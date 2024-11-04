import click
import json
import os
from .qr_processor import QRHashCombiner
from datetime import datetime
import secrets
import base64

@click.group()
def main():
    """DecentryK QR - A tool for combining and verifying QR codes with enhanced security."""
    pass

@main.command()
@click.option('--files', nargs=2, required=True, help='Two QR code files to process')
@click.option('--output', default='combined_qr.png', help='Output file for combined QR code')
@click.option('--secret-key', help='Optional secret key for hashing')
@click.option('--hash-file', default='hash_data.json', help='File to store hash information')
def combine(files, output, secret_key, hash_file):
    """Combine two QR codes into a new QR code with enhanced security."""
    try:
        qr1_path, qr2_path = files
        
        # Create processor with optional secret key
        processor = QRHashCombiner(secret_key)
        
        # Process QR codes
        click.echo("Processing QR codes...")
        combined_hash, hash_data = processor.process_qr_codes(qr1_path, qr2_path, output)
        
        # Store hash information
        with open(hash_file, 'w') as f:
            json.dump(hash_data, f, indent=2)
        
        click.echo(click.style("✓ QR codes combined successfully!", fg='green'))
        click.echo(f"Combined QR code: {output}")
        click.echo(f"Hash data stored: {hash_file}")
        click.echo(f"\nMetadata:")
        click.echo(f"  Version: {hash_data['metadata']['version']}")
        click.echo(f"  Timestamp: {hash_data['metadata']['timestamp']}")
        click.echo(f"  Algorithm: {hash_data['metadata']['algorithm']}")
        
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'), err=True)
        raise click.Abort()

@main.command()
@click.option('--files', nargs=2, required=True, help='Two QR code files to verify')
@click.option('--hash-file', default='hash_data.json', help='JSON file containing stored hash information')
@click.option('--secret-key', help='Secret key used for original hashing')
def verify(files, hash_file, secret_key):
    """Verify two QR codes against a stored hash with enhanced security."""
    try:
        if not os.path.exists(hash_file):
            raise click.ClickException(f"Hash file not found: {hash_file}")
            
        # Load stored hash data
        with open(hash_file, 'r') as f:
            stored_hash_data = json.load(f)
        
        qr1_path, qr2_path = files
        processor = QRHashCombiner(secret_key)
        
        # Verify QR codes
        click.echo("Verifying QR codes...")
        is_valid, message, details = processor.verify_qr_codes(
            qr1_path,
            qr2_path,
            stored_hash_data
        )
        
        if is_valid:
            click.echo(click.style("✓ QR codes verified successfully!", fg='green'))
            click.echo(f"\nVerification Details:")
            click.echo(f"  Time: {details['verification_time']}")
            click.echo(f"  Original Timestamp: {stored_hash_data['metadata']['timestamp']}")
        else:
            click.echo(click.style("✗ QR code verification failed!", fg='red'))
            click.echo(f"Reason: {message}")
            if 'error' in details:
                click.echo(f"Error details: {details['error']}")
            
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'), err=True)
        raise click.Abort()

@main.command()
@click.option('--length', default=32, help='Length of the secret key in bytes')
def generate_key(length):
    """Generate a new secret key for hashing."""
    try:
        key = base64.b64encode(secrets.token_bytes(length)).decode('utf-8')
        click.echo("Generated Secret Key:")
        click.echo(key)
    except Exception as e:
        click.echo(click.style(f"Error generating key: {str(e)}", fg='red'), err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()