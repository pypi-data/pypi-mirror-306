from setuptools import find_packages, setup

setup(
    name='module-inventory-binder',  # The name on PyPI (use hyphens)
    version='1.4.0',
    description='A NetBox plugin to manually bind modules with inventory items.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/module_inventory_binder',
    author='Viktor Kubec',
    author_email='Viktor.Kubec@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,  # Includes non-code files specified in MANIFEST.in
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 3.1',  # Adjust to the version NetBox uses
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',  # Adjust based on your code
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)