# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'QuestaoDeAvaliacao.retorno_correcao'
        db.alter_column('Questao_questaodeavaliacao', 'retorno_correcao_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Corretor.RetornoCorrecao'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Questao.retorno_correcao'
        db.alter_column('Questao_questao', 'retorno_correcao_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Corretor.RetornoCorrecao'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):

        # Changing field 'QuestaoDeAvaliacao.retorno_correcao'
        db.alter_column('Questao_questaodeavaliacao', 'retorno_correcao_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Corretor.RetornoCorrecao'], null=True))

        # Changing field 'Questao.retorno_correcao'
        db.alter_column('Questao_questao', 'retorno_correcao_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Corretor.RetornoCorrecao'], null=True))

    models = {
        'Aluno.aluno': {
            'Meta': {'object_name': 'Aluno'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'Avaliacao.avaliacao': {
            'Meta': {'object_name': 'Avaliacao'},
            'aluno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'avaliacoes'", 'to': "orm['Aluno.Aluno']"}),
            'ativa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            'data_termino': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'simulado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'templateAvaliacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'avaliacoes'", 'to': "orm['Avaliacao.TemplateAvaliacao']"}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'Avaliacao.templateavaliacao': {
            'Meta': {'object_name': 'TemplateAvaliacao'},
            'ativa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'templateAvaliacoes_autor'", 'null': 'True', 'to': "orm['auth.User']"}),
            'data_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            'data_termino': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permite_simulado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'turma': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'templateAvaliacoes'", 'to': "orm['Turma.Turma']"})
        },
        'Corretor.retornocorrecao': {
            'Meta': {'object_name': 'RetornoCorrecao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'Materia.materia': {
            'Meta': {'object_name': 'Materia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'Professor.professor': {
            'Meta': {'object_name': 'Professor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'Questao.entradagabarito': {
            'Meta': {'object_name': 'EntradaGabarito'},
            'arquivo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entradasGabarito'", 'to': "orm['Questao.Questao']"})
        },
        'Questao.filtroquestao': {
            'Meta': {'object_name': 'FiltroQuestao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notaBase': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'notaLimMaximo': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'notaLimMinimo': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'questaoExata': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filtrosQuestoes'", 'null': 'True', 'to': "orm['Questao.Questao']"}),
            'templateAvaliacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filtrosQuestoes'", 'to': "orm['Avaliacao.TemplateAvaliacao']"}),
            'tipo': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'filtrosQuestoes'", 'symmetrical': 'False', 'to': "orm['Questao.TipoQuestao']"})
        },
        'Questao.fonte': {
            'Meta': {'object_name': 'Fonte'},
            'arquivo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fontes'", 'to': "orm['Questao.QuestaoDeAvaliacao']"})
        },
        'Questao.fontegabarito': {
            'Meta': {'object_name': 'FonteGabarito'},
            'arquivo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fontesGabarito'", 'to': "orm['Questao.Questao']"}),
            'usarNaResolucao': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Questao.opcaomultiplaescolha': {
            'Meta': {'object_name': 'OpcaoMultiplaEscolha'},
            'anular': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'correta': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opcao': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'multiplaEscolhas'", 'to': "orm['Questao.Questao']"})
        },
        'Questao.questao': {
            'Meta': {'object_name': 'Questao'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questoes_autor'", 'null': 'True', 'to': "orm['auth.User']"}),
            'enunciado': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_corretor': ('django.db.models.fields.SmallIntegerField', [], {}),
            'percentNotaDiscursiva': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'percentNotaMultipla': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'percentNotaProgramacao': ('django.db.models.fields.DecimalField', [], {'default': "'100'", 'max_digits': '10', 'decimal_places': '2'}),
            'respostaDiscursiva': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'retorno_correcao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Corretor.RetornoCorrecao']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'questoes'", 'symmetrical': 'False', 'to': "orm['Questao.TipoQuestao']"}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'verificada': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Questao.questaodeavaliacao': {
            'Meta': {'object_name': 'QuestaoDeAvaliacao'},
            'avaliacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questoes'", 'to': "orm['Avaliacao.Avaliacao']"}),
            'filtro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questoesGeradas'", 'to': "orm['Questao.FiltroQuestao']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '10', 'decimal_places': '2'}),
            'opcoesMultiplaEscolha': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'respostasMultiplaEscolha'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['Questao.OpcaoMultiplaEscolha']"}),
            'perc_disc': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '10', 'decimal_places': '2'}),
            'perc_mult': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '10', 'decimal_places': '2'}),
            'perc_prog': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '10', 'decimal_places': '2'}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'avaliacoes'", 'to': "orm['Questao.Questao']"}),
            'respostaDiscursiva': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'retorno_correcao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Corretor.RetornoCorrecao']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'revisao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'Questao.tipoquestao': {
            'Meta': {'object_name': 'TipoQuestao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tipoPai': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tipoFilhos'", 'null': 'True', 'to': "orm['Questao.TipoQuestao']"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'Turma.turma': {
            'Meta': {'object_name': 'Turma'},
            'alunos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'turmas'", 'symmetrical': 'False', 'to': "orm['Aluno.Aluno']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'turmas'", 'to': "orm['Materia.Materia']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'turmas'", 'to': "orm['Professor.Professor']"}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Questao']