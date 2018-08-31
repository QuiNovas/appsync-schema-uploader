from __future__ import print_function

import argparse
import atexit
import boto3
import logging
import sys
import time


if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m appsync_schema_uploader"


@atexit.register
def app_exit():
    logging.getLogger().info("Terminating")


def _parse_command_line_arguments():
    argv_parser = argparse.ArgumentParser()
    argv_parser.add_argument(
        '--aws-access-key-id',
        help='The AWS IAM Access Key ID to use'
    )
    argv_parser.add_argument(
        '--aws-secret-access-key',
        help='The AWS IAM Secret Access Key to use'
    )
    argv_parser.add_argument(
        '--aws-region',
        help='The AWS Region of the AppSync API to update'
    )
    argv_parser.add_argument(
        '--api-id',
        help='The API Id of the AppSync API to update'
    )
    argv_parser.add_argument(
        '--schema',
        help='The schema file to upload'
    )
    return argv_parser.parse_args()


def main():
    try:
        args = _parse_command_line_arguments()

        # set AWS logging level
        logging.getLogger('botocore').setLevel(logging.ERROR)
        logging.getLogger('boto3').setLevel(logging.ERROR)

        appsync = boto3.client(
            'appsync',
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key,
            region_name=args.aws_region
        )
        with open(args.schema) as schema:
            print('Uploading schema', args.schema)
            response = appsync.start_schema_creation(
                apiId=args.api_id,
                definition=schema.read()
            )
        while response['status'] not in ('ACTIVE', 'SUCCESS'):
            print('Waiting for upload completion')
            time.sleep(2)
            response = appsync.get_schema_creation_status(
                apiId=args.api_id
            )
        print('Upload complete')
    except KeyboardInterrupt:
        print('Service interrupted', file=sys.stderr)
    except Exception as e:
        print('Upload FAILED:', e.message, file=sys.stderr)
        print('')
        raise e


if __name__ == '__main__':
    main()

