from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Count lines of code in the project"

    def handle(self, *args, **options):
        project_dir = os.getcwd()
        total_lines = 0

        for root, dirs, files in os.walk(project_dir):
            # Skip virtual environment and migrations
            
            if (
                "venv" in root or
                    "migrations" in root or
                    "melipayamak" in root or
                    "static" in root or
                    "media" in root or
                    "config" in root or

                    "combined_with_prompt.py" in files
            ):
                continue

            for file in files:
                if file.endswith((".py")):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
 
                            lines = len( f.readlines())
                            total_lines += lines
                            if lines > 0:
                                self.stdout.write(
                                    f"{ file } : {lines} lines"
                                )
                    except Exception as e:
                        self.stdout.write(f"Error reading {file}: {e}")

        self.stdout.write(self.style.SUCCESS(f"\nTotal lines: {total_lines}"))
