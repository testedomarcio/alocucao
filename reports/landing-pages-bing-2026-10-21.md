# Landing pages comerciais — revisão de 21/10/2026

Implementação no repositório `testedomarcio/alocucao`, sobre `aac24b8c`.

| Página | Alterações | Validação |
|---|---|---|
| /off-comercial/ | Substitui redirect HTML/JavaScript e noindex por página comercial própria, canonical próprio, aplicações publicitárias e sitemap; Off humano R$ 11,90 | Código, SEO e navegador aprovados |
| /locucao-off/ | Off humano avulso R$ 11,90; WhatsApp; vitrine de 10 locutores | Código, SEO e navegador aprovados |
| /producao-para-igrejas/ | Só humanas; R$ 29,90; navegação focada; preservados Monte Moriá e Culto de Celebração, inclusive Off separado | Código, SEO e navegador aprovados |
| /gravacao-off-e-producao/ | Só humanas; Central, cadastro, painel e pacotes preservados; retirada afirmação não comprovada sobre validade de créditos e liberação imediata | Código, SEO e navegador aprovados |
| /producao-para-supermercados/ | Só humanas; Off R$ 11,90 e produção R$ 29,90; portfólio Bethy preservado; vitrine de varejo | Código, SEO e navegador aprovados |
| /spot-black-friday/ | Só humanas; preservada promoção R$ 8,90 / R$ 16,90 até 10/11/2026; corrigida falha em elemento ausente na expiração; schema com priceValidUntil | Código, SEO, navegador e limites da data aprovados |
| /locucao-ia/ | Oferta exclusivamente IA R$ 8,50 / R$ 19,00; catálogo IA preservado; FAQ revisada sem políticas inventadas; canonical próprio; WhatsApp | Código, SEO e navegador aprovados |

Todos os preços são por gravação de até 40 segundos. Pacotes humanos preservados: Off 5/25/50/160/250 créditos por R$ 50/150/200/600/875 e produção 10/15/30 créditos por R$ 200/225/300, conferidos contra a tabela existente do projeto. O catálogo completo /vozes-ia/ permanece disponível.

## Causas corrigidas

O build executava dois normalizadores antigos. `review-dual-positioning.py` recolocava IA, comparativos e preços nas páginas humanas. `standardize-layout.py` restaurava menus, rodapés e CTAs de painel. As páginas comerciais agora preservam seu conteúdo próprio. O gerador e a atualização JavaScript limitam as vitrines humanas a 10 perfis com foto/áudio da fonte oficial, priorizando os estilos conforme a página e excluindo o perfil Teste das vitrines comerciais. O catálogo completo não foi reduzido.

Foram removidos das páginas restritas os destinos /painel/, /painel/cadastro, Área do Cliente, pedido online, cadastro e navegação comercial IA nas páginas humanas. Não foi desativado nenhum sistema. Fotos e fallback continuam mutuamente exclusivos; regra [hidden] reforçada para impedir mensagens de erro sempre visíveis.

/off-comercial/ agora tem conteúdo próprio, não usa redirecionamento de cliente e mantém os parâmetros recebidos. A normalização sem barra é feita pela hospedagem GitHub Pages. Não foram alteradas URLs nem configurações de anúncios.

## Medição

Preservados GA4 G-TBHF64CH1R, Google Ads AW-18420702149, UET 187279262, consentimento e evento existente whatsapp_click. Acrescentados classificação de /locucao-ia/ e /off-comercial/ e campos voice_kind, voice_name e service_selected (a_confirmar quando ainda não escolhido). Mensagens personalizadas por página e por voz. Nenhuma conversão nova criada nas plataformas; nenhuma conversão de compra inferida. Reprodução de áudio continua sem gerar lead UET. Identificar corretamente os cliques não comprova recebimento ou venda pelo WhatsApp.

## Testes executados

- Build completo npm run build, incluindo os geradores; separação continua preservada após o build.
- scripts/test-ads-landings.py: limites comerciais, links, preços, metadados, canonical/indexação, catálogo, avatares, portfólio, âncoras e existência de arquivos locais.
- scripts/test-black-friday.cjs: oferta ativa, último segundo de 10/11 em Brasília e expiração em 11/11, sem erro de elemento ausente.
- scripts/test-tracking.cjs: consentimento, evento único, classificação de leads humanos/IA, painel e exclusão de reprodução como lead.
- scripts/test-voice-migration.py: atualizada a fixture antiga HTML para o formato JSON atual do fornecedor; preservada rejeição de catálogo inválido. Parser diferencia offline, indisponível, retorno e status desconhecido.
- scripts/test-calculator.cjs e scripts/seo-consistency.py: aprovados; 64 URLs no sitemap sem erros.
- Sintaxe JavaScript e git diff --check aprovados. Não há comando lint no projeto.
- Conferência no navegador das sete páginas, sem overflow horizontal em desktop, sem links indevidos e sem foto/inicial simultâneas. Reprodução confirmada de Celso Ricardo (readyState 4, 137,64s) e Will IA (readyState 4, 32,94s).
- 13 endpoints de áudio humano das seleções retornaram audio/mpeg com cabeçalhos válidos no ffprobe; alguns arquivos grandes foram lidos até o limite de 5 MB. Os 29 MP3 locais (IA e portfólio) tiveram cabeçalhos/duração validados.
- Pasta original do Drive consultada: 25 arquivos, todos associados por drive_id aos dados existentes, incluindo segunda demonstração de David. Thiago continua sem arquivo correspondente e sem player falso.

As regras responsivas foram revisadas; não houve teste em aparelho físico nem medição de Core Web Vitals de usuários reais. O editor de navegador disponível foi usado em desktop. Nenhum resultado de posicionamento ou de conversão é garantido.

## Publicação

Publicação segue o GitHub Pages existente após integração da Pull Request. O status final do deploy e o link da PR são informados na entrega da conversa, após consulta ao GitHub e às URLs públicas.
