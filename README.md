# taguma

Personal blog and portfolio. Built with [Jekyll](https://jekyllrb.com/).

## Running the project

Install Ruby dependencies once:

```bash
bundle install
```

Start the local development server:

```bash
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000`.

---

## Creating new posts

Use the interactive TUI wizard to create any type of post.

**Install the dependency once:**

```bash
pip install questionary
```

**Run the wizard:**

```bash
python3 new_post.py
```

The wizard will ask for the post type, fill in the required and optional fields, and open the generated file in your `$EDITOR` (defaults to `nano` if not set).

### Post types

| Type | Directory | URL |
|------|-----------|-----|
| `blog` | `_posts/` | `/blog/<slug>/` |
| `tech` | `_tech/` | `/dev/<slug>/` |
| `atelier` | `_atelier/` | `/atelier/<slug>/` |
| `review` | `_reviews/` | `/reviews/<slug>/` |
| `manual` | `_manual_backend/` | `/backend-manual/<slug>/` |

### Atelier sub-types

When selecting `atelier`, the wizard asks for a sub-type:

| Sub-type | Layout | Main image fields |
|----------|--------|-------------------|
| `pintura` | `painting` | `image` — shown in listing and body |
| `fotografia` | `photography` | `cover` — listing thumbnail; `images[]` — gallery |
| `musica` | `music` | `image` — shown in listing only |
| `literatura` | `writing` | `cover` — listing thumbnail; `image` + `image_caption` — body |

### Images

For any field that accepts an image, the wizard will ask for a local file path (with tab-completion). The file is copied automatically to the correct `assets/images/` subdirectory and the Jekyll path is inserted into the frontmatter.

Image asset directories:

```
assets/images/atelier/pinturas/
assets/images/atelier/fotografias/
assets/images/atelier/musicas/
assets/images/reviews/
```

### Generated file

The wizard creates the markdown file with the complete frontmatter and a single placeholder line:

```
<!-- Write your content here -->
```

Edit the file to add the actual content after the wizard closes.
