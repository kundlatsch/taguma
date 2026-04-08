#!/usr/bin/env python3
"""
new_post.py — Interactive TUI wizard for creating new Jekyll blog posts.

Usage: python new_post.py
Requires: pip install questionary
"""

import sys

try:
    import questionary
    from questionary import Style
except ImportError:
    print("Missing dependency. Run: pip install questionary")
    sys.exit(1)

import datetime
import os
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rprint
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.resolve()

DIRS = {
    "blog":    PROJECT_ROOT / "_posts",
    "tech":    PROJECT_ROOT / "_tech",
    "atelier": PROJECT_ROOT / "_atelier",
    "review":  PROJECT_ROOT / "_reviews",
    "manual":  PROJECT_ROOT / "_manual_backend",
}

IMAGE_DIRS = {
    "pinturas":    PROJECT_ROOT / "assets/images/atelier/pinturas",
    "fotografias": PROJECT_ROOT / "assets/images/atelier/fotografias",
    "musicas":     PROJECT_ROOT / "assets/images/atelier/musicas",
    "reviews":     PROJECT_ROOT / "assets/images/reviews",
}

ATELIER_LAYOUT = {
    "pintura":    "painting",
    "fotografia": "photography",
    "musica":     "music",
    "literatura": "writing",
}

REVIEW_TYPES   = ["filme", "livro", "manga", "anime", "game"]
ATELIER_TYPES  = ["pintura", "fotografia", "musica", "literatura"]
POST_TYPES     = ["blog", "tech", "atelier", "review", "manual"]

CUSTOM_STYLE = Style([
    ("qmark",     "fg:#00afd7 bold"),
    ("question",  "bold"),
    ("answer",    "fg:#00d787 bold"),
    ("pointer",   "fg:#00afd7 bold"),
    ("highlighted", "fg:#00afd7 bold"),
    ("selected",  "fg:#00d787"),
    ("separator", "fg:#6c6c6c"),
    ("instruction", "fg:#6c6c6c"),
])

console = Console() if HAS_RICH else None

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    """Convert a title to a URL-safe slug, handling Portuguese accented chars."""
    normalized = unicodedata.normalize("NFD", title.lower())
    ascii_str = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_str)
    return slug.strip("-")


def get_today() -> str:
    return datetime.date.today().isoformat()


def require_text(prompt: str) -> str:
    """Prompt for text, re-asking until a non-empty value is given."""
    while True:
        value = questionary.text(prompt, style=CUSTOM_STYLE).ask()
        if value is None:
            raise KeyboardInterrupt
        if value.strip():
            return value.strip()
        _warn("This field is required.")


def _warn(msg: str) -> None:
    if HAS_RICH:
        rprint(f"[yellow]  {msg}[/yellow]")
    else:
        print(f"  WARNING: {msg}")


def _info(msg: str) -> None:
    if HAS_RICH:
        rprint(f"[cyan]  {msg}[/cyan]")
    else:
        print(f"  {msg}")


def _ask(value) -> str:
    """Unwrap questionary result, raising KeyboardInterrupt on None (Ctrl+C)."""
    if value is None:
        raise KeyboardInterrupt
    return value


# ---------------------------------------------------------------------------
# Tag collection
# ---------------------------------------------------------------------------

def _scan_existing_tags() -> list[str]:
    """Parse all markdown files to collect previously used tags."""
    tags: set[str] = set()
    for md_file in PROJECT_ROOT.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = re.search(r"^tags:\s*\[([^\]]+)\]", text, re.MULTILINE)
        if m:
            for tag in m.group(1).split(","):
                t = tag.strip().strip('"').strip("'")
                if t:
                    tags.add(t)
    return sorted(tags)


def collect_tags() -> list[str]:
    """Interactive tag selection: checkbox from known tags + free-text additions."""
    existing = _scan_existing_tags()
    selected: list[str] = []

    if existing:
        chosen = questionary.checkbox(
            "Select tags (space to toggle, enter to confirm):",
            choices=existing,
            style=CUSTOM_STYLE,
        ).ask()
        if chosen is None:
            raise KeyboardInterrupt
        selected = list(chosen)

    while True:
        new_tag = questionary.text(
            "Add a new tag (leave empty to stop):",
            style=CUSTOM_STYLE,
        ).ask()
        if new_tag is None:
            raise KeyboardInterrupt
        new_tag = new_tag.strip()
        if not new_tag:
            break
        if new_tag not in selected:
            selected.append(new_tag)

    return selected


# ---------------------------------------------------------------------------
# Image collection
# ---------------------------------------------------------------------------

def collect_image(dest_dir: Path, field_name: str) -> str | None:
    """
    Ask whether to add an image. If yes, prompt for a local path,
    copy the file to dest_dir, and return the Jekyll-relative path.
    """
    wants = questionary.confirm(
        f"Add {field_name}?",
        default=False,
        style=CUSTOM_STYLE,
    ).ask()
    if wants is None:
        raise KeyboardInterrupt
    if not wants:
        return None

    while True:
        src = questionary.path(
            f"Path to image file for {field_name}:",
            style=CUSTOM_STYLE,
        ).ask()
        if src is None:
            raise KeyboardInterrupt
        src_path = Path(src).expanduser().resolve()
        if src_path.is_file():
            break
        _warn(f"File not found: {src_path}")

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src_path.name
    if dest_path != src_path:
        shutil.copy2(src_path, dest_path)
        _info(f"Copied → {dest_path.relative_to(PROJECT_ROOT)}")

    relative = dest_path.relative_to(PROJECT_ROOT)
    return f"/{relative}"


def collect_images_array(dest_dir: Path) -> list[str]:
    """Collect multiple images for photography galleries."""
    images: list[str] = []
    _info("Add gallery images one by one.")
    while True:
        path = collect_image(dest_dir, f"image #{len(images) + 1}")
        if path is None:
            if not images:
                break
            add_more = questionary.confirm(
                "No image added. Add an image?",
                default=True,
                style=CUSTOM_STYLE,
            ).ask()
            if add_more is None:
                raise KeyboardInterrupt
            if not add_more:
                break
            continue
        images.append(path)
        add_more = questionary.confirm(
            "Add another image?",
            default=True,
            style=CUSTOM_STYLE,
        ).ask()
        if add_more is None:
            raise KeyboardInterrupt
        if not add_more:
            break
    return images


# ---------------------------------------------------------------------------
# Slug confirmation helper
# ---------------------------------------------------------------------------

def _confirm_slug(title: str) -> str:
    auto_slug = slugify(title)
    slug = questionary.text(
        "Slug:",
        default=auto_slug,
        style=CUSTOM_STYLE,
    ).ask()
    if slug is None:
        raise KeyboardInterrupt
    return slug.strip() or auto_slug


# ---------------------------------------------------------------------------
# Wizards
# ---------------------------------------------------------------------------

def wizard_blog() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)
    date  = _ask(questionary.text("Date (YYYY-MM-DD):", default=get_today(), style=CUSTOM_STYLE).ask())
    description = _ask(questionary.text("Description (optional):", style=CUSTOM_STYLE).ask()).strip()
    tags = collect_tags()

    fields: dict = {"title": title}
    if description:
        fields["description"] = description
    fields["date"] = date
    if tags:
        fields["tags"] = tags
    fields["_dir"]      = DIRS["blog"]
    fields["_filename"] = f"{date}-{slug}.md"
    return fields


def wizard_tech() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)
    date  = _ask(questionary.text("Date (YYYY-MM-DD):", default=get_today(), style=CUSTOM_STYLE).ask())
    description = _ask(questionary.text("Description (optional):", style=CUSTOM_STYLE).ask()).strip()
    tags = collect_tags()

    fields: dict = {"title": title}
    if description:
        fields["description"] = description
    fields["date"] = date
    if tags:
        fields["tags"] = tags
    fields["_dir"]      = DIRS["tech"]
    fields["_filename"] = f"{slug}.md"
    return fields


def wizard_pintura() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)
    date  = _ask(questionary.text("Date (YYYY-MM-DD):", default=get_today(), style=CUSTOM_STYLE).ask())
    medium = _ask(questionary.text("Medium (optional, e.g. 'Óleo sobre tela, 30x40cm'):", style=CUSTOM_STYLE).ask()).strip()
    image = collect_image(IMAGE_DIRS["pinturas"], "image")

    fields: dict = {"layout": "painting", "type": "pintura", "title": title}
    if medium:
        fields["medium"] = medium
    fields["date"] = date
    if image:
        fields["image"] = image
    fields["_dir"]      = DIRS["atelier"]
    fields["_filename"] = f"{slug}.md"
    return fields


def wizard_fotografia() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)
    date  = _ask(questionary.text("Date (YYYY-MM-DD):", default=get_today(), style=CUSTOM_STYLE).ask())
    medium = _ask(questionary.text("Medium (optional, e.g. 'Fotografia digital'):", style=CUSTOM_STYLE).ask()).strip()
    cover  = collect_image(IMAGE_DIRS["fotografias"], "cover (listing thumbnail)")
    images = collect_images_array(IMAGE_DIRS["fotografias"])

    fields: dict = {"layout": "photography", "type": "fotografia", "title": title}
    if medium:
        fields["medium"] = medium
    fields["date"] = date
    if cover:
        fields["cover"] = cover
    if images:
        fields["images"] = images
    fields["_dir"]      = DIRS["atelier"]
    fields["_filename"] = f"{slug}.md"
    return fields


def wizard_musica() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)
    date  = _ask(questionary.text("Date (YYYY-MM-DD):", default=get_today(), style=CUSTOM_STYLE).ask())
    medium = _ask(questionary.text("Medium (optional, e.g. 'Faixa digital, produção eletrônica'):", style=CUSTOM_STYLE).ask()).strip()
    image = collect_image(IMAGE_DIRS["musicas"], "image (listing)")

    fields: dict = {"layout": "music", "type": "musica", "title": title}
    if medium:
        fields["medium"] = medium
    fields["date"] = date
    if image:
        fields["image"] = image
    fields["_dir"]      = DIRS["atelier"]
    fields["_filename"] = f"{slug}.md"
    return fields


def wizard_literatura() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)
    date  = _ask(questionary.text("Date (YYYY-MM-DD):", default=get_today(), style=CUSTOM_STYLE).ask())
    medium = _ask(questionary.text("Medium (optional, e.g. 'Poema', 'Conto'):", style=CUSTOM_STYLE).ask()).strip()
    cover  = collect_image(IMAGE_DIRS["pinturas"], "cover (listing thumbnail)")
    image  = collect_image(IMAGE_DIRS["pinturas"], "image (body decorative)")
    image_caption = ""
    if image:
        image_caption = _ask(questionary.text("Image caption (optional):", style=CUSTOM_STYLE).ask()).strip()

    fields: dict = {"layout": "writing", "type": "literatura", "title": title}
    if medium:
        fields["medium"] = medium
    fields["date"] = date
    if cover:
        fields["cover"] = cover
    if image:
        fields["image"] = image
    if image_caption:
        fields["image_caption"] = image_caption
    fields["_dir"]      = DIRS["atelier"]
    fields["_filename"] = f"{slug}.md"
    return fields


def wizard_atelier() -> dict:
    sub_type = _ask(questionary.select(
        "Atelier sub-type:",
        choices=ATELIER_TYPES,
        style=CUSTOM_STYLE,
    ).ask())
    dispatch = {
        "pintura":    wizard_pintura,
        "fotografia": wizard_fotografia,
        "musica":     wizard_musica,
        "literatura": wizard_literatura,
    }
    return dispatch[sub_type]()


def wizard_review() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)

    review_type = _ask(questionary.select(
        "Type:",
        choices=REVIEW_TYPES,
        style=CUSTOM_STYLE,
    ).ask())

    rating_choice = _ask(questionary.select(
        "Rating (1-5 stars):",
        choices=["1", "2", "3", "4", "5", "(skip)"],
        style=CUSTOM_STYLE,
    ).ask())
    rating = None if rating_choice == "(skip)" else int(rating_choice)

    creator = _ask(questionary.text("Creator / Director / Author (optional):", style=CUSTOM_STYLE).ask()).strip()
    year_raw = _ask(questionary.text("Year (optional):", style=CUSTOM_STYLE).ask()).strip()
    year = int(year_raw) if year_raw.isdigit() else None

    cover = collect_image(IMAGE_DIRS["reviews"], "cover")

    fields: dict = {"title": title, "type": review_type}
    if rating is not None:
        fields["rating"] = rating
    if creator:
        fields["creator"] = creator
    if year is not None:
        fields["year"] = year
    if cover:
        fields["cover"] = cover
    fields["_dir"]      = DIRS["review"]
    fields["_filename"] = f"{slug}.md"
    return fields


def wizard_manual() -> dict:
    title = require_text("Title:")
    slug  = _confirm_slug(title)

    chapter = None
    while chapter is None:
        raw = _ask(questionary.text("Chapter number (integer):", style=CUSTOM_STYLE).ask()).strip()
        try:
            chapter = int(raw)
        except ValueError:
            _warn("Chapter must be an integer.")

    description = _ask(questionary.text("Description (optional):", style=CUSTOM_STYLE).ask()).strip()
    part        = _ask(questionary.text("Part / section name (optional):", style=CUSTOM_STYLE).ask()).strip()
    permalink   = _ask(questionary.text("Custom permalink (optional):", style=CUSTOM_STYLE).ask()).strip()

    fields: dict = {"layout": "manual", "title": title}
    if description:
        fields["description"] = description
    fields["chapter"] = chapter
    if part:
        fields["part"] = part
    if permalink:
        fields["permalink"] = permalink
    fields["_dir"]      = DIRS["manual"]
    fields["_filename"] = f"{chapter:02d}-{slug}.md"
    return fields


# ---------------------------------------------------------------------------
# Frontmatter rendering
# ---------------------------------------------------------------------------

_INTERNAL_KEYS = {"_dir", "_filename"}

def _needs_quoting(value: str) -> bool:
    """Return True if the YAML string value needs to be quoted."""
    return any(c in value for c in (':', '"', "'", '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`'))


def render_frontmatter(fields: dict) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if key in _INTERNAL_KEYS or value is None or value == "" or value == []:
            continue
        if isinstance(value, list):
            # Block sequence for images array; inline for tags
            if key == "images":
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                # Inline array style: tags: [a, b, c]
                inline = ", ".join(str(v) for v in value)
                lines.append(f"{key}: [{inline}]")
        elif isinstance(value, str) and _needs_quoting(value):
            escaped = value.replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Summary display
# ---------------------------------------------------------------------------

def _show_summary(fields: dict, filepath: Path) -> None:
    if not HAS_RICH:
        print("\n--- Summary ---")
        for k, v in fields.items():
            if k not in _INTERNAL_KEYS:
                print(f"  {k}: {v}")
        print(f"  file: {filepath}")
        print("---------------\n")
        return

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value")

    for key, value in fields.items():
        if key in _INTERNAL_KEYS:
            continue
        if isinstance(value, list):
            display = ", ".join(str(v) for v in value) if value else "(none)"
        else:
            display = str(value) if value is not None else "(none)"
        table.add_row(key, display)

    table.add_row("file", str(filepath.relative_to(PROJECT_ROOT)), )
    console.print(Panel(table, title="[bold]Post Summary[/bold]", border_style="cyan"))


# ---------------------------------------------------------------------------
# File writing and editor
# ---------------------------------------------------------------------------

def write_post(filepath: Path, frontmatter: str) -> None:
    content = frontmatter + "\n\n<!-- Write your content here -->\n"
    filepath.write_text(content, encoding="utf-8")


def open_editor(filepath: Path) -> None:
    editor = os.environ.get("EDITOR", "nano")
    try:
        subprocess.run([editor, str(filepath)])
    except FileNotFoundError:
        _warn(f"Editor '{editor}' not found. Open the file manually: {filepath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if HAS_RICH:
        console.print(Panel(
            "[bold cyan]Jekyll Post Creator[/bold cyan]\n[dim]Press Ctrl+C at any time to abort[/dim]",
            border_style="cyan",
        ))
    else:
        print("\n=== Jekyll Post Creator ===\n")

    post_type = _ask(questionary.select(
        "Post type:",
        choices=POST_TYPES,
        style=CUSTOM_STYLE,
    ).ask())

    wizards = {
        "blog":    wizard_blog,
        "tech":    wizard_tech,
        "atelier": wizard_atelier,
        "review":  wizard_review,
        "manual":  wizard_manual,
    }
    fields = wizards[post_type]()

    filepath: Path = fields["_dir"] / fields["_filename"]

    _show_summary(fields, filepath)

    if filepath.exists():
        _warn(f"{fields['_filename']} already exists.")
        overwrite = questionary.confirm("Overwrite?", default=False, style=CUSTOM_STYLE).ask()
        if not overwrite:
            if HAS_RICH:
                rprint("[yellow]Aborted.[/yellow]")
            else:
                print("Aborted.")
            sys.exit(0)

    confirmed = questionary.confirm("Create this post?", default=True, style=CUSTOM_STYLE).ask()
    if not confirmed:
        if HAS_RICH:
            rprint("[yellow]Aborted.[/yellow]")
        else:
            print("Aborted.")
        sys.exit(0)

    fields["_dir"].mkdir(parents=True, exist_ok=True)
    frontmatter = render_frontmatter(fields)
    write_post(filepath, frontmatter)

    if HAS_RICH:
        rprint(f"[green]Created:[/green] {filepath.relative_to(PROJECT_ROOT)}")
    else:
        print(f"Created: {filepath.relative_to(PROJECT_ROOT)}")

    open_editor(filepath)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if HAS_RICH:
            rprint("\n[yellow]Interrupted.[/yellow]")
        else:
            print("\nInterrupted.")
        sys.exit(0)
