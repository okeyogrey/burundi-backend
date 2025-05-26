import os
from django.core.files import File
from django.core.management.base import BaseCommand
from product_app.models import Product

class Command(BaseCommand):
    help = "Re-upload all existing product images to Cloudinary"

    def handle(self, *args, **options):
        for p in Product.objects.exclude(image='default_image.jpg'):
            # local media path under your project root
            local_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),  # app folder
                '..', '..',  # back up to project root
                'media', p.image.name
            )
            local_path = os.path.normpath(local_path)
            if os.path.exists(local_path):
                with open(local_path, 'rb') as f:
                    # this save() will now use Cloudinary storage
                    p.image.save(os.path.basename(p.image.name), File(f), save=True)
                    self.stdout.write(f"Re-uploaded {p.name}")
            else:
                self.stdout.write(f"Missing file for {p.name}: {p.image.name}")
