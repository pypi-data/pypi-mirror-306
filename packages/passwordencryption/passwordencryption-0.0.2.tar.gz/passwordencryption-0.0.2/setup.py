setup(
   name="Cleartxt-password-encryption"",
   author="Ricardo Claramunt",
   author_email="ricardo#claramunt.ch",
   description="Private Python library who provides an password encrytion/decryption that you do not have anyplain text password in a config file.",
   version ="0.0.2",
   include_package_data=True,
   install_requires=[
        'cryptography'
    ]
   python_requires='>=3.6',
   setup_requires=['setuptools-git-versioning'],
   version_config={
       "dirty_template": "{tag}",
   }
   keywords="password", "encryption",
   package_dir={"": "src"},
   packages=find_packages(where="src"),
   #install_requires=["cryptography"],
)
