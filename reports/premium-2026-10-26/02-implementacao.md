# Implementação e validação

O site mantém sua identidade visual e estrutura de hospedagem. A ampliação usa o gerador único existente, com catálogo central em `data/premium-services.json` e renderização em `scripts/premium_pages.py`.

Foram implementados: menu Início/Serviços/Banco de Vozes/Calculadora/Sobre Nós/Contato; quatro categorias na home e em Serviços; catálogo de preços ampliado; calculadora na home e em sua URL; mensagens de WhatsApp por serviço; páginas com escopo, limites, aplicações, briefing, FAQ e links complementares; dados estruturados Service correspondentes ao conteúdo visível. Os players permanecem sem autoplay e com carregamento sob demanda.

| URL | Oferta |
| --- | --- |
| /narracao-para-videos/ | A partir de R$ 25 por até 1 min |
| /narracoes/ | Narração longa a partir de R$ 75 por até 5 min |
| /gravacao-de-ura/ | R$ 20 por mensagem de até 30 s; cinco por R$ 75 |
| /tratamento-de-audio/ | A partir de R$ 25 por arquivo de até 5 min, sujeito à avaliação |
| /narracao-de-audiobooks/ | Sob orçamento, com direitos autorizados |
| /producao-de-podcasts/ | Sob orçamento por escopo |
| /dublagem-de-videos/ | Avaliação técnica e de licença; sem garantia de preservar a voz |

As páginas antigas de institucional e telefonia foram preservadas e ganharam links para os novos escopos. A tabela comercial nessas páginas foi explicitamente diferenciada dos novos serviços.

## Evidências de testes

`npm run build` e `npm test`: validação de H1, links e recursos locais, anchors, canonicals, sitemap, scripts duplicados, ausência de fluxos antigos, identificação de vozes, trabalhos recentes, consentimento e medição. Testes dinâmicos verificam pesquisa com acentos, filtros combinados, estado vazio, pausa de outros players e exibição aleatória sem perda ou duplicação de vozes.

Teste específico da calculadora: 1, 100, 101, 200, 201, 300 e 301 palavras; seleção de serviço; texto vazio; mensagem de WhatsApp sem o roteiro privado. Em 100 palavras: 40 segundos e R$ 12/R$ 25. Em 101: 41 segundos e R$ 24/R$ 50. Em 201: 81 segundos e R$ 36/R$ 75. A cobrança por faixas foi preservada, sem inventar regra por caracteres.

O navegador foi usado para conferir home, URA, calculadora e um perfil com áudio. As capturas estão na pasta `capturas/` do pacote de entrega. A avaliação estreita usa um frame de 390 px: confere o layout responsivo, sem equivaler a teste físico em Android/iOS. Os detalhes finais de reprodução e logs estão registrados em `qa-browser.json`.

Verificações locais não comprovam Core Web Vitals em campo, aprovação de anúncios, recebimento dos eventos na conta ou validade jurídica. Os testes de eventos confirmam a emissão no código; a configuração das metas e contagem deve ser conferida posteriormente na plataforma.

## Reversão

O estado anterior foi preservado por SHA e em cópia Git bundle local integral. Para desfazer, criar um commit revertendo a alteração premium sobre a versão mais recente da branch principal; testar e republicar pelo GitHub Pages. Não usar reset forçado sobre trabalho posterior. A referência anterior é `fb298b68546129020c24bd88d303417bbc567f22`. Configurações de DNS e campanhas não foram alteradas.
