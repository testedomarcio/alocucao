# Reformulação A Locução — 26/10/2026

## Resultado implementado

- Nova apresentação visual em verde profundo, tons claros e tipografia editorial, com adaptação por largura de tela, foco visível e navegação por teclado.
- Home, serviços, preços, contato, sobre, calculadora e páginas comerciais principais reformulados.
- 27 perfis individuais a partir dos arquivos editoriais fornecidos. E-mails publicados conforme confirmação do responsável e regra de nome sem espaços, acentos ou pontuação.
- Banco com pesquisa por nome/aplicação e filtros por perfil e estilo. Nenhum filtro ou promessa de idiomas.
- 39 MP3 importados: 20 Off e 19 Produção Completa. Reprodução no domínio próprio, sem links públicos do Drive e sem autoplay. Ao iniciar uma demonstração, as outras pausam.
- “Leo Antonio” nos arquivos foi associado a “Leão Antonio” após confirmação expressa do responsável nesta sessão. Mantido nome profissional Leão Antonio e e-mail leaoantonio@alocucao.com.br.
- Retratos ilustrativos novos para Diego, Paulo Becker e Peter, gerados pela ferramenta de imagens integrada. Prompts: homens fictícios com características distintas correspondentes aos perfis, camisa azul-marinho, fundo azul-cinza, retrato de estúdio, sem texto ou marcas. Arquivos finais em assets/vozes-ia/images/diego.webp, paulo-becker.webp e peter.webp.
- Off R$ 12,00 e Produção Completa R$ 25,00 por peça comercial de até 40 segundos. Trabalhos especiais e narrativos sob orçamento.
- Todos os links de contratação pelo WhatsApp +55 27 99652-9832; mensagens dos perfis identificam a voz.
- Atendimento: segunda a sexta, 08h–18h, e sábado, 08h–12h, Brasília. Nenhum horário regular publicado para domingos/feriados.
- Termos, Privacidade e Licenciamento atualizados, incluindo transparência sobre vozes sintéticas, política de correções e armazenamento dos arquivos finais por 12 meses.
- Removidos da navegação e das páginas geradas cadastro, acesso, compra de créditos e dependências do catálogo do fornecedor.
- Gerador único substitui a cadeia de geradores comerciais antigos. Automação periódica de sincronização do fornecedor desativada. Publicação automática do blog pausada para impedir a reintrodução de regras antigas; conteúdo editorial existente preservado.

## URLs e SEO

O inventário anterior registra 419 documentos HTML analisáveis, incluindo modelos. A nova saída contém 444 páginas completas e 90 URLs no sitemap. Os caminhos públicos anteriores foram preservados. Os 332 perfis antigos já possuíam noindex; os endereços seguem acessíveis e direcionam o visitante, por link, ao catálogo atual, sem atribuir esses profissionais à nova operação.

As páginas de serviços existentes mantêm URLs, conteúdo relevante atualizado e canonical próprio. A rota /locutores/ mantém indexação e apresenta o diretório dos novos perfis. O índice de guias e seis tutoriais úteis tiveram conteúdo reescrito para a contratação atual: preparação de roteiro, escolha da voz, solicitação de Off, produção completa, correção e recebimento de áudio. As páginas exclusivamente relacionadas a cadastro, acompanhamento do sistema antigo e indicação deixaram de ser indexáveis, mas conservam os endereços com acesso ao atendimento atual. Aliases equivalentes foram mantidos com canonical para a página principal e noindex, sem redirecionamento HTML. Não houve alteração de DNS ou de campanhas publicitárias.

**Limitação de infraestrutura:** GitHub Pages não permite configurar 301 por rota. Nenhum HTTP 301 foi inventado ou anunciado como realizado. Um 301 real para aliases exige camada adicional de servidor/proxy; isso fica pendente, sem alterações de DNS nesta entrega.

O estado original pode ser recuperado pelo commit fb45f9aeae2e80d624b7bb7c7f6b6786778b1ce4. O inventário técnico anterior está em auditoria-antes.json; a lista das saídas está em manifesto.json.

## Validação concluída

- Geração das páginas pelo novo build.
- Verificação de todas as páginas geradas: um H1 por página, canonical, links locais e âncoras, arquivos de imagem/áudio/JS/CSS, telefone de contratação, retirada de textos comerciais antigos e correspondência do sitemap.
- 39 arquivos MP3 analisados com ffprobe: codec e duração válidos. Durações entre aproximadamente 19 e 47 segundos. Arquivos preservados sem recompressão, entre cerca de 320 e 700 KB, preload=none. Nenhum arquivo foi trocado para completar um perfil.
- Testes de JavaScript: busca sem depender de acentos; combinação de gênero/estilo; resultado vazio; limpeza de filtros; pausa de players concorrentes; consentimento aceito/negado/revogado; carregamento único das tags; um evento de WhatsApp por clique; identificação da voz, da página e da origem de campanha.
- Sintaxe de scripts JS e Python verificada.

**Limitações da verificação:** não foi possível renderizar a prévia local no navegador desta sessão; o endereço de prévia respondeu com exigência de autenticação do ambiente. A adaptação mobile foi implementada e inspecionada em código, mas não houve verificação visual em viewport móvel. ffprobe verifica integridade técnica, não equivale a escuta humana de cada demonstração. Core Web Vitals de usuários reais e recebimento de conversões na conta publicitária dependem da publicação, consentimento e dados posteriores. Não se afirma conversão real de venda nem desempenho garantido.

## Pendências de materiais

| Perfil | Arquivos ausentes na pasta fornecida |
|---|---|
| Aida | Off e Produção Completa |
| Aline Mota | Produção Completa |
| Eduardo S. | Off e Produção Completa |
| Enzo | Off e Produção Completa |
| Fernanda | Off e Produção Completa |
| Marcio | Off e Produção Completa |
| Peter | Off e Produção Completa |
| Thiago | Off e Produção Completa |

Os perfis foram criados; os players ausentes não são exibidos. Não foram reaproveitados áudios do catálogo anterior como se fossem as novas demonstrações. Os materiais editoriais sugerem transcrições, mas não foram fornecidas transcrições dos áudios; esse recurso não foi inventado.

## Pendências jurídicas e operacionais

Os documentos são minutas personalizadas, sem declaração de revisão por advogado. Recomenda-se validação jurídica profissional e confirmação operacional da cadeia de licenças por pedido. A licença de geração de voz não equivale à licença musical. Os termos oficiais da ElevenLabs consultados, atualizados em 09/10/2026, diferenciam uso comercial e planos/modelos de música; rádio, TV e cinema exigem verificação específica. Não se promete licença irrestrita sobre trilhas de planos comuns.

Fontes consultadas: https://elevenlabs.io/terms-of-use ; https://elevenlabs.io/music-terms ; CDC, Decreto 7.962/2013 e LGPD no Portal Planalto. É necessário conservar evidências do plano e da licença dos materiais efetivamente usados, e conferir as bases e garantias das transferências internacionais dos fornecedores. O site estático publica a política de armazenamento por 12 meses, mas a retenção real dos pedidos deve ser cumprida na operação de produção e entrega; o site não implementa armazenamento de pedidos.
