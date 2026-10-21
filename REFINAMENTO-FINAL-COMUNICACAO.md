# Refinamento final de comunicação — 21/10/2026

## Escopo e execução
Site estático publicado por GitHub Pages; não utiliza WordPress. Foram inspecionados os títulos no navegador em 20 páginas comerciais e inventariados 417 arquivos HTML do projeto. As alterações preservam estrutura, estilos, mídias, âncoras, categorias, preços, pacotes e rastreamento. A maioria dos arquivos recebeu apenas ajustes em rótulos compartilhados, rodapé e avisos.

Páginas conferidas no navegador: /, /spot-comercial/, /locucao-off/, /producao-para-igrejas/, /gravacao-off-e-producao/, /producao-para-supermercados/, /vozes-ia/, /servicos/, /precos/, /vozes/, /locutores/, /off-comercial/, /locucao-ia/, /spot-black-friday/, /espera-telefonica-ura/, /locucao-para-video-institucional/, /spot-para-carro-de-som/, /planos-para-agencias-revenda/, /spot-comercial-natal/ e /sobre/.

## Títulos e textos
Os títulos das sete páginas prioritárias foram preservados, com acréscimo de (IA) no título da página exclusiva de vozes naturais. Títulos genéricos centrados na tecnologia foram substituídos somente nas páginas abaixo. Metadados comerciais correspondentes foram revisados. A modalidade IA continua identificada nas páginas específicas e nos contextos de escolha.

- /servicos/: Locução e produção de áudio para sua comunicação.
- /precos/: Confira os preços de locução e produção de áudio.
- /espera-telefonica-ura/: Locução profissional para URA e espera telefônica.
- /locucao-para-video-institucional/: A voz certa para seu vídeo institucional.
- /spot-para-carro-de-som/: Sua propaganda pronta para o carro de som.
- /planos-para-agencias-revenda/: Locução e produção para agências e revendedores.
- /spot-comercial-natal/: Sua campanha de Natal com uma mensagem marcante.
- /sobre/: A voz certa para sua mensagem, do início ao áudio pronto.

Avisos de origem foram encurtados para uma identificação objetiva. Rodapé passou a apresentar os serviços. Rótulos de seleção usam Vozes Naturais (IA). Preços e prazos ficam no contexto da oferta e nas FAQs, evitando sua repetição no aviso de tecnologia.

## FAQs
Adicionada a diferença entre voz humana e voz natural (IA) à inicial, spot, Off, igrejas, supermercados e banco de vozes. Na página exclusiva de IA, a pergunta equivalente foi reformulada, sem duplicação. Prazos atualizados nos FAQs existentes: humana de 10 a 30 minutos ou de 1 a 2 horas conforme disponibilidade; natural (IA) até 10 minutos; produção completa estimada de 1 a 2 horas após a conclusão da gravação. Ajustadas respostas de preços e conteúdo da produção em igrejas, Off e supermercados. Corrigida frase quebrada sobre Off na página spot. FAQs dos catálogos agora explicam corretamente WhatsApp para IA e Central para humanas. Dados estruturados FAQPage existentes acompanham as perguntas visíveis.

## Botões e WhatsApp
Cartões usam “Quero esta voz”, preservando classes e atributos de rastreamento. Mensagem natural: “Olá! Gostei da voz natural (IA) [nome] e gostaria de solicitar uma gravação.” O identificador da página de origem permanece na mensagem dos cartões. Botões genéricos da página exclusiva de IA foram encurtados, preservando o número. Cartões humanos continuam abrindo a Central de Produção, conforme o fluxo existente; não foram redirecionados ao WhatsApp. Nenhuma mensagem foi enviada.

## Verificação local
Build completo e segunda execução reproduzível; 6 testes de landing pages e 3 de migração aprovados; testes de atribuição, consentimento/rastreamento, calculadora e Black Friday aprovados. Auditoria SEO: 64 páginas no sitemap, sem erros. Comparação de todas as páginas alteradas: tags de mídia, IDs de âncoras e canonicals idênticos à versão anterior; JSON-LD válido. git diff --check aprovado.

## Limites
Não houve simulação de compra, alteração em painel, anúncios, pagamentos, pedidos ou ferramentas analíticas. A conferência visual no navegador desta etapa é em computador; não há emulação móvel disponível no navegador conectado. CSS e estrutura de layout não foram alterados. Disponibilidade humana permanece dependente da Central externa; não foram criados status ou prazos de locutores individuais.

## Arquivos modificados
- 404.html
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
- scripts/generate-vozes-ia.py
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
- scripts/refine-commercial-copy.py
