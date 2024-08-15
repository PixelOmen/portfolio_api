from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = 'Converts a .env file to docker-compose environment strings'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str,
                            help='The path to the file to read')
        parser.add_argument('--indent', type=int, default=6,
                            help='The number of spaces to indent the output')

    def handle(self, *args, **options):
        file_path = options['file_path']
        indent = options['indent']

        vars = []

        with open(file_path, "r") as f:
            for line in f:
                if (
                    not line or
                    line.startswith("#") or
                    line.startswith("\n") or
                    line.startswith(" ")
                ):
                    continue
                vars.append(line.split("=")[0])

        for var in vars:
            print((" " * indent) + "- %s=${%s}" % (var, var))
