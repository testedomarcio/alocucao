# Amostra personalizada gratuita — 29/10/2026

Melhoria comercial autorizada por Márcio, incluindo publicação após finalizar.

## Locais

- Home: chamada e botão na primeira área de conversão; painel após a abertura com oferta, condições expansíveis e três benefícios.
- Locução Off e Spot Comercial: painel após o hero, com mensagem de WhatsApp específica do serviço. URLs canônicas e aliases preservados.
- Banco de vozes: oferta após a introdução; indicador e link textual nos cards elegíveis, sem substituir contratação ou players.
- 27 perfis do catálogo próprio: oferta junto às demonstrações, identificando a voz no WhatsApp. Avaliações e trabalhos permanecem.

## Disponibilidade

`data/sample-availability.json` mantém a lista explícita de vozes próprias elegíveis. Somente `exclusive: true` e `accepting_orders: true` habilitam o status e a solicitação. Catálogo legado de terceiros não foi incluído. O status estático “Disponível para pedidos” não representa pessoa online nem atendimento imediato. Desativar `accepting_orders` suspende a oferta após executar o build.

Condições próximas ao CTA: gratuidade, ausência de obrigação, possibilidade de trecho parcial, demonstração completa a critério da equipe, marca d'água, vedação de uso comercial sem contratação/autorização, atendimento em Brasília e prazo combinado. Spot não garante trilha ou produção completa na amostra.

## Arquivos de implementação

- `scripts/sample_offer.py`: componentes e escopo da oferta.
- `scripts/build-nova.py`: integra os componentes no gerador; preserva os links de avaliações já publicados e as datas existentes do sitemap.
- `assets/sample-offer.css`: apresentação responsiva com a identidade vigente.
- `data/sample-availability.json`: configuração de elegibilidade.
- `assets/tracking.js`: eventos GA4 de intenção e classificação das rotas compatíveis de Spot.
- `scripts/test-nova.cjs`: verifica unicidade do evento WhatsApp mesmo havendo eventos analíticos de intenção.
- `scripts/test-sample-tracking.cjs` e `scripts/test-sample-offer.py`: consentimento, eventos, mensagens, suspensão de elegibilidade e preservação do conteúdo.
- `package.json`: inclui as verificações no fluxo existente.
- HTML gerado: home, banco, 27 perfis, duas landing pages e aliases existentes.

## Medição

Eventos `solicitar_amostra_click`, `contratar_locucao_click` e `escolher_voz_click`. O evento existente `whatsapp_click` continua sendo enviado uma única vez por clique, com `cta_intent`, página, serviço e voz. Eventos adicionais não são enviados como conversões de Ads/UET. Nada é medido sem consentimento analítico. A configuração de eventos-chave no GA4 não foi alterada.

## Verificação

Build e suíte npm. Comparação com a revisão anterior preserva títulos, descrições, canonicals, tags de áudio, seções de preços, calculadoras e avaliações publicadas. Testes de mensagens para todos os perfis elegíveis e os dois serviços; elegibilidade desativada não recebe oferta. Revisão visual no Chrome em desktop e viewport de 390 pixels por iframe: home, Spot, Off, banco e Christine. Filtro por Christine e condições expansíveis funcionam; nenhum overflow horizontal nas telas mobile inspecionadas. Players mantêm os arquivos e carregamento sob demanda; suíte confirma pausa de outros players ao iniciar reprodução.

A implementação não gera nem baixa amostras, não consulta status de pessoas e não promete execução imediata.
