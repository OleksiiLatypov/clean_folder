from setuptools import setup, find_namespace_packages

setup(
    name='cleanfolder',
    version='1.0',
    description='Clean folder script',
    url='https://github.com/OleksiiLatypov?tab=repositories',
    author='Oleksii Latypov',
    author_email='latypov.oleksii.la@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:read_folder']}
)