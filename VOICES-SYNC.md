# Banco de vozes

Fonte pública: https://vozlocutor.com.br/. O workflow sincroniza nomes, fotos, demos, estilos, região e status a cada 15 minutos e publica pelo GitHub Pages. O HTML é validado com BeautifulSoup; respostas incompletas, duplicadas, mídias fora do domínio e reduções superiores a 35% no mesmo fornecedor preservam o último catálogo válido.

A interface consulta o JSON local a cada 15 minutos quando visível. Status com mais de três horas passam para Disponibilidade sob consulta. Prazos recebem Gravando de; Offline, Indisponível e avisos de retorno preservam o texto original. O prazo final é confirmado pelo WhatsApp. Não são inferidos horários de gravação.

Perfis individuais foram retirados do sitemap e substituídos por redirecionamentos noindex para /vozes/. Nenhum gerador recria perfis. Nomes são texto, sem links para perfis do fornecedor. Fotos e áudios públicos são carregados da fonte; nenhuma classificação por estrelas é importada. Demos são carregadas ao reproduzir.
