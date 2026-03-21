# taguma

```
bundle exec jekyll serve
```

---

## Criando posts

### Ateliê (`_atelier/`)

Cada arquivo em `_atelier/` vira uma página em `/atelier/<nome-do-arquivo>/`. O layout é definido pelo campo `layout:` no front matter. Se omitido, usa `artwork` por padrão (definido no `_config.yml`).

#### Campos comuns a todos os tipos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `title` | sim | Título do trabalho |
| `type` | sim | Define a categoria: `pintura`, `musica`, `fotografia`, `literatura` |
| `date` | não | Data no formato `YYYY-MM-DD` |
| `medium` | não | Técnica ou formato (ex: "Óleo sobre tela, 30x40cm") |
| `image` | não | Caminho da imagem — aparece **na listagem e no corpo do post** |
| `cover` | não | Caminho da imagem — aparece **só na listagem**, nunca no corpo |

> Se tanto `image` quanto `cover` estiverem definidos, a listagem usa `cover` e o corpo do post usa `image`.

---

#### Pintura — `layout: painting`

Destaca a imagem da pintura centralizada com efeito de galeria. Clique abre lightbox.

```yaml
---
layout: painting
title: "Reprodução: Anjo Caído de Cabanel"
type: pintura
medium: "Óleo sobre tela, 30x40cm"
date: 2025-10-10
image: /assets/images/atelier/pinturas/cabanel.jpg
---

Texto descritivo da obra.
```

---

#### Fotografia — `layout: photography`

Exibe as fotos em tira horizontal com scroll. Cada foto abre em lightbox com navegação ←/→ e contador.

```yaml
---
layout: photography
title: "Série: Luz de Outubro"
type: fotografia
medium: "Fotografia digital"
date: 2025-10-30
cover: /assets/images/atelier/fotografias/capa.jpg
images:
  - /assets/images/atelier/fotografias/foto1.jpg
  - /assets/images/atelier/fotografias/foto2.jpg
  - /assets/images/atelier/fotografias/foto3.jpg
---

Texto descritivo da série.
```

> `cover` é usado como thumbnail na listagem. `images` é a lista de fotos da tira — não aparece na listagem.

---

#### Música — `layout: music`

Layout sem imagem de capa no corpo. O conteúdo do post suporta embeds (YouTube, SoundCloud) que ficam responsivos automaticamente — basta colar o `<iframe>` no corpo do markdown.

```yaml
---
layout: music
title: "Nome da faixa"
type: musica
medium: "Faixa digital, produção eletrônica"
date: 2025-10-30
image: /assets/images/atelier/musicas/capa.png
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/ID" ...></iframe>

Texto sobre a música.
```

> `image` aparece só na listagem do ateliê. O `<iframe>` no corpo é renderizado responsivo (16:9).

---

#### Literatura — `layout: writing`

Tipografia serifada, coluna estreita (680px), espaçamento generoso. Ideal para poemas e textos curtos. Suporta imagem decorativa opcional no corpo.

```yaml
---
layout: writing
title: "Nome do poema"
type: literatura
medium: "Poema"
date: 2026-03-21
cover: /assets/images/atelier/pinturas/referencia.jpg   # só na listagem
---

Verso um
verso dois
verso três.

Segunda estrofe.
```

Para incluir uma imagem decorativa **no corpo do post** (com legenda opcional):

```yaml
image: /assets/images/atelier/pinturas/referencia.jpg
image_caption: "Referência: Anjo Caído, Alexandre Cabanel (1847)"
```

---

### Reviews (`_reviews/`)

Cada arquivo em `_reviews/` vira uma página em `/reviews/<nome-do-arquivo>/`. Usa `layout: review` por padrão.

#### Campos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `title` | sim | Título da obra |
| `type` | sim | Categoria: `filme`, `livro`, `manga`, `anime`, `game` |
| `rating` | não | Nota de 1 a 5 (exibida em estrelas) |
| `creator` | não | Diretor, autor, estúdio, etc. |
| `year` | não | Ano de lançamento |
| `cover` | não | Imagem de capa (aparece no cabeçalho do post, ao lado do título) |

```yaml
---
title: "O Agente Secreto"
type: filme
rating: 5
creator: "Kleber Mendonça Filho"
year: 2025
cover: /assets/images/reviews/o-agente-secreto.jpg
---

Texto da review.
```

---

### Tech (`_tech/`)

Cada arquivo em `_tech/` vira uma página em `/dev/<nome-do-arquivo>/`. Usa `layout: post` por padrão.

#### Campos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `title` | sim | Título do post |
| `description` | não | Subtítulo ou resumo (aparece na listagem) |
| `date` | não | Data no formato `YYYY-MM-DD` |
| `tags` | não | Lista de tags (ex: `[python, tutorial]`) |

```yaml
---
title: "Criando e publicando um pacote no PyPI"
description: "Um guia prático para publicar seu primeiro pacote Python."
date: 2026-02-13
tags: [python, tutorial]
---

Conteúdo do post em markdown.
```
