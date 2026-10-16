# Revisão da contratação — 16/10/2026

Implementado: WhatsApp preservado como principal caminho comercial; alternativa “Fazer pedido online”; acesso permanente “Área do Cliente” no cabeçalho e rodapé. Trabalho baseado no commit 327f78ad19d5d4cbcd7bb2296219817d611f2e32, preservado no histórico para reversão.

## Páginas

Revisados 60 documentos HTML de conteúdo: início; Off; Spot; concorrentes/pacotes (/gravacao-off-e-producao/); igrejas; supermercados; Black Friday; Natal; calculadora; preços; vozes; serviços; portfólio; URA; vídeo institucional; voz infantil; agências/revenda; campanha política; carro de som; vinhetas; dez páginas regionais; blog e artigos; tutoriais; sobre; avaliações; indicação; privacidade; termos; 404. Nas páginas informativas e legais, apenas navegação e acesso ao cliente, sem nova seção comercial no conteúdo. Perfis antigos que já redirecionam para o catálogo foram preservados.

## Botões e orientação

- Início e páginas comerciais com ações existentes: pedido online ao lado da ação principal de WhatsApp e link menor de login. Igrejas recebem opção visualmente mais discreta.
- Concorrentes: WhatsApp primeiro, pedido online visível e preservação das condições promocionais existentes.
- Calculadora: pedido online ao lado do WhatsApp somente na área de resultados; link de login separado. Ferramenta gratuita e cálculo preservados.
- Preços e catálogo: opção de contratação independente no conteúdo, além da navegação permanente.
- Início, Off, Spot, preços, vozes, igrejas e supermercados: orientação sobre autonomia, compra de créditos, escolha da voz, acompanhamento, downloads e suporte para dificuldade de pagamento.
- Central disponível para envio de pedidos 24h; gravação e entrega dependem do prazo e da disponibilidade. Horário do atendimento pelo WhatsApp explicitado conforme contexto atual: segunda a sexta 08h–18h; sábado 08h–12h; exceto feriados; Brasília.
- Pedidos assistidos: uso dos dados de acesso fornecidos para acompanhar e baixar arquivos; expediente e demanda podem afetar envio pelo atendente.

Cadastro: https://vozes.alocucao.com.br/painel/cadastro

Login: https://vozes.alocucao.com.br/painel/

As rotas antigas /cadastro/ e /painel/ foram mantidas e passam a encaminhar aos destinos oficiais correspondentes. Mensagens existentes do WhatsApp foram preservadas.

## Preços e promoções

Nenhum preço foi modificado. A página de concorrentes já apresentava primeira compra de Off por R$ 7,90 e Produção por R$ 19,90, diferentes das referências antigas do histórico; esses valores existentes foram preservados. Black Friday e calculadora mantêm as próprias ofertas existentes. Descontos dependentes de validação pelo WhatsApp não foram prometidos no painel.

## Medição

Mantidos GA4 G-TBHF64CH1R, UET 187279262 e configuração publicitária existente, com consentimento negado inicialmente. Um listener compartilhado mede whatsapp_click e panel_click; panel_action diferencia register/login; page_path e cta_id identificam origem. UET diferencia panel_register_click e panel_login_click. Removida duplicação de panel_click na página de concorrentes. Removida regra que convertia links de cadastro em WhatsApp. Geradores antigos passam a preservar estratégia híbrida.

Nenhuma compra, cadastro concluído ou falha de pagamento foi inferida a partir de cliques. Não há integração com o pagamento do painel externo. Campanhas e lances não foram alterados.

## Validação realizada

- Testes de rastreamento: consentimento concedido/revogado, domínios permitidos, apenas um evento por clique, login/cadastro e origem por serviço.
- Testes da calculadora: inicialização, 10s/40s/41s/90s, 1/2/3 créditos, limpeza e CTA online único.
- Comparação dos 60 HTMLs: preservados title, descrição, canonical, H1, JSON-LD, elementos audio, iframes e destinos originais do WhatsApp.
- Scripts JavaScript sem erro de sintaxe; scripts Python compilam; diff sem erros de espaços.
- Normalização híbrida idempotente: nova execução não altera páginas já ajustadas.
- Cadastro e login externos abertos no navegador, sem envio de dados ou criação de conta.

## Limitações e recomendações

Não foi possível verificar pagamento real, cadastro concluído, histórico autenticado ou download de um pedido de cliente. O painel externo não foi editado. Verificação de responsividade em CSS; não houve teste em aparelho móvel físico nem medição Lighthouse. Não há garantia de desempenho ou conversão apenas por inspeção de código.

Comparar após aproximadamente 30 dias, a partir de 15/11/2026: cliques por página e canal e vendas reais conciliadas com registros do atendimento/painel. Configuração de eventos de compra requer integração legítima ao painel e confirmação de pagamento. Cliques de cadastro expressam intenção de novo pedido; cliques de login expressam intenção de acesso e não comprovam identidade de cliente.
