from setuptools import setup, Command
from setuptools.command.install import install
import shutil
import os
import logging

class PostInstallCommand(install):
    """Post-installation script to copy check.py to new_file.py and add to .gitignore"""
    def run(self):
        install.run(self)
        logging.basicConfig(level=logging.INFO)
        base_dir = os.path.dirname(__file__)
        source_file = os.path.join(base_dir, 'auto_loc', 'check.py')
        destination_file = 'web_inspector.py'
        gitignore_file = os.path.join(base_dir, '.gitignore')

        logging.info(f"Base directory: {base_dir}")
        logging.info(f"Source file path: {source_file}")
        logging.info(f"Destination file path: {destination_file}")
        logging.info(f".gitignore file path: {gitignore_file}")

        try:
            if os.path.exists(source_file):
                shutil.copyfile(source_file, destination_file)
                logging.info(f"Copied contents of {source_file} to {destination_file}")
            else:
                logging.warning(f"{source_file} does not exist")

            with open(gitignore_file, 'a') as gitignore:
                gitignore.write(f'\n{destination_file}\n')
                logging.info(f"Added {destination_file} to {gitignore_file}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

setup(
    name='qa-auto-loc',
    version='7.1.6',
    packages=['auto_loc'],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'distutils.commands': [
            'install = PostInstallCommand',
        ],
    },
)