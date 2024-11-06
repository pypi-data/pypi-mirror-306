import os
import tempfile
from datetime import datetime, timezone
from pprint import pprint
from typing import Optional

import awswrangler as wr
import boto3
import botocore
from avro.datafile import DataFileReader
from avro.io import DatumReader
from botocore.client import Config

from baram.kms_manager import KMSManager
from baram.log_manager import LogManager


class S3Manager(object):
    def __init__(self, bucket_name: str, region: Optional[str] = 'ap-northeast-2'):

        config = Config(region_name=region, signature_version='v4')
        self.cli = boto3.client('s3', config=config)
        self.km = KMSManager(region=region)
        self.logger = LogManager.get_logger('S3Manager')
        self.bucket_name = bucket_name
        try:
            bi = self.get_bucket_encryption()
            self.kms_algorithm, self.kms_id = bi['SSEAlgorithm'], bi['KMSMasterKeyID']
        except:
            self.kms_algorithm, self.kms_id = None, None

    def list_buckets(self):
        '''
        :return: response
        '''
        response = self.cli.list_buckets()
        return response['Buckets'] if 'Buckets' in response else None

    def put_object(self, s3_key_id: str, body):
        '''

        :param s3_key_id: s3 key id. ex) nylon-detector/a.csv
        :param body: byte or str data
        :return: response
        '''
        kwargs = {"Bucket": self.bucket_name,
                  "Key": s3_key_id,
                  "Body": body}
        if self.kms_id:
            kwargs['ServerSideEncryption'] = self.kms_algorithm
            kwargs['SSEKMSKeyId'] = self.kms_id
        response = self.cli.put_object(**kwargs)
        return response

    def get_object(self, s3_key_id: str):
        '''

        :param s3_key_id: s3 key id. ex) nylon-detector/a.csv
        :return: response
        '''
        try:
            response = self.cli.get_object(Bucket=self.bucket_name,
                                           Key=s3_key_id)
            return response['Body'].read()
        except self.cli.exceptions.NoSuchKey:
            self.logger.info(f'{s3_key_id} does not exist.')
            return None

    def get_object_by_lines(self, s3_key_id: str):
        '''
        get s3 object line by line.

        :param s3_key_id: s3 key id. ex) nylon-detector/a.csv
        :return: response
        '''

        try:
            import codecs
            line_stream = codecs.getreader("utf-8")
            response = self.cli.get_object(Bucket=self.bucket_name,
                                           Key=s3_key_id)
            return line_stream(response['Body'])
        except self.cli.exceptions.NoSuchKey:
            self.logger.info(f'{s3_key_id} does not exist.')
            return None

    def delete_object(self, s3_key_id: str):
        '''

        :param s3_key_id: s3 key id. ex) nylon-detector/a.csv
        :return: response
        '''
        return self.cli.delete_object(Bucket=self.bucket_name,
                                      Key=s3_key_id)

    def delete_objects(self, s3_keys: list, quiet: bool = True):
        objects = [{'Key': k} for k in s3_keys]
        return self.cli.delete_objects(Bucket=self.bucket_name,
                                       Delete={
                                           'Objects': objects,
                                           'Quiet': quiet
                                       })

    def upload_dir(self, local_dir_path: str, s3_dir_path: str):
        '''
        Upload directory.
        :param local_dir_path: local dir path. ex) /Users/lks21c/repo/sli-aflow
        :param s3_dir_path: s3 path. ex) nylon-detector/crawl_data
        :return: response
        '''
        self.logger.info('Uploading results to s3 initiated...')
        self.logger.info(f'local_path:{local_dir_path}, s3_path:{s3_dir_path}')
        try:
            for path, subdirs, files in os.walk(local_dir_path):
                for file in files:
                    dest_path = path.replace(local_dir_path, '')
                    s3_file_path = os.path.normpath(s3_dir_path + '/' + dest_path + '/' + file)
                    local_file_path = os.path.join(path, file)

                    extra_args = {'ServerSideEncryption': self.kms_algorithm,
                                  'SSEKMSKeyId': self.kms_id} if self.kms_id else None
                    self.cli.upload_file(local_file_path, self.bucket_name, s3_file_path, ExtraArgs=extra_args)
                    self.logger.info(
                        f'upload : {local_file_path} to Target: s3://{self.bucket_name}/{s3_file_path} Success.')
        except Exception as e:
            self.logger.info(e)
            raise e

    def write_and_upload_file(self, content: str, local_file_path: str, s3_file_path: str, do_remove: bool = False):
        '''
        Upload file.

        :param content: the content of file. ex) 'col1,col2\nname,height'
        :param local_file_path: local file path. ex) /Users/lks21c/repo/sli-aflow/a.csv
        :param s3_file_path: s3 path. ex) nylon-detector/crawl_data/a.csv
        :param do_remove: remove written file
        :return: response
        '''

        with open(local_file_path, 'w') as f:
            f.write(content)
        assert os.path.exists(local_file_path)
        self.upload_file(local_file_path, s3_file_path)

        if do_remove:
            os.remove(local_file_path)

    def upload_file(self, local_file_path: str, s3_file_path: str):
        '''
        Upload file.

        :param local_file_path: local file path. ex) /Users/lks21c/repo/sli-aflow/a.csv
        :param s3_file_path: s3 path. ex) nylon-detector/crawl_data/a.csv
        :return: response
        '''

        try:
            extra_args = {'ServerSideEncryption': self.kms_algorithm,
                          'SSEKMSKeyId': self.kms_id} if self.kms_id else None
            self.cli.upload_file(local_file_path, self.bucket_name, s3_file_path, ExtraArgs=extra_args)
            self.logger.info(f'upload : {local_file_path} to Target: s3://{self.bucket_name}/{s3_file_path} Success.')
        except Exception as e:
            self.logger.info(e)
            raise e

    def download_dir(self, s3_dir_path: str, local_dir_path: str = os.getcwd()):
        '''
        Download directory from s3.

        :param s3_dir_path: s3 path. ex) nylon-detector/crawl_data
        :param local_dir_path: local dir path. ex) /Users/lks21c/repo/sli-aflow
        :return: response
        '''
        self.logger.info('Downloading results to s3 initiated...')
        self.logger.info(f's3_path:{s3_dir_path}, local_path:{local_dir_path}')
        bucket = boto3.resource('s3').Bucket(self.bucket_name)
        for obj in bucket.objects.filter(Prefix=s3_dir_path):
            local_obj_path = os.path.join(local_dir_path, obj.key)
            if not os.path.exists(os.path.dirname(local_obj_path)):
                os.makedirs(os.path.dirname(local_obj_path))
            bucket.download_file(obj.key, local_obj_path)
            self.logger.info(f'download : {obj.key} to Target: {local_obj_path} Success.')

    def delete_dir(self, s3_dir_path: str):
        '''
        Delete s3 directory.

        :param s3_dir_path: s3 path. ex) nylon-detector/crawl_data
        :return:
        '''
        files = self.list_objects(s3_dir_path)
        if not files:
            return
        s3_keys = []
        for k in self.list_objects(s3_dir_path):
            s3_keys.append(k['Key'])
            if len(s3_keys) % 1000 == 0:
                self.logger.info(f'delete 1000 keys.')
                self.delete_objects(s3_keys)
                s3_keys = []
        if len(s3_keys) > 0:
            self.logger.info(f'delete {len(s3_keys)} keys.')
            self.delete_objects(s3_keys)
        self.logger.info(f'delete {s3_dir_path}')

    def download_file(self, s3_file_path: str, local_file_path: str):
        '''
        Download file from s3.
        \
        :param s3_dir_path: s3 path. ex) nylon-detector/crawl_data/a.csv
        :param local_file_path: local file path. ex) /Users/lks21c/repo/sli-aflow/a.csv
        :return: response
        '''
        bucket = boto3.resource('s3').Bucket(self.bucket_name)
        bucket.download_file(s3_file_path, local_file_path)
        self.logger.info(f'download : {s3_file_path} to Target: {local_file_path} Success.')

    def list_objects(self, prefix: str = '', delimiter: str = ''):
        '''
        List S3 objects.

        :param prefix: Limits the response to keys that begin with the specified prefix.
        :param delimiter: A delimiter is a character you use to group keys.
        :return: response
        '''
        kwargs = {'Bucket': self.bucket_name, 'Prefix': prefix, 'Delimiter': delimiter}
        objects = []

        while True:
            response = self.cli.list_objects_v2(**kwargs)
            if 'Contents' in response:
                for obj in response['Contents']:
                    objects.append(obj)
            if 'NextContinuationToken' in response:
                kwargs['ContinuationToken'] = response['NextContinuationToken']
            else:
                break

        return objects if objects else None

    def list_dir(self, prefix: str = '', delimiter: str = '/'):
        '''
        List directory.

        :param prefix: Limits the response to keys that begin with the specified prefix.
        :param delimiter: A delimiter is a character you use to group keys.
        :return: response
        '''
        response = self.cli.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, Delimiter=delimiter)
        list = []
        if 'Contents' in response:
            list += [item['Key'] for item in response['Contents'] if 'Key' in item]
        if 'CommonPrefixes' in response:
            list += [prefix['Prefix'] for prefix in response['CommonPrefixes']]
        return list

    def get_s3_arn(self, bucket_name):
        '''

        :param bucket_name: bucket name
        :return: s3 bucket arn
        '''
        return next(
            (f'arn:aws:s3:::{i["Name"]}' for i in self.list_buckets() if bucket_name in i['Name']),
            None)

    def get_bucket_encryption(self):
        '''

        :return: KMS ID
        '''
        conf = self.cli.get_bucket_encryption(Bucket=self.bucket_name)['ServerSideEncryptionConfiguration']
        return conf['Rules'][0]['ApplyServerSideEncryptionByDefault'] if conf else None

    def copy(self, from_key: str, to_key: str, to_bucket: Optional[str] = None, **kwargs):
        '''
        Creates a copy of an object that is already stored in Amazon S3.

        :param from_key: origin s3 key
        :param to_key: destination s3 key
        :param to_bucket: destination s3 bucket
        :return:
        '''

        copy_source = {
            'Bucket': self.bucket_name,
            'Key': from_key
        }
        to_bucket = to_bucket if to_bucket else self.bucket_name
        self.cli.copy(copy_source, to_bucket, to_key, ExtraArgs=kwargs)

    def copy_object(self, from_key: str, to_key: str):
        '''
        Creates a copy of an object that is already stored in Amazon S3.

        :param from_key: origin s3 key
        :param to_key: destination s3 key
        :return:
        '''
        self.cli.copy_object(
            Bucket=self.bucket_name,
            CopySource=f'{self.bucket_name}/{from_key}',
            Key=to_key
        )

    def get_s3_web_url(self, s3_bucket_name, path: str, region: str = 'ap-northeast-2'):
        '''
        get s3 web url

        :param s3_bucket_name: s3 bucket name
        :param path: s3 path
        :param region: s3 region
        :return:
        '''
        return f'https://s3.console.aws.amazon.com/s3/buckets/{s3_bucket_name}?region={region}&prefix={path}'

    def convert_s3_path_to_web_url(self, s3_path: str):
        '''
        Convert s3 url to web url

        :param s3_path:
        :return:
        '''
        token = s3_path.replace('s3://', '').split('/')
        return self.get_s3_web_url(token[0], '/'.join(token[1:]))

    def get_s3_full_path(self, s3_bucket_name: str, path: str):
        '''
        Get s3 full path.

        :param s3_bucket_name: bucket name
        :param path: path
        :return:
        '''
        return f's3://{s3_bucket_name}/{path}'

    def head_s3_object(self, s3_bucket_name: str, path: str):
        '''
        Head s3 object.
        :param s3_bucket_name:
        :param path:
        :return:
        '''

        try:
            response = self.cli.head_object(Bucket=s3_bucket_name, Key=path)
            return response
        except botocore.exceptions.ClientError as e:
            return None

    def check_s3_object_exists(self, s3_bucket_name: str, path: str):
        '''
        Check if s3 object exists.

        :param s3_bucket_name: s3 bucket name
        :param path:  path
        :return:
        '''
        try:
            self.head_s3_object(s3_bucket_name, path)
            return True
        except botocore.exceptions.ClientError as e:
            pass
        return False

    def rename_file(self, from_file_path: str, to_file_path: str):
        '''
        Rename s3 obj.

        :param from_file_path:
        :param to_file_path:
        :return:
        '''
        self.copy_object(from_key=from_file_path, to_key=to_file_path)
        self.delete_dir(from_file_path)

    def count_csv_row_count(self, csv_path: str, distinct_col_name: Optional[str] = None):
        df = wr.s3.read_csv(path=f's3://{self.bucket_name}/{csv_path}', index_col=False,
                            keep_default_na=False)
        import pandas as pd

        if distinct_col_name:
            return len(pd.unique(df[distinct_col_name]))
        else:
            return df.shape[0]

    def analyze_s3_access_logs(self,
                               bucket_name: str,
                               prefix: str = None,
                               start_date: str = None,
                               end_date: str = None,
                               timezone=timezone.utc):
        '''
        Analyze S3 access logs to count read and write operations.

        :param bucket_name:
        :param prefix:
        :param start_date:
        :param end_date:
        :return:
        '''

        s3 = boto3.client('s3')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone)

        kwargs = {'Bucket': bucket_name}
        if prefix:
            kwargs['Prefix'] = prefix

        stats = []
        while True:
            response = s3.list_objects_v2(**kwargs)

            if 'Contents' not in response:
                break

            pprint(response)

            for obj in response['Contents']:

                if start_date and obj['LastModified'] < start_date:
                    continue
                if end_date and obj['LastModified'] >= end_date:
                    continue

                log_file = obj['Key']
                try:
                    log_content = s3.get_object(Bucket=bucket_name, Key=log_file)['Body'].read().decode('utf-8')
                except Exception as e:
                    print(f'Error: {e} {log_file}')
                    continue

                for line in log_content.splitlines():
                    token = line.split(' ')
                    cnt_type = 'read' if token[9].replace('"', '') in ('GET', 'HEAD') else 'write'
                    target_bucket = token[1]
                    resource = token[10]

                    found = False
                    for i, (ct, tb, res, val) in enumerate(stats):
                        if ct == cnt_type and tb == target_bucket and res == resource:
                            stats[i] = (ct, tb, res, val + 1)
                            found = True
                            break

                    if not found:
                        stats.append((cnt_type, target_bucket, resource, 1))

            if 'NextContinuationToken' in response:
                kwargs['ContinuationToken'] = response['NextContinuationToken']
            else:
                break

        stats.sort(key=lambda x: x[3], reverse=True)
        return self._format_stats_for_excel(stats)

    def _format_stats_for_excel(self, stats):
        headers = ["Count Type", "Target Bucket", "Resource", "Value"]
        rows = [headers] + stats
        formatted_output = "\n".join(["\t".join(map(str, row)) for row in rows])
        return formatted_output

    def get_avro_as_list(self, avro_path: str):
        """
        :param avro_path:
        :return:
        """
        filename = avro_path.split('/')[-1]
        assert filename.split('.')[-1] != 'avro'

        with tempfile.TemporaryDirectory() as tmpdir:
            local_file_path = f'{tmpdir}/{filename}'
            self.download_file(s3_file_path=avro_path,
                               local_file_path=local_file_path)
            reader = DataFileReader(open(local_file_path, 'rb'), DatumReader())

        return list(reader)

    def change_object_storage_class(self, prefix: str = '', delimiter: str = '', storage_class: str = 'DEEP_ARCHIVE'):
        '''
        Change the storage class of all objects in the S3 bucket to DEEP_ARCHIVE.

        :param prefix: Limits the response to keys that begin with the specified prefix.
        :param delimiter: A delimiter is a character you use to group keys.
        :param storage_class: STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, GLACIER, DEEP_ARCHIVE
        '''

        objects = self.list_objects(prefix=prefix,delimiter=delimiter)
        if objects:
            for obj in objects:
                try:
                    self.copy(from_key=obj['Key'], to_key=obj['Key'], StorageClass=storage_class)
                except Exception as e:
                    print(obj['Key'] + f' error {e}')