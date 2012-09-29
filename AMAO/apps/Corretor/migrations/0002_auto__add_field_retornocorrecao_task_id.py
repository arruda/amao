# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RetornoCorrecao.task_id'
        db.add_column('Corretor_retornocorrecao', 'task_id', self.gf('django.db.models.fields.CharField')(max_length=350, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RetornoCorrecao.task_id'
        db.delete_column('Corretor_retornocorrecao', 'task_id')


    models = {
        'Corretor.retornocorrecao': {
            'Meta': {'object_name': 'RetornoCorrecao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['Corretor']
