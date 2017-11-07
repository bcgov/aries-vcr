from django.core import management
from django.core.management.commands import migrate

class Command(migrate.Command):
    """
    Overrides django's default migrate command in order to update the solr index following migration.
    """

    def handle(self, *args, **options):
      self.stdout.write("")
      self.stdout.write("Migrating database ...")
      super(Command, self).handle(*args, **options)

      self.stdout.write("")
      self.stdout.write("Updating search indexes ...")
      management.call_command('update_index')