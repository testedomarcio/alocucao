(() => {
  const container = document.getElementById("home-voice-grid");
  if (!container) return;

  // Only 4 champion voice demos (Impacto, Varejo, Institucional) for PageSpeed optimization
  const voices = [
    {name:"Marcelo Ferraz",type:"Masculina",region:"São Paulo",styles:["Impacto","Varejo","Institucional","Vídeo"],audio:"https://storageoffs.offsbrasil.com.br/uploadifive/masculino/MARCELO%20FERRAZ.mp3"},
    {name:"Elissandra",type:"Feminina",region:"Rio Grande do Norte",styles:["Institucional","Varejo","Impacto"],audio:"https://storageoffs.offsbrasil.com.br/uploadifive/masculino/ELISSANDRA.mp3"},
    {name:"Pablo Siqueira",type:"Masculina",region:"Goiás",styles:["Varejo","Impacto","Animada"],audio:"https://storageoffs.offsbrasil.com.br/uploadifive/masculino/PABLO%20SIQUEIRA.mp3"},
    {name:"Patricia Vieira",type:"Feminina",region:"Minas Gerais",styles:["Padrão","Institucional","Varejo"],audio:"https://storageoffs.offsbrasil.com.br/uploadifive/masculino/PATRICIA%20VIEIRA%20.mp3"}
  ];

  const schedules = {
    "Elissandra":{1:["06:00","20:00"],2:["06:00","22:15"],3:["06:00","20:00"],4:["06:30","20:30"],5:["06:30","20:00"]},
    "Patricia Vieira":{1:["07:00","20:00"],2:["07:00","20:00"],3:["07:00","20:00"],4:["06:00","20:00"],5:["07:00","20:00"]},
    "Kassia Renostro":{1:["08:00","17:00"],2:["08:00","17:00"],3:["08:00","17:00"],4:["08:00","17:00"],5:["08:00","17:00"]},
    "Lindy":{1:["08:30","12:00"],2:["08:30","12:00"],3:["08:30","12:00"],4:["08:30","12:00"],5:["08:30","12:00"]},
    "Absamira Santos":{1:["07:00","21:00"],2:["07:00","21:00"],3:["07:00","21:00"],4:["07:00","21:00"],5:["07:00","21:00"]},
    "Sunshine":{1:["07:00","20:00"],2:["07:00","20:00"],3:["07:00","20:00"],4:["07:00","20:00"],5:["07:00","20:00"]},
    "Zanhe Moura":{1:["08:00","11:00"],2:["08:00","11:00"],3:["08:00","11:00"],4:["08:00","11:00"],5:["08:00","11:00"]},
    "Patricia Souza":{1:["08:00","18:00"],2:["08:00","17:30"],3:["08:00","18:00"],4:["08:00","18:00"],5:["08:00","16:30"]},
    "Josi de Oliveira":{1:["07:00","19:00"],2:["07:00","19:00"],3:["07:00","19:00"],4:["07:00","19:00"],5:["07:00","19:00"]},
    "Janaina Hanauer":{1:["07:00","22:00"],2:["07:00","20:00"],3:["07:00","20:00"],4:["07:00","20:00"],5:["07:00","20:00"]},
    "Marcelo Ferraz":{1:["06:00","23:59"],2:["06:00","23:59"],3:["06:00","23:59"],4:["06:00","23:59"],5:["06:00","23:59"]},
    "Pablo Siqueira":{1:["07:00","21:00"],2:["07:00","21:00"],3:["07:00","21:00"],4:["07:00","21:00"],5:["07:00","21:00"]},
    "Marcio":{1:["07:00","18:00"],2:["07:15","17:00"],3:["07:00","21:00"],4:["07:00","21:00"]},
    "Anderson Henrique":{1:["07:00","19:00"],2:["07:00","19:00"],3:["07:00","19:00"],4:["07:00","19:00"],5:["07:00","19:00"]},
    "Tito":{1:["08:00","17:00"],2:["08:00","17:30"],3:["08:00","17:00"],4:["08:00","17:00"],5:["08:00","17:00"]},
    "Flávio":{1:["07:00","20:00"],2:["07:00","20:00"],3:["07:00","20:00"],4:["07:00","20:00"],5:["07:00","18:00"]},
    "Alan Fernandes":{1:["09:00","18:00"],2:["08:00","21:00"],3:["08:00","21:00"],4:["08:00","21:00"],5:["08:00","21:00"]},
    "Vinicius Silveira":{1:["06:30","21:00"],2:["06:30","21:00"],3:["06:30","21:00"],4:["06:30","21:00"],5:["06:30","21:00"]},
    "Charles Helfer":{1:["06:30","21:00"],2:["06:30","21:00"],3:["06:30","21:00"],4:["06:30","21:00"],5:["06:30","21:00"]},
    "Douglas Camargo":{1:["06:30","23:59"],2:["07:00","23:59"],3:["07:00","23:59"],4:["07:00","23:59"],5:["07:00","23:00"]}
  };

  const brasiliaNow = () => {
    const parts = new Intl.DateTimeFormat("en-GB", {timeZone:"America/Sao_Paulo",weekday:"short",hour:"2-digit",minute:"2-digit",hourCycle:"h23"}).formatToParts(new Date());
    const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
    const days = {Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6,Sun:0};
    return {day:days[values.weekday],minutes:Number(values.hour) * 60 + Number(values.minute)};
  };
  const toMinutes = value => { const [hour, minute] = value.split(":").map(Number); return hour * 60 + minute; };
  const availableNow = name => {
    const now = brasiliaNow(), slot = schedules[name]?.[now.day];
    return Boolean(slot && now.minutes >= toMinutes(slot[0]) && now.minutes <= toMinutes(slot[1]));
  };
  const todaySchedule = name => schedules[name]?.[brasiliaNow().day];
  const shortTime = value => value.replace(":00", "h").replace(":", "h");
  const normalize = value => value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  const render = () => {
    container.innerHTML = voices.map(voice => {
      const slot = todaySchedule(voice.name);
      const schedule = slot ? `Hoje: ${shortTime(slot[0])}–${shortTime(slot[1])}` : "Agenda de hoje sob consulta";
      const badge = availableNow(voice.name) ? '<span class="home-availability">Disponível hoje</span>' : '<span class="home-availability off">Fora da agenda agora</span>';
      const message = encodeURIComponent(`Olá! Ouvi a voz de ${voice.name} no site da A Locução e gostaria de usá-la no meu projeto. Pode confirmar a disponibilidade e me orientar?`);
      return `<article class="voice-sample" data-name="${voice.name}">
        <div class="voice-sample-head"><div><strong>${voice.name}</strong><small>Voz ${voice.type.toLowerCase()}</small></div>${badge}</div>
        <div class="home-voice-tags">${voice.styles.slice(0,4).map(style => `<span>${style}</span>`).join("")}</div>
        <p class="home-voice-region">${voice.region}</p>
        <p class="home-voice-schedule">${schedule} · horário habitual</p>
        <audio controls preload="none" data-voice="${voice.name}" aria-label="Demonstração da voz de ${voice.name}"><source src="${voice.audio}" type="audio/mpeg"></audio>
        <a class="home-voice-choice" data-cta="home_voz_${normalize(voice.name).replace(/\s+/g,"_")}" href="https://wa.me/5527996529832?text=${message}" target="_blank" rel="noopener">Quero esta voz</a>
      </article>`;
    }).join("");
  };

  render();
})();
