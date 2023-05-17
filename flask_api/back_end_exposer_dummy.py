import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Expose the backend"
    )  # FIXME: Better description
    parser.add_argument(
        "--couchdb_master_ip",
        type=str,
        help="ip of a node in the couchdb cluster",
        default="localhost",
    )
    parser.add_argument(
        "--couchdb_username",
        type=str,
        help="username of the couchdb cluster",
        default="admin",
    )
    parser.add_argument(
        "--couchdb_password",
        type=str,
        help="password of the couchdb cluster",
        default="admin",
    )

    args = parser.parse_args()

    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("Welcome to back_end_exposer_dummy.py")
    print("Here are todays parse variables:")
    print(f"    - couchdb_master_ip: {args.couchdb_master_ip}")
    print(f"    - couchdb_username: {args.couchdb_username}")
    print(f"    - couchdb_password: {args.couchdb_password}")
    print("------------------------------------------------------------")
