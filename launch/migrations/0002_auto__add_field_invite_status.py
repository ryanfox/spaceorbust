# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Invite.status'
        db.add_column('launch_invite', 'status',
                      self.gf('django.db.models.fields.CharField')(max_length=2, default='PN'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Invite.status'
        db.delete_column('launch_invite', 'status')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'launch.card': {
            'Meta': {'object_name': 'Card'},
            'hand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['launch.Hand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'suit': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'launch.game': {
            'Meta': {'object_name': 'Game'},
            'clocks': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'discardpile': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'discardpile'", 'to': "orm['launch.Hand']"}),
            'drawpile': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'drawpile'", 'to': "orm['launch.Hand']"}),
            'fuses': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ispublic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'launchpad': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'launchpad'", 'to': "orm['launch.Hand']"}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'turn': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'turn'", 'to': "orm['auth.User']"})
        },
        'launch.hand': {
            'Meta': {'object_name': 'Hand'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['launch.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']"})
        },
        'launch.invite': {
            'Meta': {'object_name': 'Invite'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['launch.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitee'", 'to': "orm['auth.User']"}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviter'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'PN'"})
        },
        'launch.note': {
            'Meta': {'object_name': 'Note'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['launch.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['launch']