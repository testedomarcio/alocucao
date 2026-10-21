# Correções do banco de vozes — 21/10/2026

## Resultado

Catálogo de IA com 25 perfis, 24 perfis com áudio e 25 demonstrações (David tem duas). Todas as vozes IA permanecem Online para solicitação; Thiago continua com “Demonstração em breve”. Zozo permanece masculina.

A nova leitura completa da pasta Drive retornou 25 arquivos de áudio. Os 18 anteriores foram preservados e os sete novos foram integrados:

| Arquivo | Ação |
| --- | --- |
| Will.mp3 | Preencheu perfil pendente |
| Aida.mp3 | Preencheu perfil pendente |
| Ana Alice.mp3 | Preencheu perfil pendente |
| Leonardo.mp3 | Novo perfil Leonardo |
| Leonardo Br.mp3 | Novo perfil Leonardo BR, separado de Leonardo |
| Christine.mp3 | Novo perfil Christine |
| David (1).mp3 | Opção adicional no perfil David, original preservado |

As associações usam os nomes exatos dos arquivos. O sufixo “(1)” não foi interpretado como autorização para apagar ou substituir o original. IDs do Drive e durações estão registrados nos dados. Os originais do Drive e as fotos humanas na fonte oficial não foram alterados. As imagens dos novos perfis IA são retratos ilustrativos fictícios.

## Correções

- Causa dos avatares: `humanRow` colocava a inicial como texto e depois acrescentava a imagem no mesmo elemento. O componente agora cria exclusivamente a imagem ou a inicial. Erros de carregamento trocam todo o conteúdo pela inicial. A mesma proteção atende ao HTML inicial e às listas atualizadas em todas as 20 páginas com o componente.
- Avatares circulares, centralizados e com dimensão uniforme em cada faixa de tela.
- Página IA em lista horizontal de largura completa no computador; avatar, identificação, gênero/estilo, descrição, Online, player e botão verde WhatsApp por linha. Em telas pequenas os controles se reorganizam. Filtros de nome, gênero e estilo preservados.
- Seletor de demonstrações de David sem reprodução automática; troca pausa e descarrega o áudio anterior.
- Reprodução sob demanda, sem autoplay; início de outro áudio interrompe o anterior, inclusive portfólio. Mensagem de erro e atendimento WhatsApp preservados.
- Ordem aleatória por carregamento com classificação estável ao pesquisar, filtrar e expandir resultados; atualização não troca as linhas durante a reprodução.
- Conteúdo comercial, benefícios IA, FAQ, metadados, SEO, preços, portfólio, sistema original de locutores, disponibilidade ao vivo, pedidos e cadastro preservados. Nenhuma configuração desses sistemas foi modificada.

## Validação

- Build completo sem erro; verificador SEO com 61 URLs e zero erros.
- Testes DOM do HTML real com 116 humanos e 25 IA: foto sem texto, fallback em erro, abas móveis, pesquisa sem acentos, filtros, paginação 12/24/25, Zozo masculina, ordem estável e visitas aleatórias, seleção da demonstração adicional, reprodução única e eventos de medição.
- Os 25 MP3 IA foram integralmente decodificados sem erro; David original conferido byte a byte contra a versão anterior. Uma cópia vazia foi detectada e reconvertida do original antes da publicação.
- Todas as 20 páginas com catálogo conferidas: quantidades, avatar exclusivo, status Online IA, destinos WhatsApp e preservação das URLs de áudio anteriores.
- Testes de consentimento e tracking aprovados; sintaxe JavaScript e diff sem erro.
- Revisão das regras responsivas para desktop, tablet e celular. Não houve teste visual em navegador real nem reprodução em aparelho físico: o navegador de validação exigido pelo ambiente não estava disponível. Os testes DOM simulam eventos de mídia, sem substituir a audição humana ou testes reais no Safari/Chrome móvel.

Preços mantidos por até 40 segundos: humana Off R$ 11,90 / produzida R$ 29,90; IA Off R$ 8,50 / produzida R$ 19,00.
