#!/usr/bin/env python3
import runpy, unittest
M=runpy.run_path('scripts/sync-voices.py')
class MigrationTest(unittest.TestCase):
    def payload(self,status='10 a 30 minutos'):
        import json
        rows=[dict(id=i,nome=f'Voz {i}',sexo='feminino',display=status,estado='São Paulo',estilos='Padrão - Impacto - Varejo',avatar_url=f'midia.php?file={i}.jpg',demo_url=f'download-audio.php?id={i}&v=2') for i in range(1,41)]
        return 'const locutoresData = '+json.dumps(rows)+';'

    def test_real_fields_and_origins(self):
        voices=M['parse_catalog'](self.payload())
        self.assertEqual(len(voices),40);self.assertEqual(voices[0]['region'],'São Paulo')
        self.assertEqual(voices[0]['statusLabel'],'10 a 30 minutos');self.assertEqual(voices[0]['type'],'Feminina')
        self.assertIn('&v=2',voices[0]['audio']);self.assertNotIn('profile',voices[0])
    def test_status_semantics(self):
        for label,expected in [('Online (1-5 horas)','recording_online'),('30 min a 1 hora','recording_online'),('1 a 2 horas','recording_online'),('Offline','offline'),('Indisponível','unavailable'),('Locutor(a) Volta hoje às 13:00','returning'),('Novo status','unknown')]:
            v=M['parse_catalog'](self.payload(label))[0]
            self.assertEqual(v['status'],expected);self.assertEqual(v['statusLabel'],label)
    def test_invalid_catalogs_rejected(self):
        for payload in ['',self.payload().replace('"id": 2,','"id": 1,'),self.payload().replace('download-audio.php?id=1','https://example.com/demo.mp3?id=1'),self.payload().replace('demo_url','invalid_demo')]:
            with self.assertRaises(ValueError):M['parse_catalog'](payload)
if __name__=='__main__':unittest.main()
