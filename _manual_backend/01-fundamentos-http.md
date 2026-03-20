---
layout: manual
title: "Fundamentos do HTTP"
description: "Entendendo o protocolo HTTP e os princípios REST."
chapter: 1
part: "Fundamentos"
---

## O que é HTTP?

HTTP (*HyperText Transfer Protocol*) é o protocolo de comunicação que fundamenta a web. Toda requisição que seu navegador faz a um servidor — carregar uma página, enviar um formulário, consumir uma API — usa HTTP.

### Modelo cliente-servidor

O HTTP funciona no modelo **requisição/resposta**:

1. O **cliente** (browser, app, `curl`) envia uma requisição
2. O **servidor** processa e devolve uma resposta

### Métodos HTTP

| Método | Uso |
|--------|-----|
| `GET` | Buscar um recurso |
| `POST` | Criar um recurso |
| `PUT` | Substituir um recurso |
| `PATCH` | Atualizar parcialmente |
| `DELETE` | Remover um recurso |

### Códigos de status

- **2xx** — Sucesso (`200 OK`, `201 Created`)
- **3xx** — Redirecionamento (`301 Moved Permanently`)
- **4xx** — Erro do cliente (`400 Bad Request`, `404 Not Found`, `401 Unauthorized`)
- **5xx** — Erro do servidor (`500 Internal Server Error`)

## REST

REST (*Representational State Transfer*) é um estilo arquitetural para APIs HTTP com algumas restrições centrais:

- **Interface uniforme** — URLs identificam recursos, métodos HTTP indicam a ação
- **Stateless** — cada requisição contém toda informação necessária; o servidor não guarda estado de sessão
- **Recursos** — tudo é um recurso endereçável por URL (ex: `/users/42`)

### Exemplo: API de usuários

```
GET    /users        → lista usuários
POST   /users        → cria um usuário
GET    /users/42     → busca o usuário 42
PATCH  /users/42     → atualiza o usuário 42
DELETE /users/42     → remove o usuário 42
```
