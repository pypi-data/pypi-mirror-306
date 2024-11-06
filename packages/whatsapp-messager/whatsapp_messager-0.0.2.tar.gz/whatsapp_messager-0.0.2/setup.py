from setuptools import setup, find_packages

# Package meta-data
VERSION = "0.0.1"
DESCRIPTION = "WhatsApp message sender"
LONG_DESCRIPTION = open("README.md").read()
AUTHOR = "John Gbaya-kokoya"
EMAIL = "gbayakokoyajohnjr@gmail.com"
URL = "https://github.com/John-sys/whatsapp-sender_library"

setup(
    name="whatsapp_messager",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=[
        "requests>=2.25.0",
        "setuptools>=42.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="whatsapp, messaging, automation, api",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/whatsapp-sender/issues",
        "Source": "https://github.com/yourusername/whatsapp-sender",
        "Documentation": "https://github.com/yourusername/whatsapp-sender#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
