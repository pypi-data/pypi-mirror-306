# passwordencryption
Reversible password encryption.  
This module encrypt and decrypt a plain text password, with that is possible to add this encrypted password in a config file

# Installation

```
pip install passwordencryption
```
# Usage
```
from passwordencryption import *

```
## Encrypt password
```
password = 'ABCabc'
encrypted_password = passwordencryption.encrypt(password)

print(encrypted_password)
```
Output
```
'bEdyoFB0wjDBK0WOWm6kyR3MLUe7rwkjvv_RXiFVkf4gAAAAABnKhHGTfmlI5Y9kw_3umDMLBI7vHh1k2x_8UyUm-jIvyWgl-fw6m7aDgGiutImaK6CbCp_ua4vrGHGW5D7sdl5Wn9eAg=='
```
## Decrycpt encrypted password
```
encrypted_password = 'bEdyoFB0wjDBK0WOWm6kyR3MLUe7rwkjvv_RXiFVkf4gAAAAABnKhHGTfmlI5Y9kw_3umDMLBI7vHh1k2x_8UyUm-jIvyWgl-fw6m7aDgGiutImaK6CbCp_ua4vrGHGW5D7sdl5Wn9eAg=='
password = passwordencryption.decrypt(encrypted_password)

print(password)
```
Output
```
'ABCabc'
```