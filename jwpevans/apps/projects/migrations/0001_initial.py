# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pun'
        db.create_table(u'projects_pun', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('pun_target', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'projects', ['Pun'])

    def backwards(self, orm):
        # Deleting model 'Pun'
        db.delete_table(u'projects_pun')

    models = {
        u'projects.pun': {
            'Meta': {'object_name': 'Pun'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pun_target': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['projects']