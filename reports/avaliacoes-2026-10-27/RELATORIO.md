# Entrega — avaliações verificadas — 27/10/2026

## Publicação e alcance

Etapa visual concluída para os **27 locutores**, inclusive Lucan Rook: cinco estrelas SVG cinza e **0 avaliações**, tanto nos perfis como nos cards reutilizáveis. Seção `#avalie` e mensagem clara de preparação, sem formulário que finja receber dados. Contatos, demos, últimos trabalhos, idiomas, filtros, ordem aleatória e selos TOP foram preservados.

URL de exemplo: https://alocucao.com.br/locutores/aline-mota/#avalie

Painel preparado: https://alocucao.com.br/administracao/avaliacoes/

**O sistema de recebimento ainda NÃO está ativo.** O painel não permite login ou operações até configurar o serviço. O código Supabase/Turnstile está preparado no repositório, sem contas provisionadas, banco remoto, administrador cadastrado ou função remota publicada. Não foram contratados serviços pagos e não há mensalidade criada por esta entrega. Custos futuros dependem da infraestrutura e do uso escolhidos pelo proprietário.

## Validação realizada

- Build das 452 entradas de páginas, 27 perfis e 54 demos; validação do site sem erros.
- Testes existentes de consentimento, atribuição, WhatsApp, filtros de gênero/idioma/estilo, reprodução, ordem aleatória e calculadora: passaram.
- Testes novos de todos os templates, estado zero, ausência de envio quando desativado, limpeza do token da URL, limites de campos e pré-validação de imagens: passaram.
- Migrações executadas em PostgreSQL WASM/PGlite: permissões fechadas para anon/authenticated, convites inválidos/expirados/reutilizados e de outro locutor, reemissão, unicidade por pedido, moderação com auditoria, média apenas de aprovadas, rejeição, ocultação, exclusão, retenção e limites: passaram.
- TypeScript do código Edge: passou em Deno, com a dependência fixada instalada localmente.
- WASM de imagem: decodificação de arquivo WebP real, redimensionamento e recodificação: passaram.
- Chromium/Playwright: 27 perfis nas larguras 390 e 1440, contadores/estrelas, âncoras, demos presentes, ausência de formulário desativado, sem overflow horizontal ou erro JavaScript: passaram.
- Ainda pendentes os testes em Supabase hospedado com autenticação, Turnstile e armazenamento reais, disputa concorrente e uploads completos nos três formatos. A integração não será ativada com base somente nos testes locais.

## Próximas configurações do proprietário

Selecionar/criar projeto Supabase, widget Turnstile e usuário administrativo. Aplicar migrações e catálogo, configurar segredos no serviço, publicar Edge Function, configurar retenção e executar homologação. Somente após esse fluxo preencher a configuração pública e ativar o recebimento.

Passo a passo, segurança, operação, retenção e testes: [docs/avaliacoes-implantacao.md](../../docs/avaliacoes-implantacao.md).

## Arquivos alterados/adicionados

- `administracao/avaliacoes/index.html`
- `assets/reviews-config.js`
- `assets/reviews.css`
- `assets/reviews.js`
- `docs/avaliacoes-implantacao.md`
- `scripts/prepare-review-images.mjs`
- `scripts/prepare-reviews.py`
- `scripts/test-reviews-db.cjs`
- `scripts/test-reviews.mjs`
- `supabase/config.toml`
- `supabase/functions/reviews/index.ts`
- `supabase/functions/reviews/validation.mjs`
- `supabase/migrations/202610270001_reviews.sql`
- `supabase/migrations/202610270002_retention.sql`
- `supabase/seed-review-voices.sql`
- `.gitignore`
- `data/legal-pages.json`
- `gravacao-off-e-producao/index.html`
- `index.html`
- `locucao-ia/index.html`
- `locucao-off/index.html`
- `locucao_off.html`
- `locucao_off/index.html`
- `locucaooff/index.html`
- `locutores/aida/index.html`
- `locutores/aline-mota/index.html`
- `locutores/amanda-kelly/index.html`
- `locutores/ana-alice/index.html`
- `locutores/audrey/index.html`
- `locutores/cassio-cruz/index.html`
- `locutores/christine/index.html`
- `locutores/david/index.html`
- `locutores/diego/index.html`
- `locutores/eduardo-s/index.html`
- `locutores/enzo/index.html`
- `locutores/fernanda/index.html`
- `locutores/kaique/index.html`
- `locutores/koraly/index.html`
- `locutores/larissa/index.html`
- `locutores/lax/index.html`
- `locutores/leao-antonio/index.html`
- `locutores/leonardo/index.html`
- `locutores/lucan-rook/index.html`
- `locutores/marcio/index.html`
- `locutores/mario/index.html`
- `locutores/noel-natal/index.html`
- `locutores/paulo-becker/index.html`
- `locutores/roberta/index.html`
- `locutores/thiago/index.html`
- `locutores/will/index.html`
- `locutores/zozo/index.html`
- `off-comercial/index.html`
- `package.json`
- `politica-de-privacidade/index.html`
- `producao-para-igrejas/index.html`
- `producao-para-supermercados/index.html`
- `reports/reformulacao-2026-10-26/manifesto.json`
- `reports/reformulacao-2026-10-26/validacao.json`
- `scripts/build-nova.py`
- `spot-black-friday/index.html`
- `spot-comercial/index.html`
- `spot_comercial.html`
- `spot_comercial/index.html`
- `spot_supermercado/index.html`
- `spotcomercial/index.html`
- `talentos/index.html`
- `vozes-ia/index.html`
- `vozes/index.html`
- `reports/avaliacoes-2026-10-27/RELATORIO.md`
