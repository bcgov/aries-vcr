from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api_v2", "0030_remove_credentialtype_schema_description")]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "like",
                    models.BooleanField(null=True),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("ip", models.GenericIPAddressField(null=True))
            ],
            options={"db_table": "feedback"},
        )
    ]
