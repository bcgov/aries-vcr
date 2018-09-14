import os
from django.core import management
from django.core.management.commands import migrate
from django.db.models import Q

# Get our customized User
from django.contrib.auth import get_user_model
User = get_user_model()

from api_v2.suggest import SuggestManager

class Command(migrate.Command):
    """
    Overrides django's default migrate command in order to update the solr index, and initialize user accounts following migration.
    """

    def handle(self, *args, **options):
      self.stdout.write("")
      self.stdout.write("Migrating database ...")
      super(Command, self).handle(*args, **options)

      self.__update_search_indexes()
      self.__initialize_user_accounts()

    def __update_search_indexes(self):
      SKIP_INDEXING = os.environ.get('SKIP_INDEXING_ON_STARTUP', 'false')
      if not SKIP_INDEXING or SKIP_INDEXING.lower() == 'false':
        self.stdout.write("\nUpdating search indexes ...")
        batch_size = os.getenv("SOLR_BATCH_SIZE", 500)
        management.call_command("update_index", "--max-retries=5", "--batch-size={}".format(batch_size))
      elif SKIP_INDEXING == 'active':
        self.stdout.write("\nSearch indexing in progress ...")
      else:
        self.stdout.write("\nSkipping search indexing ...")
      SuggestManager().rebuild()

    def __initialize_user_accounts(self):
      self.stdout.write("\nInitializing user accounts ...")
      self.__initialize_superuser()
      self.__initialize_user()

    def __initialize_user(self):
      USER_ID = os.environ.get('USER_ID')
      USER_PASSWORD = os.environ.get('USER_PASSWORD')

      # ToDo - Generate these automatically.
      # Refer to ...\theorgbook\tob-api\env\lib\site-packages\von_agent\wallet.py
      # for information on how to get a did and verkey from a seed.
      # For now we're not using did auth for these api accounts, so it's not critical.
      # We just need these variables to create the account.
      USER_SEED = os.environ.get('USER_SEED', 'tob_api_user_0000000000000000000')
      USER_DID = os.environ.get('USER_DID', 'TQDrf89hBWzcCiLu4FLP91')
      USER_VERKEY = os.environ.get('USER_VERKEY', 'FPZwF913VqgMfXyKxdquR4i9GmSUqCnUd9RJVQAjFhRj')

      if USER_ID and USER_PASSWORD:
        if User.objects.filter(Q(is_superuser=False)).count() <= 0:
          self.stdout.write("Initializing API user account ...")
          User.objects.filter(username=USER_ID).exists() or User.objects.create_user(username=USER_ID, password=USER_PASSWORD, DID=USER_DID, verkey=USER_VERKEY.encode())
        else:
          self.stdout.write("An API user account already exists.")
      else:
        self.stdout.write("Either or both of USER_ID and USER_PASSWORD where not specified.\n"
                          "Clients may not be able to authenticate with the api as a result.")

    def __initialize_superuser(self):
      ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID', 'api-admin')
      ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

      if ADMIN_USER_ID and ADMIN_PASSWORD:
        if User.objects.filter(Q(is_superuser=True)).count() <= 0:
          self.stdout.write("Initializing superuser account ...")
          User.objects.filter(username=ADMIN_USER_ID).exists() or User.objects.create_superuser(ADMIN_USER_ID, 'do-not-reply@toanywhere.com', ADMIN_PASSWORD)
        else:
          self.stdout.write("A superuser account already exists.")
      else:
        self.stdout.write("Either or both of ADMIN_USER_ID and ADMIN_PASSWORD where not specified.\n"
                          "Clients may not be able to authenticate with the api as a result.")
