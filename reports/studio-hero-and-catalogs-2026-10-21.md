# Visual dos topos, Home e Banco de Vozes

- Cinco landing pages: imagem de estúdio ao lado da comunicação comercial, com identificação específica do serviço e onda sonora decorativa estática. Em telas menores a imagem fica abaixo do texto, sem animações ou downloads adicionais de áudio.
- Home: comparativo removido; Off a partir de R$ 8,50 e produção a partir de R$ 19,00, sempre identificados como IA e com preço humano próximo. Textos e metadados focam o serviço. Dados estruturados incluem ambas as modalidades.
- Home e `/vozes/`: mesmo catálogo por abas das landing pages, humanas selecionadas inicialmente, IA na segunda aba, filtros e áudio sob demanda. O catálogo humano completo permanece disponível nessas duas páginas. Black Friday e páginas exclusivas IA não foram alteradas.
- Geração: `scripts/unified-catalog.py` preserva os novos catálogos em compilações e sincronizações futuras. A comunicação comercial da Home está protegida pelo mecanismo já utilizado nas landing pages.

## Imagem

Gerada pela ferramenta integrada imagegen e otimizada para WebP:
- `assets/images/voice-studio-480.webp`: 29.560 bytes.
- `assets/images/voice-studio-960.webp`: 90.284 bytes.

Prompt final: fotografia realista premium para o topo do site A Locução, com microfone condensador profissional em shock mount, filtro antipop e fones sobre mesa escura, console desfocado, painéis acústicos azul-marinho, luz lateral verde-petróleo e luz ambiente âmbar; composição quadrada, foco no microfone, profundidade de campo suave; sem pessoas, textos, logos ou marcas d’água. Uma única fotografia coerente para serviços de locução e produção.

## Verificação

Passaram: build completo; 5 testes de landing pages e catálogo completo; testes Black Friday, tracking, migração de vozes e calculadora; consistência SEO sem erros; teste de atribuição e diff-check. Imagem inspecionada diretamente. A validação visual dos layouts e a interação em navegador real continuam pendentes devido à indisponibilidade de Chromium neste ambiente. Não foi comprovada a reprodução da mídia remota por navegador.
