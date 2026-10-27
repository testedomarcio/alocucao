# Avaliações manuais e novo trabalho de Diego — 27/10/2026

## Resultado

O formulário foi removido dos **27 perfis**, e nenhuma página pública carrega a integração de recebimento automático. O endereço antigo `#avalie` permanece como âncora de compatibilidade para a seção de avaliações, sem formulário. O antigo painel informa que a gestão é manual. O projeto Supabase foi pausado, com estado `INACTIVE` confirmado; não foi apagado.

Foram publicados os três depoimentos fornecidos pelo proprietário em `Avaliações.txt`, preservando o teor dos comentários, inclusive a crítica construtiva e a nota de três estrelas:

| Voz | Cliente | Nota | Média/contador no perfil e nos cards |
| --- | --- | --- | --- |
| Diego | Evandro — Ponto do Pastelão | 5 | 5,0/5 · 1 avaliação |
| Enzo | Matheus — Rádio Mellody FM | 5 | 5,0/5 · 1 avaliação |
| Fernanda | Rubner Estaquio — LEMEDE ULTRASSOM em IPATINGA | 3 | 3,0/5 · 1 avaliação |

As duas imagens fornecidas foram otimizadas para WebP, preservando seu conteúdo, e hospedadas no próprio site. Nenhuma fotografia foi criada para Rubner. A data exibida corresponde à publicação no site, sem inventar a data do envio do depoimento.

A fonte pública `data/customer-reviews.json` e o componente reutilizável calculam médias e contadores a cada build. Não foram inseridos dados de contato, identificadores privados de pedidos ou rótulos de verificação não comprovados. Os demais locutores continuam com cinco estrelas cinza e zero avaliações. As posições TOP 1/2/3 foram mantidas e são independentes das notas.

## Trabalho do Diego

Importado da pasta fornecida, identificada como “Diego”, o arquivo “Ponto do Pastelão - Produção - Locutor Diego - 27/10/2026.mp3”. A data, voz, cliente e formato vieram do nome do arquivo. O áudio original foi preservado: 1.225.709 bytes e aproximadamente 51,04 segundos, validados por ffprobe. Publicado em `assets/trabalhos/diego-2026-10-27-ponto-do-pastelao.mp3` e incluído na seção `#ultimos-trabalhos`. O card de Diego agora aponta diretamente para essa seção. Não há link público para a pasta do Drive no perfil.

## Validação

- Build: 452 entradas de páginas, 27 perfis, 54 demos preservadas; validação geral sem erros.
- `npm test`: passou, incluindo médias reais, notas originais 5/5/3, estado sem avaliações, validação de dados e ausência de formulário/scripts automáticos em todos os perfis.
- Chromium/Playwright em 360, 820 e 1440 pixels: passaram filtros, selos, modal, players presentes, médias/contador e preenchimento dourado corretos. Os três perfis com depoimentos foram inspecionados; as duas imagens carregam e não há overflow ou erro JavaScript. Agora há cinco vozes com portfólio e 22 com mensagem de novidades.
- Sem publicação de avaliações fictícias. O recebimento por Supabase foi cancelado. A tentativa de configurar limpeza automática foi recusada pela revisão automática por envolver exclusão definitiva; nenhum agendamento desse tipo foi criado.

## Manutenção

Receber pelo atendimento o nome público, voz, nota original de 1 a 5, comentário e eventual imagem; obter autorização do cliente para publicação. Incluir somente depoimentos aprovados no arquivo público, executar `npm run build && npm test` e publicar. A média e a contagem se atualizam em todos os locais sem edição duplicada. Instruções no README.

## Arquivos

- `README.md`
- `administracao/avaliacoes/index.html`
- `assets/reviews.css`
- `assets/reviews/evandro-ponto-do-pastelao.webp`
- `assets/reviews/matheus-radio-mellody-fm.webp`
- `assets/trabalhos/diego-2026-10-27-ponto-do-pastelao.mp3`
- `data/customer-reviews.json`
- `data/latest-works.json`
- `data/legal-pages.json`
- `docs/avaliacoes-implantacao.md`
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
- `scripts/build-nova.py`
- `scripts/manual_reviews.py`
- `scripts/test-manual-reviews.py`
- `scripts/test-reviews.mjs`
- `scripts/test-voice-ui.cjs`
- `sitemap.xml`
- `spot-black-friday/index.html`
- `spot-comercial/index.html`
- `spot_comercial.html`
- `spot_comercial/index.html`
- `spot_supermercado/index.html`
- `spotcomercial/index.html`
- `talentos/index.html`
- `vozes-ia/index.html`
- `vozes/index.html`
- `reports/avaliacoes-manuais-2026-10-27/RELATORIO.md`
