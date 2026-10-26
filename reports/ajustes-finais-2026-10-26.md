# Ajustes finais — A Locução
26 de outubro de 2026

## Resultado publicado

- Peter removido do catálogo, diretório, perfil e sitemap. A antiga página responde 404, conforme a remoção solicitada.
- Zozo atualizado com retrato masculino ilustrativo, de acordo com o perfil animado, expressivo e alegre. A nova imagem foi conferida na página publicada.
- 26 perfis ativos, com 52 players e 51 arquivos distintos. A ordem é sorteada em cada acesso, inclusive no retorno pelo histórico.
- Aviso extenso retirado de baixo dos catálogos. O rodapé global mantém uma observação legível com link para a seção de tecnologia dos Termos. Os perfis mantêm esclarecimento próprio sobre a natureza da voz.
- Preços e atendimento preservados: Off R$ 12,00 e Produção Completa R$ 25,00 por peça comercial de até 40 segundos; segunda a sexta 08h–18h e sábado 08h–12h, Brasília.

## Melhorias das landing pages

As URLs /spot_comercial e /locucao_off foram preservadas. A primeira seção agora apresenta o serviço, o preço, a contratação pelo WhatsApp e exemplos reproduzíveis.

Na página de Spot, Produção Completa aparece primeiro. Na página de Off, Locução Off aparece primeiro. Ambos os formatos continuam acessíveis. As mensagens de contratação identificam o serviço ou a voz escolhida.

Na medição visual realizada em viewport de 1363 × 936, o preço terminou a aproximadamente 457 pixels do topo e o botão principal a 536 pixels, nas duas páginas. Antes, o preço ficava em uma seção posterior. Não havia rolagem horizontal nas quatro páginas principais inspecionadas.

O catálogo ganhou título inicial mais compacto, fotos proporcionais, cartões alinhados, áreas clicáveis ampliadas e sequência de títulos adequada a leitores de tela. As cores e a identidade visual da reformulação foram mantidas.

## Demonstrações importadas nesta atualização

| Voz | Novos arquivos |
|---|---|
| Aida | Off e Produção Completa |
| Aline Mota | Produção Completa |
| Eduardo S. | Off e Produção Completa |
| Enzo | Off e Produção Completa |
| Fernanda | Off e Produção Completa |
| Marcio | Off e Produção Completa |
| Thiago | Off |

Foram adicionados 12 arquivos, sem substituir os 39 arquivos corretos já hospedados. As 12 novas URLs responderam HTTP 200, sem redirecionamentos.

Os dois arquivos de Thiago fornecidos no Drive eram idênticos. O responsável confirmou que se trata de Off e autorizou sua utilização nos dois players até a atualização. O player de Produção está identificado como amostra temporária de Locução Off, sem trilha ou produção. É a única substituição temporária.

## Situação por perfil

| Perfil | Locução Off | Produção Completa |
|---|---|---|
| Aida | Disponível | Disponível |
| Aline Mota | Disponível | Disponível |
| Amanda Kelly | Disponível | Disponível |
| Ana Alice | Disponível | Disponível |
| Audrey | Disponível | Disponível |
| Cássio Cruz | Disponível | Disponível |
| Christine | Disponível | Disponível |
| David | Disponível | Disponível |
| Diego | Disponível | Disponível |
| Eduardo S. | Disponível | Disponível |
| Enzo | Disponível | Disponível |
| Fernanda | Disponível | Disponível |
| Kaique | Disponível | Disponível |
| Koraly | Disponível | Disponível |
| Larissa | Disponível | Disponível |
| Lax | Disponível | Disponível |
| Leão Antonio | Disponível | Disponível |
| Leonardo | Disponível | Disponível |
| Marcio | Disponível | Disponível |
| Noel Natal | Disponível | Disponível |
| Paulo Becker | Disponível | Disponível |
| Roberta | Disponível | Disponível |
| Thiago | Disponível | Amostra temporária do mesmo Off |
| Will | Disponível | Disponível |
| Zozo | Disponível | Disponível |
| Mário | Disponível | Disponível |

Todos os e-mails profissionais permanecem publicados segundo a confirmação do responsável. Não foi criada nova caixa de e-mail nesta execução.

## Testes concluídos

- Build e verificações de 443 páginas geradas, 89 URLs no sitemap, canonicals, links locais, âncoras, arquivos e telefone de contratação.
- Integridade técnica de 51 MP3 distintos, analisados com ffprobe.
- Reprodução real iniciada nos 52 players do catálogo publicado. Todos carregaram com duração válida e sem erro de mídia.
- Reprodução real das duas demonstrações nos 26 perfis individuais, sem erro de mídia. A reprodução de um player pausou o anterior.
- Player principal de Produção Completa na landing page testado no navegador.
- Conferência das mesmas referências de áudio usadas na home e nas demais landing pages.
- Ordem aleatória observada em dois acessos sucessivos. Busca sem acento por “Cassio” encontrou uma voz; busca por “Peter” encontrou zero. Filtros combinados de voz feminina e estilo comercial funcionaram.
- Testes de consentimento aceito, negado e revogado; carregamento único das tags; identificação da voz, serviço, página e campanha; apenas o clique em WhatsApp disparando o evento de contato.
- Publicação e verificações no GitHub concluídas com sucesso.

Não foram enviados pedidos ou mensagens de WhatsApp, nem modificadas campanhas, anúncios, palavras-chave, sistemas de terceiros ou DNS.

## Desempenho e acessibilidade

Resultados laboratoriais de PageSpeed após as melhorias. Não representam garantia de conversão, teste completo de acessibilidade ou dados de usuários reais.

| Página | Dispositivo | Desempenho | Acessibilidade | Boas práticas | SEO |
|---|---|---:|---:|---:|---:|
| Home | Desktop | 100 | 100 | 100 | 100 |
| Spot Comercial, URL principal | Desktop | 100 | 100 | 100 | 100 |
| Locução Off, URL principal | Desktop | 100 | 100 | 100 | 100 |
| Home | Mobile simulado | 100 | 100 | 100 | 100 |
| Spot Comercial, URL principal | Mobile simulado | 100 | 100 | 100 | 100 |
| Locução Off, URL principal | Mobile simulado | 100 | 100 | 100 | 100 |
| Banco de Vozes | Mobile simulado, última medição | 93 | 100 | 100 | 100 |

As páginas principais tiveram LCP laboratorial de aproximadamente 0,2–0,3 segundo no desktop e 1,0–1,1 segundo no mobile. No catálogo mobile, a última medição apontou CLS 0,164; permanece como oportunidade de melhoria de estabilidade visual. Também restam recomendações leves de cache e cadeia de carregamento. A inicialização aleatória foi antecipada, mas não se declara eliminado o CLS observado.

Não havia dados de campo suficientes na resposta para validar Core Web Vitals de usuários reais.

## SEO, URLs e rastreamento

As duas URLs com sublinhado, inclusive com parâmetros UTM e msclkid de teste, responderam HTTP 200 sem redirecionamentos e sem perder os parâmetros.

As páginas principais /spot-comercial/ e /locucao-off/ continuam indexáveis. As variantes equivalentes mantêm canonical para a principal e noindex para evitar duplicação. Por esse motivo, o teste de SEO das variantes com sublinhado acusou bloqueio de indexação; isso não significa que a landing page esteja inacessível aos anúncios.

Os aliases existentes foram mantidos. Um HTTP 301 por rota continua dependendo de infraestrutura que o GitHub Pages não oferece nativamente. Nenhuma alteração de DNS foi realizada.

A tag UET e o evento de clique no WhatsApp foram preservados. Não foi criada conversão de contato por visualização de página. O recebimento dos eventos e a configuração dos objetivos dentro da conta de anúncios não foram alterados nem certificados por esta auditoria do site.

## Documentos jurídicos

A consulta pública confirmou que /termos/ já mostrava a versão de 26/10/2026, com contratação direta, preços novos, horários novos e política de correções. Não foi necessário substituir seu conteúdo jurídico nesta atualização. A revisão abrangeu também a privacidade e o licenciamento já preparados na reformulação.

A geração comercial de voz e o licenciamento musical têm condições diferentes. As referências oficiais da ElevenLabs foram consultadas, sem conceder direitos além dos efetivamente contratados. A documentação permanece como minuta personalizada, sem afirmar revisão por advogado. A licença e o plano dos materiais efetivamente utilizados precisam ser comprovados por pedido.

Referências: https://elevenlabs.io/terms-of-use e https://elevenlabs.io/music-terms.

## Limitações e pendências

1. Substituir a amostra temporária de Produção Completa de Thiago quando o arquivo correto estiver disponível.
2. Melhorar e monitorar a estabilidade visual do catálogo mobile; última medição CLS 0,164.
3. A inspeção visual real ocorreu em 1363 × 936. Não foram simuladas manualmente as três resoluções exatas solicitadas, nem houve teste real em Safari/iPhone ou Android. Mobile foi avaliado por auditoria automatizada.
4. Foram feitas e inspecionadas capturas reais antes e depois de home, Off, Spot e catálogo, além do retrato publicado de Zozo. O ambiente de trabalho foi desconectado no fechamento, impedindo anexar esses arquivos nesta sessão.
5. Permanecem a validação jurídica profissional e as confirmações operacionais de licença e armazenamento de arquivos finais por 12 meses.

O estado publicado pode ser recuperado pelo histórico do repositório. A atualização final de interface corresponde ao commit 9b9edeedd3909d2b5f4f0a7584023a59091f6505.
