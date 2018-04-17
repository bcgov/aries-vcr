import os
from django.core import management
from django.core.management.commands import migrate
from django.contrib.auth.models import User
from django.db.models import Q

class Command(migrate.Command):
    """
    Overrides django's default migrate command in order to update initialize user accounts.
    """
    def handle(self, *args, **options):
      self.stdout.write("")
      self.stdout.write("Migrating database ...")
      super(Command, self).handle(*args, **options)

      self.__initialize_user_accounts()

    def __initialize_user_accounts(self):
      self.stdout.write("\nInitializing user accounts ...")
      self.__initialize_superuser()
      self.__initialize_user()

    def __initialize_user(self):
      WALLET_USER_ID = os.environ.get('WALLET_USER_ID')
      WALLET_USER_PASSWORD = os.environ.get('WALLET_USER_PASSWORD')
      
      if WALLET_USER_ID and WALLET_USER_PASSWORD:
        if User.objects.filter(Q(is_superuser=False)).count() <= 0:
          self.stdout.write("Initializing API user account ...")
          User.objects.filter(username=WALLET_USER_ID).exists() or User.objects.create_user(username=WALLET_USER_ID, password=WALLET_USER_PASSWORD)
        else:
          self.stdout.write("An API user account already exists.")
      else:
        self.stdout.write("Either or both of WALLET_USER_ID and WALLET_USER_PASSWORD where not specified.\n"
                          "Clients may not be able to authenticate with the wallet api as a result.")

    def __initialize_superuser(self):
      WALLET_ADMIN_USER_ID = os.environ.get('WALLET_ADMIN_USER_ID', 'wall-e-admin')
      WALLET_ADMIN_PASSWORD = os.environ.get('WALLET_ADMIN_PASSWORD')
      
      if WALLET_ADMIN_USER_ID and WALLET_ADMIN_PASSWORD:
        if User.objects.filter(Q(is_superuser=True)).count() <= 0:
          self.stdout.write("Initializing superuser account ...")
          User.objects.filter(username=WALLET_ADMIN_USER_ID).exists() or User.objects.create_superuser(WALLET_ADMIN_USER_ID, 'do-not-reply@nowhere.com', WALLET_ADMIN_PASSWORD)
        else:
          self.stdout.write("A superuser account already exists.")
      else:
        self.stdout.write("Either or both of WALLET_ADMIN_USER_ID and WALLET_ADMIN_PASSWORD where not specified.\n"
                          "Clients may not be able to authenticate with the wallet api as a result.")