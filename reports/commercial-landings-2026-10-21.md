# Reestruturação comercial das cinco landing pages

## Alterações por página

- `spot-comercial/index.html`: hero orientado ao anúncio pronto; produção desde R$ 19,00 com identificação IA, alternativa humana R$ 29,90; remoção do comparativo e da Central; preços por serviço e catálogo por abas.
- `locucao-off/index.html`: hero dedicado à gravação somente da voz; Off desde R$ 8,50 IA, alternativa humana R$ 11,90; preços, abas e WhatsApp.
- `producao-para-igrejas/index.html`: mensagem para eventos cristãos, produção em destaque, preços IA/humano e abas; portfólio real preservado.
- `gravacao-off-e-producao/index.html`: hero com os dois serviços, condições de ambas as modalidades e abas; links da Central preservados; CTA fixo móvel prioriza WhatsApp.
- `producao-para-supermercados/index.html`: foco em ofertas e produção completa, preço inicial identificado, substituição do bloco antigo de preços e catálogo por abas; aplicações comerciais e portfólio preservados.

Em todas: títulos SEO, descrições e metadados sociais revistos; URLs e canonicals mantidos; CTA secundário leva ao catálogo; preços de entrada identificam IA e duração; mensagens de contato específicas no hero; condições e pacotes existentes preservados.

## Componentes e arquivos de suporte

- `assets/commercial-refresh.css`: estilo exclusivo das cinco páginas, abas horizontais também no desktop, catálogo único e espaço para CTA fixo móvel.
- `assets/commercial-refresh.js`: preservação de UTM/MSCLKID/GCLID em links internos, painel e WhatsApp, incluindo cards atualizados; não dispara conversões; contato sem voz definida não é classificado como humano.
- `assets/unified-voices.js`: nas páginas com layout por abas, painéis têm estados ARIA, navegação por teclado e pausa do áudio ao trocar de modalidade em qualquer largura.
- `scripts/unified-catalog.py`: geração persistente de duas abas apenas nas cinco rotas; seleção inicial humana, dados e mídia reais, carregamento de áudio sob demanda e cache de script atualizado nessas páginas.
- `scripts/review-dual-positioning.py`: preserva a comunicação comercial revisada durante a compilação.
- `scripts/test-ads-landings.py`: requisitos atualizados para ambas as modalidades nas cinco páginas, preservando testes de páginas exclusivas.
- `scripts/test-commercial-attribution.cjs`: teste de atribuição e links dinâmicos.

## Validação realizada

- `npm run build`: passou.
- `python scripts/test-ads-landings.py`: 4 testes passaram; cobre estrutura, metadados, JSON-LD, links/âncoras, arquivos locais, preços, composição do catálogo, separação de modalidades, avatares e preservação durante geração.
- `node scripts/test-tracking.cjs`: passou; consentimento, eventos de navegação e uma única conversão UET por clique de WhatsApp.
- `node scripts/test-commercial-attribution.cjs`: passou; parâmetros, âncoras, links dinâmicos, domínios e indisponibilidade de armazenamento.
- Verificação de sintaxe JavaScript e `git diff --check`: passaram.
- Comparação binária com a base: Home, Black Friday, banco principal, vozes IA e locução IA idênticos.

## Limitações e revisão pendente

O ambiente não dispõe de navegador Chromium. A tentativa de instalação pelo Playwright falhou porque o download retornou arquivo inválido. Portanto, não foram validados visualmente os tamanhos 360/390/768/1366/1920 px, a reprodução efetiva de mídia externa, a disponibilidade da fonte remota nem a interação das abas/filtros em navegador real. A existência dos arquivos locais e os estados de fallback foram verificados no código; isso não comprova a reprodução dos áudios. Essas conferências precisam ser feitas no preview do PR antes de autorizar produção.

As regras CSS e os comportamentos novos são delimitados às cinco páginas. Os HTML fora do escopo permanecem idênticos; a ausência de regressão visual dos componentes compartilhados ainda requer navegador.

Nenhuma mudança na conta Microsoft Advertising. Nenhum deploy, merge ou publicação automática solicitado por este trabalho.
