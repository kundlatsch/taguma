---
title: "Criando e publicando o py-deal no PyPI"
description: "Um guia prático para publicar seu primeiro pacote Python."
date: 2026-02-13
tags: [python, tutorial]
---

Fazia algum tempo que eu queria ter meu próprio pacote Python distribuído pelo PyPI, o problema é que eu nunca conseguia pensar em algo que para mim fizesse sentido ter meu próprio pacote.

Resolvi então que reinventaria a roda mesmo, para conhecer o processo. Tive a ideia a partir de um problema simples mas que sempre me ocorria: ter que configurar um `config.py` com as variáveis de ambiente de projeto.

Eu queria uma forma previsível de carregar variáveis de ambiente usando `.env`, validar tipos automaticamente e manter tudo centralizado em um único objeto de configuração. Nada de variáveis soltas pelo código. Nada de `os.getenv` espalhado. Nada de conversões manuais repetidas. Certamente existem bibliotecas que já fazem isso, pacotes muito mais maduros, mas eu queria criar o meu próprio, só pelo amor ao jogo.

A ideia então foi simples: usar `dataclass` como contrato de configuração. Se os campos estão tipados, eles já dizem exatamente o que a aplicação espera. A partir disso, o que o py-deal faz é:

- carregar o `.env` com `python-dotenv`
- ler os campos definidos na dataclass
- converter automaticamente para os tipos declarados
- falhar cedo se algo estiver faltando ou inválido
- mascarar campos sensíveis quando o objeto é impresso

O uso ficou assim:

```python
from dataclasses import dataclass
from deal.config import Config

@dataclass
class AppConfig(Config):
    APP_NAME: str
    DEBUG: bool
    PORT: int
    AWS_KEY: str
```

Instanciar a configuração já valida tudo:

```python
config = AppConfig()
```

Se `PORT` não for inteiro, quebra.
Se `APP_NAME` não existir, quebra.

É intencional. Configuração errada não deve ser tolerada.

Usei `hatchling` como backend moderno de build. Meu `pyproject.toml` ficou essencialmente assim:

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "py-deal"
version = "0.1.0"
description = "Simple .env-to-dataclass validator and static config holder"
requires-python = ">=3.9"
dependencies = [
  "python-dotenv>=1.0.0",
]
```

Uma coisa que aprendi no processo: metadados importam. Em uma das tentativas de upload recebi um erro de metadata inválida por causa de um campo `license-file` mal configurado. O padrão moderno é definir a licença diretamente no campo `license`.

Para gerar os artefatos:

```
pip install build twine
python -m build
```

Para publicar basta:

```
twine upload dist/*
```

E pronto. O pacote passou a existir de verdade.

Depois disso fiz o teste mais importante: criar um ambiente virtual limpo e instalar como qualquer outra pessoa faria:

```
python -m venv venv
source venv/bin/activate
pip install py-deal
```

Criar um `.env`, instanciar a configuração e ver funcionando fora do meu ambiente original foi a confirmação de que estava funcionando.

Uma dúvida comum nesse processo é sobre GitHub Releases. Não é necessário subir o .whl lá, o PyPI já é o canal oficial de distribuição. O GitHub pode ficar com changelog e histórico de versões, mas os binários pertencem ao PyPI.

O que eu tiro disso tudo não é que o `py-deal` seja um pacote enorme ou revolucionário: ele é simples e específico. Mas o processo de empacotar corretamente, versionar, escrever testes, ajustar metadados e publicar ensina coisas que normalmente abstraímos e deixamos na mão de outros desenvolvedores.

E no fim, rodar `pip install py-deal` é uma sensação muito legal.
