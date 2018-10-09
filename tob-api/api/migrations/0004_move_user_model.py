from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181005_2140'),
    ]

    database_operations = [
        migrations.AlterModelTable('User', 'user')
    ]

    state_operations = [
        migrations.DeleteModel('User')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
    