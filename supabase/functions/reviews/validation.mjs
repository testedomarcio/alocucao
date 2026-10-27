export function text(value,min,max){
 if(typeof value!=='string')throw Error('Campo inválido.');
 const clean=value.trim();if(clean.length<min||clean.length>max||/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/u.test(clean))throw Error(`Informe entre ${min} e ${max} caracteres.`);return clean;
}
export function slug(value){if(typeof value!=='string'||! /^[a-z0-9-]{1,80}$/.test(value))throw Error('Locutor inválido.');return value;}
export function token(value){if(typeof value!=='string'||! /^[a-f0-9]{64}$/.test(value))throw Error('Convite inválido.');return value;}
export function review(data){
 if(data.consent!==true)throw Error('É necessário autorizar a publicação.');
 if(!Number.isInteger(data.rating)||data.rating<1||data.rating>5)throw Error('Selecione de 1 a 5 estrelas.');
 return {voice:slug(data.voice),token:token(data.token),name:text(data.name,2,80),rating:data.rating,comment:text(data.comment,20,2000)};
}
// Read dimensions before decoding to block decompression bombs and reject SVG/other formats.
export function imageInfo(b){
 if(b.length<24||b.length>2097152)throw Error('Imagem inválida ou maior que 2 MB.');
 const d=new DataView(b.buffer,b.byteOffset,b.byteLength);let width=0,height=0,format='';
 if(b[0]===137&&b[1]===80&&b[2]===78&&b[3]===71&&b[4]===13&&b[5]===10&&b[6]===26&&b[7]===10){format='png';width=d.getUint32(16);height=d.getUint32(20);}
 else if(b[0]===255&&b[1]===216){format='jpeg';let i=2;while(i+9<b.length){if(b[i]!==255)break;const marker=b[i+1];if(marker===255){i++;continue;}const size=d.getUint16(i+2);if(size<2||i+2+size>b.length)break;if([192,193,194].includes(marker)){height=d.getUint16(i+5);width=d.getUint16(i+7);break;}i+=2+size;}}
 else if(String.fromCharCode(...b.slice(0,4))==='RIFF'&&String.fromCharCode(...b.slice(8,12))==='WEBP'){
  format='webp';const type=String.fromCharCode(...b.slice(12,16));
  if(type==='VP8X'&&b.length>=30){if(b[20]&2)throw Error('Envie uma imagem estática.');width=1+b[24]+(b[25]<<8)+(b[26]<<16);height=1+b[27]+(b[28]<<8)+(b[29]<<16);}
  else if(type==='VP8 '&&b.length>=30&&b[23]===157&&b[24]===1&&b[25]===42){width=d.getUint16(26,true)&16383;height=d.getUint16(28,true)&16383;}
  else if(type==='VP8L'&&b.length>=25&&b[20]===47){width=1+((b[21]|b[22]<<8)&16383);height=1+((b[22]>>6|b[23]<<2|b[24]<<10)&16383);}
 }
 if(!format||width<1||height<1||width>4000||height>4000||width*height>12000000)throw Error('Envie JPG, PNG ou WebP estático de até 4000 × 4000 pixels (12 megapixels).');
 return {format,width,height};
}
