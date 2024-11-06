import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Configura Tailwind CSS per il progetto Django'

    def handle(self, *args, **options):
        # 1. Controlla se Node.js è installato
        self.stdout.write('Checking for Node.js installation...')
        try:
            subprocess.run(['node', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.stderr.write(self.style.ERROR('Error: Node.js is not installed. Please install Node.js.'))
            return

        # 2. Inizializza npm
        self.stdout.write('Initializing npm...')
        subprocess.run(['npm', 'init', '-y'], check=True)

        # 3. Installa Tailwind CSS
        self.stdout.write('Installing Tailwind CSS...')
        subprocess.run(['npm', 'install', 'tailwindcss'], check=True)

        # 4. Inizializza Tailwind CSS
        self.stdout.write('Configuring Tailwind CSS...')
        subprocess.run(['npx', 'tailwindcss', 'init'], check=True)

        # 4.1 Scrive il testo specificato come commento in tailwind.config.js
        self.stdout.write('Updating tailwind.config.js...')
        tailwind_config_content = """// Custom Tailwind CSS Configuration example
module.exports = {
  content: [
    './templates/**/*.html',
    './your_app/templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        with open('tailwind.config.js', 'w') as f:
            f.write(tailwind_config_content)

        # 5. Crea la cartella static/css e il file input.css
        self.stdout.write('Creating static/css/input_tailwind.css...')
        os.makedirs('static/css', exist_ok=True)
        input_css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;
@layer components {
    //insert you custom class here 
    @first_class{
        @apply tailwind classes
    }
}

"""
        with open('static/css/input_tailwind.css', 'w') as f:
            f.write(input_css_content)

        # 7. Aggiorna package.json con lo script build-css
        self.stdout.write('Updating package.json...')
        import json
        with open('package.json', 'r') as f:
            package_json = json.load(f)

        scripts = package_json.get('scripts', {})
        scripts['build_tailwind'] = 'tailwindcss -i ./static/css/input_tailwind.css -o ./static/css/output_tailwind.css --watch'
        package_json['scripts'] = scripts

        with open('package.json', 'w') as f:
            json.dump(package_json, f, indent=2)

        # 8. Istruzioni per aggiornare settings.py
        self.stdout.write(self.style.SUCCESS('Tailwind CSS has been successfully configured!'))
        self.stdout.write('Please add the following lines to your Django settings.py:')
        self.stdout.write("""
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
""")