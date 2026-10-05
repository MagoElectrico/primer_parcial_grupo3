from setuptools import find_packages, setup

package_name = 'grupo_03_doosan_m0609_tasks'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hp',
    maintainer_email='luquipuqui3@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cinematica_directa_executable=grupo_03_doosan_m0609_tasks.cinematica_directa:main',
            'cinematica_inversa_executable=grupo_03_doosan_m0609_tasks.cinematica_inversa:main',
        ],
    },
)