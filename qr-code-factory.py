import typer
import qrcode
import os
from PIL import Image
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

def create_qr(data: str, filename: str, fill_color: str = "black", back_color: str = "white"):
    """
    Core function to generate QR Code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction (biar tetep kebaca meski agak burem)
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    try:
        # Create Image with Colors
        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
        
        # Save File
        if not filename.endswith(".png"):
            filename += ".png"
            
        img.save(filename)
        
        console.print(Panel(f"[bold green]✅ QR CODE GENERATED![/bold green]\nSaved as: [underline]{filename}[/underline]\nData: {data}", title="QR Factory"))
        
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")

@app.command()
def link(url: str, name: str = "qr_link", color: str = "black", bg: str = "white"):
    """
    Create a QR Code for a Website URL.
    Usage: python qr-factory.py link "https://google.com" --name "my_site" --color "blue"
    """
    console.print(f"[cyan]Generating QR for Link: {url}...[/cyan]")
    create_qr(url, name, color, bg)

@app.command()
def wifi(ssid: str, password: str, encryption: str = "WPA", name: str = "qr_wifi"):
    """
    Create a QR Code for WiFi Login (Auto-Connect).
    Usage: python qr-factory.py wifi "NamaWiFi" "Password123"
    """
    # Format WiFi: WIFI:T:WPA;S:MyNetwork;P:mypass;;
    wifi_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    
    console.print(f"[cyan]Generating QR for WiFi: {ssid}...[/cyan]")
    create_qr(wifi_data, name, fill_color="blue", back_color="white") # Default WiFi warna Biru

@app.command()
def vcard(name: str, phone: str, email: str, filename: str = "qr_contact"):
    """
    Create a QR Code for Digital Business Card (Save Contact).
    Usage: python qr-factory.py vcard "John Doe" "08123456789" "john@email.com"
    """
    # Format VCard
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{name}
TEL:{phone}
EMAIL:{email}
END:VCARD"""
    
    console.print(f"[cyan]Generating Contact QR for: {name}...[/cyan]")
    create_qr(vcard_data, filename, fill_color="black", back_color="yellow") # Default Kartu Nama Background Kuning

if __name__ == "__main__":
    app()