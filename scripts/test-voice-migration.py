#!/usr/bin/env python3
"""Regression checks for a provider change, status semantics and public-field allowlisting."""
import copy,json,runpy,unittest
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('sync-voices.py')))
parse=M['parse_catalog']
class MigrationTest(unittest.TestCase):
    def payload(self):
        rows=[{'ID':i,'nome':f'Voz {i}','demo':f'demo-{i}.mp3','imagem':f'foto-{i}.jpg','filtro':'masculina','estado':'São Paulo','status_titulo':'Online','status_texto':'','estilos':'PADRÃO, VAREJO<br><b>Informações adicionais:</b><br>Textos Comerciais de até 02:00 minutos','demos':'','obs':'internal-only','ID_obs':123} for i in range(1,41)]
        return {'recordsTotal':40,'recordsFiltered':40,'data':rows}
    def test_public_fields_and_media_origin(self):
        voices=parse(self.payload());serialized=json.dumps(voices)
        self.assertNotIn('internal-only',serialized);self.assertNotIn('ID_obs',serialized)
        self.assertTrue(all(v['id'].startswith('lb-') for v in voices))
        self.assertTrue(all(v['audio'].startswith('https://hd.paineldegravacao.com.br/demos/') for v in voices))
        self.assertTrue(all(v['schedule']==[] for v in voices))
    def test_source_status_not_invented_delivery(self):
        data=self.payload();statuses=['10 min','30 min','Online','Offline','Volto já','Férias','Indisponível','Novo status']
        for row,status in zip(data['data'],statuses):row['status_titulo']=status
        voices=parse(data)
        self.assertEqual([v['status'] for v in voices[:8]],['recording_10min','recording_30min','recording_online','offline','returning','unavailable','unavailable','unknown'])
        self.assertEqual(voices[2]['statusLabel'],'Online')
    def test_missing_main_demo_uses_real_published_alternative(self):
        data=self.payload();data['data'][0]['demo']=None
        data['data'][0]['demos']=json.dumps({'padroes':{'padrao':{'estilo':'padrao','demo':'alternative.mp3'}}})
        self.assertTrue(parse(data)[0]['audio'].endswith('/alternative.mp3'))
    def test_partial_duplicate_and_unsafe_catalogs_are_rejected(self):
        for mutate in [lambda d:d.update(recordsTotal=41),lambda d:d['data'][1].update(ID=1),lambda d:d['data'][0].update(demo='../private.mp3')]:
            data=self.payload();mutate(data)
            with self.assertRaises(ValueError):parse(data)
if __name__=='__main__':unittest.main()
