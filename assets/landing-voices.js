(() => {
  const containers = document.querySelectorAll("[data-landing-voices]");
  if (!containers.length) return;
  const voices = [
    {name:"Elissandra",type:"feminina",region:"Rio Grande do Norte",styles:["Padrão","Impacto","Animada","Varejo"],audio:"https://storageoffs.offsbrasil.com.br/uploadifive/masculino/ELISSANDRA.mp3",schedule:{1:["06:00","20:00"],2:["06:00","22:15"],3:["06:00","20:00"],4:["06:30","20:30"],5:["06:30","20:00"]}},
    {name:"Marcelo Ferraz",type:"masculina",region:"São Paulo",styles:["Padrão","Impacto","Animada","Varejo"],audio:"https://storageoffs.offsbrasil.com.br/uploadifive/masculino/MARCELO%20FERRAZ.mp3",schedule:{1:["06:00","23:59"],2:["06:00","23:59"],3:["06:00","23:59"],4:["06:00","23:59"],5:["06:00","23:59"]}}
  ];
  const now = () => {
    const parts = new Intl.DateTimeFormat("en-GB",{timeZone:"America/Sao_Paulo",weekday:"short",hour:"2-digit",minute:"2-digit",hourCycle:"h23"}).formatToParts(new Date());
    const values = Object.fromEntries(parts.map(part => [part.type,part.value]));
    const days = {Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6,Sun:0};
    return {day:days[values.weekday],minutes:Number(values.hour)*60+Number(values.minute)};
  };
  const minutes = value => { const [hour,minute] = value.split(":").map(Number); return hour*60+minute; };
  const short = value => value.replace(":00","h").replace(":","h");
  const normalize = value => value.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
  const card = voice => {
    const current = now(), slot = voice.schedule[current.day];
    const available = Boolean(slot && current.minutes >= minutes(slot[0]) && current.minutes <= minutes(slot[1]));
    const status = available ? '<span class="landing-voice-status">Disponível hoje</span>' : '<span class="landing-voice-status off">Fora da agenda agora</span>';
    const schedule = slot ? `Hoje: ${short(slot[0])}–${short(slot[1])} · horário habitual` : "Agenda de hoje sob consulta";
    const message = encodeURIComponent(`Olá! Ouvi a voz de ${voice.name} no site da A Locução e gostaria de usá-la no meu projeto. Pode confirmar a disponibilidade?`);
    return `<article class="landing-voice"><div class="landing-voice-head"><div><strong>${voice.name}</strong><small>Voz ${voice.type} · ${voice.region}</small></div>${status}</div><div class="landing-voice-tags">${voice.styles.map(style=>`<span>${style}</span>`).join("")}</div><p class="landing-voice-meta">${schedule}</p><audio controls preload="none" data-voice="${voice.name}" aria-label="Demonstração da voz de ${voice.name}"><source src="${voice.audio}" type="audio/mpeg"></audio><div class="landing-voice-actions"><a class="landing-voice-pick" data-cta="landing_voz_${normalize(voice.name).replace(/\s+/g,"_")}" href="https://wa.me/5527996529832?text=${message}" target="_blank" rel="noopener">Quero esta voz</a><a class="landing-voice-more" href="/vozes/">Ouvir mais vozes</a></div></article>`;
  };
  containers.forEach(container => container.innerHTML = voices.map(card).join(""));
})();
