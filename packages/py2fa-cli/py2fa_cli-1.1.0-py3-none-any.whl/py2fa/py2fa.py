"""Calculate one-time passwords for two-factor authentication."""

import argparse
import binascii
import sys
from time import time

from pyotp import TOTP, parse_uri

from py2fa import VERSION
from py2fa.config import load_secrets


def _parse_args():
    parser = argparse.ArgumentParser(
        description="""Calculate one-time passwords for two-factor authentication.""")

    parser.add_argument('secret_name', help='name of secret to display TOTP code for')
    parser.add_argument('-v', '--version', action='version', version=VERSION)

    return parser.parse_args()


def _make_totp(secret):
    if secret.startswith('otpauth://totp/'):
        return parse_uri(secret)

    return TOTP(secret)


def main():
    args = _parse_args()

    secrets = load_secrets()
    if secrets is None:
        sys.exit('ERR: Failed to load secrets file!')

    try:
        secret = secrets[args.secret_name]
    except KeyError:
        sys.exit(f'ERR: No secret for {args.secret_name} is available!')

    try:
        totp = _make_totp(secret)
    except ValueError as err:
        sys.exit(f'ERR: Failed to create TOTP object: {err}')

    valid_for = totp.interval - time() % totp.interval

    try:
        print(f'One-time password: {totp.now()} (valid for {valid_for:.1f} seconds)')
    except (ValueError, binascii.Error) as err:
        sys.exit(f'ERR: Failed to generate TOTP: {err}. Verify your secret.')


if __name__ == '__main__':
    main()
