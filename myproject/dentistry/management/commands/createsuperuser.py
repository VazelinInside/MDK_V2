from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Create a superuser with a password non-interactively'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        database = options.get('database')
        password = options.get('password')
        email = options.get('email')
        firstname = options.get('first_name')
        lastname = options.get('last_name')
        patronymic = options.get('patronymic')

        if not password or not email or not firstname or not lastname:
            raise CommandError(
                "--email, --password, --firstname and --lastname are required options")

        user_data = {
            'password': password,
            'email': email,
            'first_name': firstname,
            'last_name': lastname,
            'patronymic': patronymic,
        }

        self.UserModel._default_manager.db_manager(
            database).create_superuser(**user_data)

        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Superuser created successfully.")