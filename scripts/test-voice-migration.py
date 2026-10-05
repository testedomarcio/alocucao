#!/usr/bin/env python3
import runpy, unittest
M=runpy.run_path('scripts/sync-voices.py')
class MigrationTest(unittest.TestCase):
    def payload(self,status='10 a 30 minutos'):
        return '<table><tbody>'+''.join(f'''<tr><td data-label="Locutor"><span>feminino, {status}, Padrão - Impacto - Varejo, Gravação Comercial, SP</span><div class="locutor-name">Voz {i}</div><img class="avatar-img" src="perfil-img.php?file={i}.jpg&amp;sexo=feminino"></td><td data-locutor-id="{i}">{status}</td><td><audio src="download-audio.php?id={i}&amp;v=2"></audio></td></tr>''' for i in range(1,41))+'</tbody></table>'
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
        for payload in ['',self.payload().replace('data-locutor-id="2"','data-locutor-id="1"'),self.payload().replace('download-audio.php?id=1','https://example.com/demo.mp3?id=1'),self.payload().replace('<audio','<span')]:
            with self.assertRaises(ValueError):M['parse_catalog'](payload)
if __name__=='__main__':unittest.main()
