# Security

The administration website must be secure. This is one of the critical elements of Telco's information system.

## User access

User access is protected. Several incorrect password entries result in blocking the IP address of the attacker.

## User password

The password policy must be strong. Passwords must be complex.

### Complexity of passwords

The validation of the passwords is thus configured by default:

* checks the similarity between the password and certain attributes of the user,
* Just check the minimum length of the password. This validator is configured with a custom option: it requires a minimum length of 11 characters,
* Check if the password is in a list of current passwords. By default, this comparison is done with a list of 10,000 common passwords created by [Mark Burnett] (https://web.archive.org/web/20150315154609/https://xato.net/passwords/more- top-worst-passwords /).
* verifies that the password is not entirely numeric.

### Storage

Django's password storage system uses PBKDF2 by default. The PBKDF2 algorithm with hash function SHA256, a password stretching mechanism recommended by NIST. This should be enough for most users: it is a very secure algorithm and requires huge amounts of computing power to be broken.

But to increase security, we use the Argon2 algorithm (requires an external library). Argon2 is the winner of the 2015 Password Hashing Competition, an open competition organized by the community to select a new generation hashing algorithm. It is designed to be easier to compute on dedicated hardware than it is on an ordinary processor.

References: [password management in the Django framework] (https://docs.djangoproject.com/en/1.11/topics/auth/passwords/)

## Honey pot

Robots pollute our internet environment by automatically attacking websites. Remarkable addresses are targeted like */admin*. The introduction of a honeypot can detect fraudulent attempts simply and automatically. The robots are thus blocked without causing them damage.

