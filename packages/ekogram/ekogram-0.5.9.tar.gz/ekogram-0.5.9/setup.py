from setuptools import setup

package_name = 'ekogram'

setup(
    name=package_name,
    version='0.5.9',
    description='Lightweight library for working with Telegram Bot Api version 7.10',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SiriRSST/Ekogram',
    author='Siri-Team',
    author_email='siriteamrs@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'],
    keywords=['telebot', 'bot', 'gram', 'pytelegrambotapi', 'telegram', 'ekogram', 'aiogram'],
    packages=['ekogram'],
    install_requires=['requests'],
    python_requires='>=3.7'
)
