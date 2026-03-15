![IFoundYou banner](assets/banner.svg)

# IFoundYou

`IFoundYou` is a practical host-inspection CLI for Windows and Linux. Once installed, you use it like a normal command: `ifoundyou <ip-or-domain>`. It turns that target into a readable report with DNS resolution, geolocation context, provider data, TLS certificate details, map links, JSON output, and Markdown exports.

It started as a tiny bash geolocation script. This new version keeps the original spirit, but upgrades it into a real tool that people can use for support work, homelabs, blue-team triage, bug reports, web diagnostics, and quick network sanity checks.

![IFoundYou demo report](assets/demo-report.svg)

## Usage

```bash
ifoundyou <ip-or-domain>
```

Examples:

```bash
ifoundyou 8.8.8.8
ifoundyou github.com
ifoundyou https://openai.com
```

## Why this is useful

- Inspect domains, raw IPs, and URLs with one command.
- Run the same workflow on Windows PowerShell and Linux shells.
- Resolve DNS locally before geolocation, which makes domain lookups more reliable.
- Pull provider and ASN context fast when you need to understand who is behind an endpoint.
- Summarize TLS certificate identity and validity for HTTPS targets.
- Export reports as JSON for automation or Markdown for incident notes and tickets.
- Check your own public IP with `--self`.

## Quick start

### Windows

```powershell
git clone https://github.com/sularhen/IFoundYou.git
cd IFoundYou
python -m pip install -e .
ifoundyou github.com
```

You can also use the included PowerShell wrapper:

```powershell
.\whereareyou.ps1 github.com
```

### Linux

```bash
git clone https://github.com/sularhen/IFoundYou.git
cd IFoundYou
python3 -m pip install -e .
ifoundyou github.com
```

Or keep the original feel with the legacy wrapper:

```bash
chmod +x whereareyou.sh
./whereareyou.sh github.com
```

## Releases

For simple downloads outside git, the project is prepared for two release artifacts:

- `ifoundyou-windows-<version>.zip`
- `ifoundyou-linux-<version>.tar.gz`

### Windows release

1. Download and extract the `.zip`.
2. Open PowerShell inside the extracted folder.
3. Run:

```powershell
.\install.ps1
```

After installation, open a new terminal and use:

```powershell
ifoundyou github.com
```

### Linux release

1. Download and extract the `.tar.gz`.
2. Open a terminal inside the extracted folder.
3. Run:

```bash
chmod +x install.sh
./install.sh
```

After installation, use:

```bash
ifoundyou github.com
```

## Example commands

```bash
ifoundyou github.com
ifoundyou https://openai.com --json
ifoundyou --self
ifoundyou --batch targets.txt --save reports/team-scan.md
ifoundyou 8.8.8.8 --save reports/dns.json
```

## Example output

```text
IFoundYou Report
========================================================
Input            github.com
Host             github.com
Primary IP       4.228.31.150
IPv4             4.228.31.150

Location
--------------------------------------------------------
Country          Brazil
Region           State of Sao Paulo
City             Campinas

Provider
--------------------------------------------------------
ISP              Microsoft Corporation
Organization     Microsoft Corporation
ASN              8075

TLS Certificate
--------------------------------------------------------
Common Name      github.com
Issuer           Sectigo Public Server Authentication CA DV E36
```

## Command reference

```text
usage: ifoundyou [-h] [--self] [--batch BATCH] [--json] [--save SAVE]
                 [--timeout TIMEOUT] [--no-ssl]
                 [target]
```

- `target`: IP, domain, or URL.
- `--self`: inspect your current public IP.
- `--batch`: load targets from a text file, one per line.
- `--json`: print structured JSON.
- `--save`: export to `.json` or `.md`.
- `--timeout`: override the network timeout.
- `--no-ssl`: skip certificate checks.

## How it works

1. The target is normalized from an IP, domain, or URL.
2. DNS is resolved locally using the Python standard library.
3. A public geolocation API is queried for the resolved IP.
4. TLS metadata is collected directly from the remote server when applicable.
5. Everything is merged into one human-readable or machine-readable report.

## Project structure

```text
.
|-- assets/
|   |-- banner.svg
|   `-- demo-report.svg
|-- src/ifoundyou/
|   |-- cli.py
|   |-- core.py
|   `-- formatters.py
|-- tests/
|   `-- test_core.py
|-- whereareyou.ps1
`-- whereareyou.sh
```

## Privacy note

`IFoundYou` performs local DNS and TLS inspection on your machine, and uses public web services for public IP detection and geolocation enrichment. That means the inspected IP may be sent to those external services during lookup. For local-only scenarios, disable the tool or adapt the providers for your own environment.

## Development

```bash
python -m unittest discover -s tests -v
```

To build release artifacts locally:

```bash
python scripts/build_release.py
```

This generates:

- `dist/ifoundyou-windows-2.0.1.zip`
- `dist/ifoundyou-linux-2.0.1.tar.gz`

## License

MIT

---

# IFoundYou en Espanol

`IFoundYou` es una CLI practica de inspeccion de hosts para Windows y Linux. Una vez instalada, se usa como un comando normal: `ifoundyou <ip-o-dominio>`. Le pasas una IP, un dominio o una URL completa y la herramienta lo convierte en un reporte legible con resolucion DNS, contexto de geolocalizacion, datos del proveedor, detalles del certificado TLS, enlaces a mapas, salida JSON y exportaciones en Markdown.

Nacio como un script bash pequeno de geolocalizacion. Esta nueva version mantiene la idea original, pero la convierte en una herramienta real para soporte, homelabs, triage defensivo, reportes de bugs, diagnostico web y comprobaciones rapidas de red.

## Uso

```bash
ifoundyou <ip-o-dominio>
```

Ejemplos:

```bash
ifoundyou 8.8.8.8
ifoundyou github.com
ifoundyou https://openai.com
```

## Por que esto es util

- Inspecciona dominios, IPs y URLs con un solo comando.
- Funciona con el mismo flujo en Windows PowerShell y en terminales Linux.
- Resuelve DNS localmente antes de geolocalizar, lo que hace las consultas mas confiables.
- Obtiene rapido contexto del proveedor y ASN para entender quien esta detras de un endpoint.
- Resume identidad y validez del certificado TLS en objetivos HTTPS.
- Exporta reportes como JSON para automatizacion o Markdown para tickets e informes.
- Permite revisar tu IP publica actual con `--self`.

## Inicio rapido

### Windows

```powershell
git clone https://github.com/sularhen/IFoundYou.git
cd IFoundYou
python -m pip install -e .
ifoundyou github.com
```

Tambien puedes usar el wrapper incluido para PowerShell:

```powershell
.\whereareyou.ps1 github.com
```

### Linux

```bash
git clone https://github.com/sularhen/IFoundYou.git
cd IFoundYou
python3 -m pip install -e .
ifoundyou github.com
```

O mantener la experiencia del script original:

```bash
chmod +x whereareyou.sh
./whereareyou.sh github.com
```

## Releases

Para descargas sencillas fuera de git, el proyecto ya esta preparado con dos artefactos de release:

- `ifoundyou-windows-<version>.zip`
- `ifoundyou-linux-<version>.tar.gz`

### Release para Windows

1. Descarga y extrae el `.zip`.
2. Abre PowerShell dentro de la carpeta extraida.
3. Ejecuta:

```powershell
.\install.ps1
```

Despues de instalar, abre una terminal nueva y usa:

```powershell
ifoundyou github.com
```

### Release para Linux

1. Descarga y extrae el `.tar.gz`.
2. Abre una terminal dentro de la carpeta extraida.
3. Ejecuta:

```bash
chmod +x install.sh
./install.sh
```

Despues de instalar, usa:

```bash
ifoundyou github.com
```

## Comandos de ejemplo

```bash
ifoundyou github.com
ifoundyou https://openai.com --json
ifoundyou --self
ifoundyou --batch targets.txt --save reports/team-scan.md
ifoundyou 8.8.8.8 --save reports/dns.json
```

## Ejemplo de salida

```text
IFoundYou Report
========================================================
Input            github.com
Host             github.com
Primary IP       4.228.31.150
IPv4             4.228.31.150

Location
--------------------------------------------------------
Country          Brazil
Region           State of Sao Paulo
City             Campinas

Provider
--------------------------------------------------------
ISP              Microsoft Corporation
Organization     Microsoft Corporation
ASN              8075

TLS Certificate
--------------------------------------------------------
Common Name      github.com
Issuer           Sectigo Public Server Authentication CA DV E36
```

## Referencia de comandos

```text
usage: ifoundyou [-h] [--self] [--batch BATCH] [--json] [--save SAVE]
                 [--timeout TIMEOUT] [--no-ssl]
                 [target]
```

- `target`: IP, dominio o URL.
- `--self`: inspecciona tu IP publica actual.
- `--batch`: carga objetivos desde un archivo de texto, uno por linea.
- `--json`: imprime JSON estructurado.
- `--save`: exporta a `.json` o `.md`.
- `--timeout`: cambia el tiempo maximo de red.
- `--no-ssl`: omite la inspeccion del certificado.

## Como funciona

1. El objetivo se normaliza desde una IP, dominio o URL.
2. El DNS se resuelve localmente con la libreria estandar de Python.
3. Se consulta una API publica de geolocalizacion con la IP resultante.
4. Se obtienen metadatos TLS directamente del servidor remoto cuando aplica.
5. Todo se une en un unico reporte legible para personas o maquinas.

## Estructura del proyecto

```text
.
|-- assets/
|   |-- banner.svg
|   `-- demo-report.svg
|-- src/ifoundyou/
|   |-- cli.py
|   |-- core.py
|   `-- formatters.py
|-- tests/
|   `-- test_core.py
|-- whereareyou.ps1
`-- whereareyou.sh
```

## Nota de privacidad

`IFoundYou` realiza inspeccion DNS y TLS localmente en tu maquina, y usa servicios web publicos para detectar la IP publica y enriquecer la geolocalizacion. Eso significa que la IP inspeccionada puede enviarse a servicios externos durante la consulta. Para escenarios completamente locales, puedes desactivar esa parte o adaptar los proveedores a tu entorno.

## Desarrollo

```bash
python -m unittest discover -s tests -v
```

Para construir los artefactos de release localmente:

```bash
python scripts/build_release.py
```

Esto genera:

- `dist/ifoundyou-windows-2.0.1.zip`
- `dist/ifoundyou-linux-2.0.1.tar.gz`

## Licencia

MIT
