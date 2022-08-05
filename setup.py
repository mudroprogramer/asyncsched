
import setuptools

setuptools.setup(
    name='asyncsched',
    version='0.1.0',
    author='Alexander Shapiro',
    author_email='mudroprogramer@gmail.com',
    description='Simple coroutine scheduler for asyncio',
    license='MIT',
    packages=['asyncsched', 'asyncsched.src'],
    install_requires=['asyncio', 'datetime', 'typing', 'freezegun', 'pytest'],
)
