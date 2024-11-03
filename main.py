import argparse

from cmd_parser.command import import_key, decrypt


def parse_args():
    parser = argparse.ArgumentParser(description="blackbox decryptor")
    subparsers = parser.add_subparsers(dest="command", required=True, help="sub-command help")

    import_key = subparsers.add_parser("import_key", help="Import keys to current PC")
    import_key.add_argument("--encrypted_key", type=str, required=True, help="Path of encrypted key file")
    import_key.add_argument("--password", type=str, required=False, help="Password of encrypted key", default=None)
    import_key.add_argument("--alias", type=str, required=True, help="Key alias")

    decrypt = subparsers.add_parser("decrypt", help="Decrypt black box")
    decrypt.add_argument("--blackbox", type=str, required=True, help="Path of encrypted blackbox")
    decrypt.add_argument("--alias", type=str, required=True, help="Alias of key used to decrypt blackbox")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.command == "import_key":
        import_key(args.alias, args.encrypted_key, args.password)
        print("Import successfully!")
    elif args.command == "decrypt":
        decrypt(args.blackbox, args.alias)
        print("Decrypt successfully!")
    else:
        print("Invalid command")
