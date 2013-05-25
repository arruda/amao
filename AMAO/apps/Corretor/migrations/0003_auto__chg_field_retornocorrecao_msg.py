# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RetornoCorrecao.msg'
        db.alter_column('Corretor_retornocorrecao', 'msg', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'RetornoCorrecao.msg'
        db.alter_column('Corretor_retornocorrecao', 'msg', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

    models = {
        'Corretor.retornocorrecao': {
            'Meta': {'object_name': 'RetornoCorrecao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['Corretor']