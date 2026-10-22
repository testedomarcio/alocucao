# Integração do Painel de Gravação — 22/10/2026

Implementação no site estático existente, publicado no GitHub Pages. O sistema interno de gravação permanece externo.

## Alterações

- Cabeçalhos: serviços, banco de vozes, preços, apresentação do painel, entrar, criar conta grátis e WhatsApp. Menu acessível no celular.
- Rodapés: cadastro e acesso à conta; horários de pedidos e suporte diferenciados.
- Primeira dobra das landing pages: WhatsApp em destaque, cadastro como ação secundária.
- Bloco do painel após as demonstrações e preços, com captura real fornecida pelo proprietário em moldura CSS de notebook; imagens WebP responsivas.
- Catálogo antigo substituído pelo iframe oficial, uma instância por página. Exemplos de trabalhos produzidos preservados.
- Redimensionamento do iframe valida origem exata, janela remetente, sinalizador booleano, altura numérica finita e intervalo seguro.
- Como funciona: percursos pelo painel e pelo WhatsApp; perguntas frequentes atualizadas.
- Off R$ 10,00 e Produção Completa R$ 25,00 por crédito de até 40 segundos, inclusive metadados, ofertas estruturadas e textos de mensagens nos links.
- WhatsApp: segunda a sexta, 8h às 18h. Pedidos no painel: 24h. Gravações até as 22h, conforme a disponibilidade.
- Métricas existentes preservadas: cadastro e login medidos como navegação, WhatsApp como contato, sujeitos ao consentimento. Não são vendas nem cadastros concluídos.
- A rotina de geração termina com a política de integração, para preservar as alterações em atualizações futuras.

## Páginas com bloco do painel e catálogo integrado

- https://alocucao.com.br/
- https://alocucao.com.br/espera-telefonica-ura/
- https://alocucao.com.br/gravacao-off-e-producao/
- https://alocucao.com.br/locucao-campanha-politica/
- https://alocucao.com.br/locucao-ia/
- https://alocucao.com.br/locucao-off/
- https://alocucao.com.br/locucao-para-video-institucional/
- https://alocucao.com.br/locucao-voz-infantil/
- https://alocucao.com.br/locutores/
- https://alocucao.com.br/off-comercial/
- https://alocucao.com.br/planos-para-agencias-revenda/
- https://alocucao.com.br/precos/
- https://alocucao.com.br/producao-para-igrejas/
- https://alocucao.com.br/producao-para-supermercados/
- https://alocucao.com.br/produtora-de-audio-bahia/
- https://alocucao.com.br/produtora-de-audio-distrito-federal/
- https://alocucao.com.br/produtora-de-audio-espirito-santo/
- https://alocucao.com.br/produtora-de-audio-goias/
- https://alocucao.com.br/produtora-de-audio-minas-gerais/
- https://alocucao.com.br/produtora-de-audio-parana/
- https://alocucao.com.br/produtora-de-audio-rio-de-janeiro/
- https://alocucao.com.br/produtora-de-audio-rio-grande-do-sul/
- https://alocucao.com.br/produtora-de-audio-santa-catarina/
- https://alocucao.com.br/produtora-de-audio-sao-paulo/
- https://alocucao.com.br/servicos/
- https://alocucao.com.br/spot-black-friday/
- https://alocucao.com.br/spot-comercial/
- https://alocucao.com.br/spot-comercial-natal/
- https://alocucao.com.br/spot-para-carro-de-som/
- https://alocucao.com.br/vinhetas-para-podcast-e-radio/
- https://alocucao.com.br/vozes/

## Verificações

- Build completo e verificações de integridade das landing pages, preços, links, âncoras, identificadores únicos e dados estruturados.
- Segurança do postMessage, consentimento e eventos, calculadora e migração de vozes.
- Auditoria de SEO: 64 páginas do sitemap sem erros.
- Navegador: cadastro e login oficiais; busca por Koraly no iframe e ajuste automático de altura; inspeção visual em desktop.
- Viewport de celular incorporado de 390 px (375 px úteis): menu, botões de 49 px e ausência de rolagem horizontal na landing de spot.

## Limitações

- Os nomes, símbolos, avaliações, botões e regras dentro do iframe pertencem ao provedor externo. O iframe exibe 🧠 em algumas vozes; o site institucional não altera esse conteúdo.
- Não é possível medir cliques internos do iframe a partir do domínio institucional sem um protocolo de eventos adicional do provedor. Nenhum evento de compra ou cadastro concluído foi presumido.
- Login e cadastro foram verificados sem criar conta, pagar créditos ou enviar pedidos de teste.
- O banner de Black Friday presente na captura é parte da imagem real fornecida; não foi criado um prazo promocional adicional.
