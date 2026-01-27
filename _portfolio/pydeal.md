---
title: "pyDEAL"
description: "Dataclass Environment Auto Loader."
tech: [Python]
github: "https://github.com/kundlatsch/py_deal"
live: "https://pypi.org/project/py-deal/"
image: /assets/images/portfolio/deal.png
---

# 🧩 DEAL — Dataclass Environment Auto Loader

O DEAL é uma biblioteca Python leve e tipada para carregamento e validação de variáveis de ambiente a partir de arquivos .env, utilizando dataclasses como esquema de configuração.

O projeto automatiza a leitura de configurações, faz conversão segura de tipos (como bool, int, list, dict e Optional), valida os dados em tempo de inicialização e centraliza o acesso às configurações por meio de um objeto estático global.

Entre seus principais diferenciais estão:

* Integração direta com dataclasses, garantindo tipagem forte e clareza de contrato;

* Parsing automático de estruturas complexas (listas e JSON);

* Mascaramento automático de informações sensíveis ao imprimir configurações;

* Suporte tanto a arquivos .env quanto a variáveis de ambiente do sistema;

* Design simples e extensível, pensado para aplicações backend e scripts Python.

O DEAL foi desenvolvido com foco em simplicidade, segurança e legibilidade, reduzindo boilerplate e erros comuns no gerenciamento de configuração em projetos Python.