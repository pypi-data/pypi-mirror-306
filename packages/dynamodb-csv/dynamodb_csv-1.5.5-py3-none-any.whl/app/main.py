import os
import boto3
from boto3.session import Session
import configparser
import argparse
import sys
from typing import Any, Tuple, List

from app.dynamodb import csv_import, csv_export, truncate, move

__version__ = "1.5.5"
config_file = "config.ini"


def main() -> None:
    """Main routine
    """
    (message, code) = execute()
    print(message)
    sys.exit(code)


def execute() -> Tuple:
    """Command execute

    Raises:
        ValueError: invalid config

    Returns:
        Tuple: result message and exit code
    """

    result = "No operations."

    # arguments parse
    args = parse_args(sys.argv[1:])

    # boto3 config setting
    try:
        tables = config_read_and_get_table(args)
    except ValueError as e:
        return (str(e), 1)

    except Exception:
        return (f"Invalid format {config_file} file", 1)

    # csv import
    if args.imp:
        if args.file is not None:
            result = csv_import(tables[0], args.file, args.ignore)
        else:
            return ("Import mode requires a input file option.", 1)

    # csv export
    if args.exp:
        if args.output is not None:
            parameters = {}
            if args.index is not None:
                parameters["IndexName"] = args.index
            result = csv_export(tables[0], args.output, parameters)
        else:
            return ("Export mode requires a output file option.", 1)

    # truncate table
    if args.truncate:
        result = truncate(tables[0])

    # move table
    if args.move:
        if len(tables) == 2:
            result = move(tables)
        else:
            return ("Move mode requires a two tables.", 1)

    return result


def parse_args(args: str) -> Any:
    """Parse arguments

    Args:
        args (str): _description_

    Returns:
        Any: parsed args
    """
    parser = argparse.ArgumentParser(
        description="Import CSV file into DynamoDB table utilities")
    parser.add_argument("-v", "--version", action="version",
                        version=__version__,
                        help="show version")
    parser.add_argument(
        "-i", "--imp", help="mode import", action="store_true")
    parser.add_argument(
        "-e", "--exp", help="mode export", action="store_true")
    parser.add_argument(
        "--truncate", help="mode truncate", action="store_true")
    parser.add_argument(
        "--move", help="mode move", action="store_true")
    parser.add_argument(
        "-t", "--table", nargs="*", help="DynamoDB table name", required=True)
    parser.add_argument(
        "-idx", "--index", help="DynamoDB index name")
    parser.add_argument(
        "-f", "--file", help="UTF-8 CSV file path required import mode")
    parser.add_argument(
        "-o", "--output", help="output file path required export mode")
    parser.add_argument(
        "--ignore", help="ignore import error", action="store_true")
    parser.add_argument(
        "--profile", help="using AWS profile")

    return parser.parse_args()


def config_read_and_get_table(args: Any) -> List:
    """Config read and Create DynamoDB table instance

    Args:
        args (Any): arguments

    Returns:
        List: DynamoDB tables class
    """
    # using AWS profile
    if args.profile:
        session = Session(profile_name=args.profile)
        dynamodb = session.resource('dynamodb')
    else:
        # using config
        if not os.path.isfile(config_file):
            raise ValueError(f"Please make your {config_file} file")

        config = configparser.ConfigParser()
        config.optionxform = str
        config.read_dict({"AWS": {"ENDPOINT_URL": ""}})
        config.read(config_file)

        endpoint_url = None
        if config.get("AWS", "ENDPOINT_URL"):
            endpoint_url = config.get("AWS", "ENDPOINT_URL")
        dynamodb = boto3.resource("dynamodb",
                                  region_name=config.get("AWS", "REGION"),
                                  aws_access_key_id=config.get(
                                      "AWS", "AWS_ACCESS_KEY_ID"),
                                  aws_secret_access_key=config.get(
                                      "AWS", "AWS_SECRET_ACCESS_KEY"),
                                  endpoint_url=endpoint_url)

    tables = []
    for table in args.table:
        tables.append(dynamodb.Table(table))

    return tables


if __name__ == "__main__":
    main()
