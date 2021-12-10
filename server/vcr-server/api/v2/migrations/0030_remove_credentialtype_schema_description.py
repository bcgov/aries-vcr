from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api_v2", "0029_credentialtype_schema_labels")]

    operations = [
        migrations.RemoveField(
            model_name="credentialtype",
            name="schema_description",
        )
    ]