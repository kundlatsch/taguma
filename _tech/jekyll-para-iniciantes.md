---
title: "Jekyll para Iniciantes"
description: "Um guia pratico para comecar com Jekyll e criar seu proprio site estatico."
date: 2024-01-20
tags: [jekyll, tutorial, web]
---

ESTE É UM PLACEHOLDER GERADO POR IA!

## Por que Jekyll?

1. **Simples** - Markdown + templates = site pronto
2. **Gratuito** - GitHub Pages hospeda de graca
3. **Rapido** - Sites estaticos sao muito rapidos
4. **Flexivel** - Customize tudo que quiser

## Estrutura basica

```
meu-site/
├── _config.yml      # Configuracoes
├── _layouts/        # Templates
├── _includes/       # Componentes reutilizaveis
├── _posts/          # Seus posts
├── assets/          # CSS, JS, imagens
└── index.html       # Pagina inicial
```

## Comecando

```bash
# Instale Ruby primeiro, depois:
gem install bundler jekyll

# Crie um novo site
jekyll new meu-site
cd meu-site

# Rode localmente
bundle exec jekyll serve
```

Acesse `http://localhost:4000` e veja seu site funcionando!

## Proximos passos

- Customize o tema
- Adicione colecoes para diferentes tipos de conteudo
- Configure deploy automatico no GitHub Pages
