import csv
import logging


from django.core.management.base import BaseCommand

from regions.models import City, County, Region


# @TODO make a possibility to set up a file name from the command line
class Command(BaseCommand):
    help = 'Imports regions from CSV file'

    # @TODO Consider a better way to determine fields in case of the CSV format update
    def handle_row(self, reader, row):
        try:
            region, _ = Region.objects.get_or_create(code=int(row[16]), defaults={'name': row[4]})
            county, _ = County.objects.get_or_create(
                code=row[15],
                defaults={'name': row[3], 'region': region}
            )
            city, _ = City.objects.get_or_create(
                # If it wouldn't be a test I would ask instead of the assumption of the city unique identifier
                code_insee=row[0],
                defaults={
                    'area': float(row[7]),
                    'code_postal': row[1],
                    'county': county,
                    'name': row[2],
                    'population': float(row[8])
                }
            )
            logging.info('Updated information for city with Code INSEE: {}'.format(city.code_insee))
        except ValueError as e:
            message = 'Error accured during handling of the row {line}. \n' \
                      'Message: {error}\n' \
                      'Values: {values}'.format(
                error=e,
                line=reader.line_num,
                values=row
            )
            logging.error(message)

    def handle(self, *args, **options):
        logging.getLogger().setLevel(logging.INFO)
        file_name = 'correspondance-code-insee-code-postal.csv'

        try:
            with open(file_name) as file:
                reader = csv.reader(file, delimiter=';')
                # Skip file's header
                next(reader)

                for row in reader:
                    self.handle_row(reader, row)
        except FileNotFoundError:
            logging.error(
                'File not found. Make sure that file with the name "{}" exist in the root directory of the app.'
                    .format(file_name)
            )

