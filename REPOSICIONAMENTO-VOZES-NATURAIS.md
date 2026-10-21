# Reposicionamento Vozes Naturais — 21/10/2026

## Implementado
- Catálogo genérico na home e /vozes/: Vozes Naturais primeiro, Vozes Humanas acessíveis por aba.
- Landings humanas preservam seleção humana; /spot-comercial/ é genérica e abre naturais. /vozes-ia/ e /locucao-ia/ mantêm catálogo específico.
- Nome comercial Vozes Naturais em títulos e links; explicação visível de inteligência artificial, preservando termos técnicos em SEO e URLs.
- Off R$ 8,50 / produção R$ 19,00; humanas R$ 11,90 / R$ 29,90; até 40 segundos. Prazo de até 10 minutos refere-se à locução, sem promessa equivalente para produção completa.
- Cartões naturais direcionam WhatsApp com voz identificada; cartões humanos direcionam a Central de Produção existente.
- Preferência persistida somente com consentimento aceito, removida ao recusar. Sem armazenamento disponível, permanece funcional.
- Links explícitos têm prioridade sobre a preferência: /vozes/?categoria=ia#banco-de-vozes e /vozes/?categoria=human#banco-de-vozes. Âncora direta preservada: /vozes-ia/#buscar-voz.
- Eventos voice_category_view e voice_category_switch usam integração existente; demonstrações e escolha de voz mantêm eventos anteriores. Não há instalação de rastreadores novos.
- Geradores e pipeline atualizados para manter o reposicionamento após build.

## Validação
Build completo aprovado; segunda execução reproduzível sem diferenças. Sintaxe JavaScript e Python aprovada. 6 testes de landing pages e 3 de migração aprovados. Testes de rastreamento/consentimento e atribuição aprovados. git diff --check aprovado.

## Limitações e pendências
Validação visual, interação real das abas/filtros e reprodução de áudio em navegador pendentes: Playwright não dispõe de executável Chromium instalado. Não foi realizada verificação de Core Web Vitals nem validação ao vivo de serviços externos. Dados reais de disponibilidade dos humanos continuam na Central; não foram fabricados status locais. Painel externo, pagamentos, clientes e anúncios não foram alterados.

Sem acesso aos relatórios históricos, não foi registrada uma linha de base de conversões e lucro. Não foi iniciado teste A/B nem agenda automática: a apresentação é reversível pela branch/commit. Recomenda-se comparar 30 dias com volume e origem de tráfego equivalentes, separando cliques de vendas confirmadas.

A publicação ocorre via GitHub Pages conforme README. Esta entrega permanece em branch/PR para revisão; não altera main nem publica produção.

## Arquivos analisados e modificados
Levantamento da árvore do repositório, templates e geradores; revisão automatizada de HTML público, sem modificar arquivos de áudio, imagens, preços de pacotes ou dados de clientes. Relação de arquivos alterados:

- 404.html
- assets/unified-voices.js
- avaliacoes/index.html
- blog/agencia-de-vozes-locucao-comercial/index.html
- blog/audio-para-campanha-eleitoral/index.html
- blog/como-fazer-roteiro-para-carro-de-som/index.html
- blog/index.html
- blog/locucao-comercial-publicitaria/index.html
- blog/locucao-off-o-que-e/index.html
- blog/locucao-para-igrejas-e-eventos-evangelicos/index.html
- blog/locucao-para-supermercado/index.html
- blog/locucao-profissional-como-contratar-locutor/index.html
- blog/propaganda-dia-das-criancas/index.html
- blog/quanto-custa-um-spot-comercial/index.html
- blog/roteiro-spot-black-friday/index.html
- blog/spot-black-friday/index.html
- blog/voz-ia-ou-locucao-humana/index.html
- cadastro/index.html
- calculadora/index.html
- espera-telefonica-ura/index.html
- gravacao-off-e-producao/index.html
- index.html
- indique-e-ganhe/index.html
- locucao-campanha-politica/index.html
- locucao-ia/index.html
- locucao-off/index.html
- locucao-para-video-institucional/index.html
- locucao-voz-infantil/index.html
- locutores/index.html
- off-comercial/index.html
- package.json
- planos-para-agencias-revenda/index.html
- politica-de-privacidade/index.html
- portfolio/index.html
- precos/index.html
- producao-para-igrejas/index.html
- producao-para-supermercados/index.html
- produtora-de-audio-bahia/index.html
- produtora-de-audio-distrito-federal/index.html
- produtora-de-audio-espirito-santo/index.html
- produtora-de-audio-goias/index.html
- produtora-de-audio-minas-gerais/index.html
- produtora-de-audio-parana/index.html
- produtora-de-audio-rio-de-janeiro/index.html
- produtora-de-audio-rio-grande-do-sul/index.html
- produtora-de-audio-santa-catarina/index.html
- produtora-de-audio-sao-paulo/index.html
- scripts/test-ads-landings.py
- scripts/unified-catalog.py
- servicos/index.html
- sobre/index.html
- spot-black-friday/index.html
- spot-comercial-natal/index.html
- spot-comercial/index.html
- spot-para-carro-de-som/index.html
- templates/region-template.html
- templates/site-footer.html
- templates/site-header.html
- termos/index.html
- tutoriais/como-acompanhar-pedido/index.html
- tutoriais/como-adquirir-creditos/index.html
- tutoriais/como-baixar-pedido/index.html
- tutoriais/como-completar-cadastro/index.html
- tutoriais/como-escolher-locutor/index.html
- tutoriais/como-pedir-locucao-off/index.html
- tutoriais/como-pedir-spot-comercial/index.html
- tutoriais/como-preparar-texto/index.html
- tutoriais/como-se-cadastrar/index.html
- tutoriais/como-solicitar-correcao/index.html
- tutoriais/index.html
- vinhetas-para-podcast-e-radio/index.html
- vozes-ia/index.html
- vozes/index.html
- assets/natural-positioning.css
- scripts/natural-positioning.py
