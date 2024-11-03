from setuptools import setup, Command
import shutil
import os

class PostInstallCommand(Command):
    """Post-installation script to copy check.py to new_file.py and add to .gitignore"""
    description = 'Post-installation script to copy check.py to new_file.py and add to .gitignore'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        source_file = os.path.join('auto_loc', 'check.py')
        destination_file = 'web_inspector.py'
        gitignore_file = '.gitignore'

        try:
            # Copy the contents of check.py to new_file.py
            if os.path.exists(source_file):
                shutil.copyfile(source_file, destination_file)
                print(f"Copied contents of {source_file} to {destination_file}")
            else:
                print(f"{source_file} does not exist")

            # Add new_file.py to .gitignore
            with open(gitignore_file, 'a') as gitignore:
                gitignore.write(f'\n{destination_file}\n')
                print(f"Added {destination_file} to {gitignore_file}")
        except Exception as e:
            print(f"An error occurred: {e}")

setup(
    name='web_inspector_selenium',
    version='0.1',
    packages=['web_inspector'],
    cmdclass={
        'install': PostInstallCommand,
    },
)