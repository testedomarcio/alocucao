# Banco de vozes — redesign e formulário visível — 27/10/2026

## Alterações

- Cards reutilizáveis redesenhados com bordas suaves, tags legíveis, demonstrações em painéis, espaços equilibrados, CTA inferior alinhado e “Ver perfil completo”. Três colunas em desktop, duas em tablet e uma em celular.
- Selos compactos com ícones SVG e cores próprias: Aida TOP 1 ouro; Aline Mota TOP 2 prata; Fernanda TOP 3 bronze. Posições preservadas conforme confirmação do proprietário. A base histórica é o portfólio publicado; não foi apresentado um total de pedidos inferido desse portfólio.
- Cinco estrelas cinza/zero avaliações preservadas e com link para o resumo no perfil. A integração já preparada continua calculando apenas avaliações aprovadas quando for ativada.
- Todos os 27 cards e perfis têm “Ver últimos trabalhos”, com fone SVG, descrição e seta. Aida, Aline Mota, Fernanda e Zozo levam às seções existentes; as outras 23 vozes abrem diálogo acessível. Escape/fechar/clique externo restauram foco; “Ouvir demonstrações” leva ao player da voz correta, sem autoplay.
- O formulário completo está no HTML de todos os 27 perfis: estrelas, nome, comentário, imagem opcional e consentimento. A âncora `#avalie` agora leva diretamente ao formulário. Os campos são visíveis; **o envio continua desativado até configurar e homologar Supabase e Turnstile e receber convite válido**. Nenhuma confirmação falsa, persistência fictícia ou avaliação de teste foi publicada.
- Estrutura de agregados para pedidos entregues, sem dados individuais. Nenhum número é exibido porque não há fonte oficial integrada. Futuros totais verificados passam a alimentar automaticamente indicadores e ranking no build. Nenhum agendamento foi criado ou reativado.
- Fotos, arquivos de áudio, URLs comerciais, metadados, WhatsApp, idiomas, filtros e ordem aleatória preservados. Ajustada a junção de palavras do título do banco de vozes quando a quebra de linha é ocultada.

## Testes

`npm run build` e `npm test`: passaram (452 entradas de páginas, 27 perfis, 54 demos, sem erros). Incluem regressões existentes e validações do formulário, estado zero, ausência de rede enquanto desativado e agregados de pedidos verificados.

`npm run test:voice-ui` com Chromium: passou nas larguras 360, 820 e 1440. Verificados 27 cards/formulários, quatro links de trabalhos, 23 controles de diálogo, cores e larguras dos selos, grade 1/2/3, foco/teclado, estrelas selecionáveis, botão desativado, ausência de overflow e erros JavaScript. Também passou o fluxo local com API/CAPTCHA simulados para integração habilitada, sem duplicação de formulário, token removido da URL, média recebida e confirmação após resposta do servidor. Essa simulação não substitui a homologação do serviço remoto.

## Pendências

Criar ou conectar projeto Supabase, configurar usuário administrador/Turnstile, aplicar migrações, publicar funções e concluir os testes externos antes de habilitar envio real. O painel preparado fica em `/administracao/avaliacoes/`. O envio do formulário não está ativo em produção e nenhum serviço pago foi contratado.

A fonte real de pedidos entregues permanece pendente; o indicador está oculto. Passos atuais: [implantação das avaliações](../../docs/avaliacoes-implantacao.md).

## Publicação

As alterações são entregues em commit próprio na branch principal; o identificador e a confirmação do GitHub Pages são apresentados na mensagem de entrega. Recursos compartilhados têm novo identificador de cache `20261027cards2`.

## Arquivos alterados ou adicionados

- `administracao/avaliacoes/index.html`
- `assets/nova.css`
- `assets/reviews.css`
- `assets/reviews.js`
- `assets/voice-ui.js`
- `data/delivered-orders.json`
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
- `producao-para-igrejas/index.html`
- `producao-para-supermercados/index.html`
- `scripts/build-nova.py`
- `scripts/test-reviews.mjs`
- `scripts/test-voice-orders.py`
- `scripts/test-voice-ui.cjs`
- `scripts/update-top-voices.py`
- `scripts/voice_orders.py`
- `spot-black-friday/index.html`
- `spot-comercial/index.html`
- `spot_comercial.html`
- `spot_comercial/index.html`
- `spot_supermercado/index.html`
- `spotcomercial/index.html`
- `talentos/index.html`
- `vozes-ia/index.html`
- `vozes/index.html`
- `reports/redesign-vozes-2026-10-27/RELATORIO.md`
