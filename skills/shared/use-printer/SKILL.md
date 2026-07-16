---
name: use-printer
description: Print local documents via CUPS. Use when asked to print files, HTML, PDFs, reports, or to check printer/default duplex settings.
---

# Use Printer

## Workflow

1. Locate the file to print.
   - If the user refers to “the HTML” or “the report,” inspect the recent working directory or relevant project folder rather than asking immediately.
   - Prefer printing from a stable local path.

2. Inspect printer state and defaults.

```bash
lpstat -p -d
lpoptions
lpoptions -p <printer-name> -l
```

3. Choose the printer.
   - If the user says “Brother” or “brothers,” use `Brother_HL_L2325DW` when available.
   - If no printer is specified, use the system default from `lpstat -d`.

4. Check duplex settings.
   - For the Brother printer, `Duplex=DuplexNoTumble` means double-sided long-edge.
   - `Duplex=DuplexTumble` means double-sided short-edge.
   - `Duplex=None` means single-sided.
   - Set duplex explicitly when the user asks for double-sided, even if it is already the default. Always use double-sided as the default.

5. Convert HTML before printing.
   - Do not send `.html` directly to `lp`; CUPS may reject it with `Unsupported document-format "text/html"`.
   - Render HTML to PDF first with headless Chrome, then print the PDF.

```bash
HTML="/absolute/path/to/file.html"
PDF="${HTML%.html}.print.pdf"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-first-run --print-to-pdf="$PDF" "file://$HTML"
```

6. Print.

```bash
lp -d <printer-name> \
  -o Duplex=DuplexNoTumble \
  -o sides=two-sided-long-edge \
  -o media=Letter \
  /absolute/path/to/file.pdf
```

7. Verify the job was accepted and monitor briefly.

```bash
lpstat -o <printer-name>
lpstat -p <printer-name>
```

Report the printer used, whether duplex was explicit/default, and any named blocker. If the job remains queued with a printer-side wait, say that plainly rather than implying completion.
