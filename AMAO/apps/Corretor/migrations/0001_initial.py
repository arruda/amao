# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RetornoCorrecao'
        db.create_table('Corretor_retornocorrecao', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('Corretor', ['RetornoCorrecao'])


    def backwards(self, orm):
        
        # Deleting model 'RetornoCorrecao'
        db.delete_table('Corretor_retornocorrecao')


    models = {
        'Corretor.retornocorrecao': {
            'Meta': {'object_name': 'RetornoCorrecao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['Corretor']
