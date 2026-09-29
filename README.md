# A Locução

Site institucional e páginas de conversão da A Locução, publicado no GitHub Pages em [alocucao.com.br](https://alocucao.com.br/).

## Estrutura

- `data/regions.json`: base de dados regional para geração de páginas de SEO local.
- `templates/region-template.html`: template HTML base para páginas estáticas de SEO regional.
- `scripts/generate-seo-pages.js`: script gerador de páginas regionais e atualizador do `sitemap.xml`.
- `index.html`: página inicial.
- `locucao-off/`: landing page de locução off.
- `spot-comercial/`: landing page de produção de spot comercial.
- `calculadora/`: estimador público de palavras, duração e blocos de até 40 segundos.
- `sobre/`: apresentação e contato.
- `politica-de-privacidade/` e `termos-de-uso/`: páginas de confiança e conformidade.
- `assets/`: scripts compartilhados e estilos das páginas institucionais.
- `robots.txt`, `sitemap.xml` e `404.html`: suporte técnico de SEO e navegação.
- `.github/workflows/indexnow.yml`: avisa Bing e mecanismos participantes do IndexNow quando URLs públicas são alteradas.

Os arquivos `locucao_off.html` e `spot_comercial.html` são mantidos temporariamente para compatibilidade com links antigos. As URLs preferenciais estão definidas nas tags canônicas e no sitemap.

## Medição

O site usa a tag do Google Ads `AW-18420702149` e dispara a conversão existente em cliques para o WhatsApp. O Consent Mode mantém armazenamento publicitário e analítico negado por padrão até a escolha do visitante.

Antes de alterar IDs, rótulos de conversão ou URLs de campanha, valide a configuração da conta do Google Ads.

## Geração Dinâmica de Páginas de SEO Local

O projeto possui um sistema automatizado para gerar landing pages regionais (`/produtora-de-audio-[slug]/`) e atualizar o `sitemap.xml`.

### Como adicionar novos estados ou cidades:
1. Abra o arquivo `data/regions.json`.
2. Adicione um novo objeto ao array com a seguinte estrutura:
```json
{
  "stateName": "Nome do Estado ou Cidade",
  "stateAbbr": "UF",
  "slug": "nome-do-estado",
  "nicheEmphasis": "ênfase nos nichos de mercado da região",
  "pageTitle": "Título SEO para a tag <title>",
  "metaDescription": "Descrição única para meta description (evitando doorway pages)",
  "eyebrow": "Sua Produtora de Áudio em [Nome]",
  "h1Title": "Produtora de Áudio e Estúdio de Locução em [Nome]",
  "heroParagraph": "Descrição persuasiva sobre atendimento e locução para a região.",
  "regionalFocus": "Pontos fortes e setores atendidos no estado.",
  "cities": ["Cidade 1", "Cidade 2", "Cidade 3"]
}
```
3. Execute o comando de build no terminal:
```bash
npm run build
```
4. As novas páginas serão geradas na raiz do projeto (ex: `produtora-de-audio-nome-do-estado/index.html`) e adicionadas ao `sitemap.xml`.

## Indexação no Bing

O arquivo de chave IndexNow fica na raiz pública. A automação envia somente URLs afetadas por cada publicação; não remova a chave nem altere o domínio no workflow sem gerar e publicar uma nova chave.

