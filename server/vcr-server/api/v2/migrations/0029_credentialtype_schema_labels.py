
from django.db import migrations, models
import django.contrib.postgres.fields.jsonb


class Migration(migrations.Migration):

    dependencies = [("api_v2", "0028_credentialtype_metadata")]

    operations = [
        migrations.AddField(
            model_name="credentialtype",
            name="schema_label",
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="credentialtype",
            name="schema_description",
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        )
    ]
