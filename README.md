# public-docs

Site público das minhas notas de estudo — <https://alsvinicius.github.io/public-docs>.

Hoje: a trilha de **agentic commerce** (12 notas), com um índice que organiza por
camada e dá duas trilhas de leitura (histórica e de decisão).

## O que é este repo

O conteúdo em `content/` é a **cópia pública** de notas que têm uma fonte de
verdade numa vault Obsidian privada. As duas coisas divergem: o que é privado
(marcadores de sessão, aliases de cross-link entre notas privadas, links para
notas que não saem) é removido na conversão.

Portanto, **não edite `content/` direto** esperando que a mudança chegue na vault.
O caminho normal é editar a nota na vault e reexportar.

## Rodando localmente

```bash
npm ci
npx quartz build --serve   # http://localhost:8080
```

O servidor de desenvolvimento resolve URLs sem extensão; o build estático
emite `pagina.html`. É por isso que os links internos aparecem como
`/estudos/agentic-commerce/` no HTML mas o arquivo é `index.html`.

## Convenções

- **Slug, não nome de arquivo.** O Quartz resolve wikilink por slug, então
  `[[seguranca]]` e não `[[Segurança]]`. O mesmo vale para `[[pasta/index]]`:
  apontar para `[[pasta]]` gera o href certo mas marca o link como quebrado.
- **`index.md` dentro de pasta** precisa do plugin `folder-page` ligado, senão
  a página é lida, aparece no índice de busca e nunca tem HTML emitido.
- **`$` de moeda precisa de escape** (`\$188`). Sem escape o katex abre math
  mode e renderiza a frase como fórmula.

## Licença

O conteúdo é meu. O gerador é o [Quartz](https://quartz.jzhao.xyz/) (MIT),
mantido por `jackyzha0` — o `LICENSE.txt` e o código em `quartz/` são dele.