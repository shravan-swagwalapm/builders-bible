#!/usr/bin/env python3
"""
The Builder's Bible — PDF Build Script
Combines markdown chapters into a single HTML, then generates PDF via WeasyPrint.
"""

import os
import sys
import re
try:
    import yaml
except ImportError:
    yaml = None
import markdown
from markdown.extensions import tables, toc, fenced_code
from pathlib import Path
from datetime import datetime

# Add weasyprint to path if needed
sys.path.insert(0, os.path.expanduser('~/Library/Python/3.9/lib/python/site-packages'))

BOOK_DIR = Path(__file__).parent.parent / 'book'
BUILD_DIR = Path(__file__).parent
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
CSS_FILE = BUILD_DIR / 'book.css'

# Chapter order — the spine of the book
CHAPTER_ORDER = [
    # Frontmatter
    'frontmatter/title-page.md',
    'frontmatter/copyright.md',
    'frontmatter/foreword.md',
    'frontmatter/about-the-author.md',
    'frontmatter/table-of-contents.md',
    'frontmatter/how-to-read.md',
    'frontmatter/state-of-the-art.md',

    # Part 0
    'part-0/part-intro.md',
    'part-0/ch-00-1-computer-not-fragile.md',
    'part-0/ch-00-2-setting-up.md',
    'part-0/ch-00-3-first-conversation.md',

    # Part I
    'part-1/part-intro.md',
    'part-1/ch-01-internet.md',
    'part-1/ch-02-frontend.md',
    'part-1/ch-03-backend.md',
    'part-1/ch-04-databases.md',
    'part-1/ch-05-version-control.md',
    'part-1/ch-06-deployment.md',
    'part-1/ch-07-testing.md',
    'part-1/ch-08-architecture.md',
    'projects/project-01.md',

    # Part II
    'part-2/part-intro.md',
    'part-2/ch-09-ai-history.md',
    'part-2/ch-10-llms.md',
    'part-2/ch-11-prompt-engineering.md',
    'part-2/ch-12-embeddings.md',
    'part-2/ch-13-rag.md',
    'part-2/ch-14-fine-tuning.md',
    'part-2/ch-15-agents.md',
    'part-2/ch-16-mcp.md',
    'part-2/ch-17-multimodal.md',
    'part-2/ch-18-evaluations.md',
    'projects/project-02.md',

    # Part III
    'part-3/part-intro.md',
    'part-3/ch-19-claude-code.md',
    'part-3/ch-20-ai-landscape.md',
    'part-3/ch-21-design-systems.md',
    'part-3/ch-22-production-chatbot.md',
    'part-3/ch-23-multi-agent.md',
    'projects/project-03.md',

    # Part IV
    'part-4/part-intro.md',
    'part-4/ch-24-system-design.md',
    'part-4/ch-25-analytics.md',
    'part-4/ch-26-token-economics.md',
    'part-4/ch-27-cicd.md',
    'part-4/ch-28-security.md',
    'part-4/ch-29-open-source.md',

    # Part V
    'part-5/part-intro.md',
    'part-5/ch-30-compound-ai.md',
    'part-5/ch-31-reasoning.md',
    'part-5/ch-32-voice-ai.md',
    'part-5/ch-33-auto-research.md',
    'part-5/ch-34-whats-next.md',
    'projects/project-04.md',

    # Backmatter
    'backmatter/appendix-a-resources.md',
    'backmatter/appendix-b-claude-templates.md',
    'backmatter/appendix-c-design-system.md',
    'backmatter/appendix-d-glossary.md',
    'backmatter/appendix-e-case-studies.md',
    'backmatter/afterword.md',
    'backmatter/colophon.md',
]


def load_bibliography():
    """Load bibliography.yaml for citation resolution."""
    bib_path = Path(__file__).parent.parent / 'resources' / 'bibliography.yaml'
    if bib_path.exists():
        with open(bib_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def process_custom_blocks(html):
    """Convert custom markdown patterns into styled HTML."""

    # ARIA boxes: > **ANALOGY**: text
    patterns = {
        r'<blockquote>\s*<p><strong>ANALOGY</strong>:\s*(.*?)</p>\s*</blockquote>':
            r'<div class="aria-box aria-analogy"><div class="aria-label">Analogy</div><p>\1</p></div>',
        r'<blockquote>\s*<p><strong>REAL-LIFE</strong>:\s*(.*?)</p>\s*</blockquote>':
            r'<div class="aria-box aria-reallife"><div class="aria-label">Real-Life Example</div><p>\1</p></div>',
        r'<blockquote>\s*<p><strong>INTUITION</strong>:\s*(.*?)</p>\s*</blockquote>':
            r'<div class="aria-box aria-intuition"><div class="aria-label">Why This Exists</div><p>\1</p></div>',
        r'<blockquote>\s*<p><strong>EXERCISE</strong>:\s*(.*?)</p>\s*</blockquote>':
            r'<div class="exercise"><div class="exercise-title">Try It Yourself</div><p>\1</p></div>',
        r'<blockquote>\s*<p><strong>CALLOUT</strong>:\s*(.*?)</p>\s*</blockquote>':
            r'<div class="callout"><p>\1</p></div>',
    }

    for pattern, replacement in patterns.items():
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    return html


def markdown_to_html(md_content):
    """Convert markdown to HTML with extensions."""
    md = markdown.Markdown(
        extensions=[
            'tables',
            'toc',
            'fenced_code',
            'footnotes',
            'attr_list',
            'meta',
            'smarty',
        ],
        extension_configs={
            'toc': {'permalink': False},
            'smarty': {'smart_quotes': True, 'smart_dashes': True},
        }
    )
    html = md.convert(md_content)
    html = process_custom_blocks(html)
    return html


def build_book(chapters=None):
    """Build the complete book HTML and PDF."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load CSS
    css_content = CSS_FILE.read_text()

    # Build HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="utf-8">',
        f'<style>{css_content}</style>',
        '</head>',
        '<body>',
    ]

    chapter_list = chapters or CHAPTER_ORDER
    chapters_found = 0

    for chapter_path in chapter_list:
        full_path = BOOK_DIR / chapter_path
        if full_path.exists():
            md_content = full_path.read_text()
            html_content = markdown_to_html(md_content)
            # Use filename stem as unique section ID for internal linking
            section_id = full_path.stem
            html_parts.append(f'\n<!-- {chapter_path} -->\n')
            html_parts.append(f'<section id="{section_id}">')
            html_parts.append(html_content)
            html_parts.append('</section>')
            chapters_found += 1
        else:
            print(f"  [SKIP] {chapter_path} (not yet written)")

    html_parts.extend(['</body>', '</html>'])
    full_html = '\n'.join(html_parts)

    # Write HTML
    html_path = OUTPUT_DIR / 'builders-bible.html'
    html_path.write_text(full_html)
    print(f"  [HTML] {html_path} ({chapters_found} chapters)")

    # Generate PDF
    try:
        from weasyprint import HTML
        pdf_path = OUTPUT_DIR / 'The-Builders-Bible.pdf'
        HTML(string=full_html).write_pdf(str(pdf_path))
        pdf_size = pdf_path.stat().st_size / (1024 * 1024)
        print(f"  [PDF]  {pdf_path} ({pdf_size:.1f} MB)")
    except ImportError:
        print("  [WARN] WeasyPrint not importable. HTML generated, PDF skipped.")
        print("         Run: pip3 install weasyprint")
    except Exception as e:
        print(f"  [ERR]  PDF generation failed: {e}")

    return chapters_found


def build_single_chapter(chapter_path):
    """Build a single chapter for preview."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    css_content = CSS_FILE.read_text()

    full_path = BOOK_DIR / chapter_path
    if not full_path.exists():
        print(f"Chapter not found: {full_path}")
        return

    md_content = full_path.read_text()
    html_content = markdown_to_html(md_content)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>{css_content}</style></head>
<body>{html_content}</body>
</html>"""

    stem = full_path.stem
    html_path = OUTPUT_DIR / f'preview-{stem}.html'
    html_path.write_text(html)
    print(f"  [PREVIEW] {html_path}")


if __name__ == '__main__':
    print(f"\n  The Builder's Bible — Build System")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  {'=' * 40}\n")

    if len(sys.argv) > 1:
        if sys.argv[1] == '--preview':
            chapter = sys.argv[2] if len(sys.argv) > 2 else CHAPTER_ORDER[0]
            build_single_chapter(chapter)
        elif sys.argv[1] == '--list':
            for i, ch in enumerate(CHAPTER_ORDER):
                exists = '✓' if (BOOK_DIR / ch).exists() else ' '
                print(f"  [{exists}] {i+1:2d}. {ch}")
        else:
            print(f"Usage: {sys.argv[0]} [--preview <chapter>] [--list]")
    else:
        count = build_book()
        print(f"\n  Done. {count} chapters included.\n")
