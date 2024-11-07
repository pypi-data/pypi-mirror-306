import os

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from obs import ObsClient, GetObjectHeader, CompleteMultipartUploadRequest, CompletePart

class OBSManager:
    def __init__(self, access_key_id, secret_access_key, server, bucket_name):
        """
        初始化 OBS 下载器
        
        Args:
            access_key_id (str): OBS访问密钥ID
            secret_access_key (str): OBS访问密钥
            server (str): OBS服务器地址
            bucket_name (str): 桶名称
        """
        
        self.client = ObsClient(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            server=server
        )
        self.bucket_name = bucket_name


    def download(self, object_key: str, file_path: str) -> bool:
        """
        从OBS下载文件
        
        Args:
            object_key (str): OBS对象键（文件在OBS中的路径）
            file_path (str): 本地保存路径
            
        Returns:
            bool: 下载是否成功
        """
        try:
            headers = GetObjectHeader()

            resp = self.client.getObject(
                self.bucket_name, object_key, file_path, headers=headers)

            # 返回码为2xx时，接口调用成功，否则接口调用失败
            if resp.status < 300:
                print(f'文件{object_key}下载成功, request={resp.requestId}')
                return True
            else:
                print(f'文件{object_key}下载失败: {resp.status}, errorCode={resp.errorCode}, errorMessage={resp.errorMessage}')

        except Exception as e:
            print(f'文件{object_key}下载失败: {str(e)}')
            return False


    def upload(self, file_path: str, object_key: str, content_type: str = "application/zip") -> bool:
        """
        向OBS上传文件
        
        Args:
            file_path (str): 本地文件路径
            object_key (str): OBS对象键（文件在OBS中的路径）
            
        Returns:
            bool: 上传是否成功
        """
        try:
            BULK_SIZE = 512 * 1024 * 1024

            # 初始化分段上传任务
            resp = self.client.initiateMultipartUpload(
                bucketName=self.bucket_name,
                objectKey=object_key,
                contentType=content_type
            )
            upload_id = resp.body["uploadId"]
            part_num = 1
            content_length = os.path.getsize(file_path)

            offset = 0
            etags = {}

            while offset < content_length:
                part_size = min(BULK_SIZE, (content_length - offset))
                # 用于上传段
                print('uploading part ' + str(part_num) + '/' + str(int(content_length / BULK_SIZE)))
                resp1 = self.client.uploadPart(self.bucket_name, object_key, part_num, upload_id, file_path, True, part_size, offset)
                etags[part_num] = resp1.body.etag
                offset = offset + part_size
                part_num += 1


            completes = []
            for i in range(1, part_num):
                completes.append(CompletePart(i, etags[i]))

            resp = self.client.completeMultipartUpload(self.bucket_name, object_key, upload_id, CompleteMultipartUploadRequest(parts = completes))
            # 返回码为2xx时，接口调用成功，否则接口调用失败
            if resp.status < 300:
                print(f'文件{file_path}上传成功, request={resp.requestId}, etag={resp.body.etag}')
                return True
            else:
                print(f'文件{file_path}上传失败: {resp.status}, errorCode={resp.errorCode}, errorMessage={resp.errorMessage}')
                return False
                
        except Exception as e:
            print(f'文件{file_path}上传失败: {str(e)}')
            return False
            

    def __del__(self):
        """
        析构函数，确保关闭OBS客户端
        """
        if hasattr(self, 'client'):
            self.client.close()


if __name__ == '__main__':
    parser = ArgumentParser(description='OBS工具', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--access_key', required=True, type=str, help="密钥ID")
    parser.add_argument('--access_secret', required=True, type=str, help="访问密钥")
    parser.add_argument('--bucket_name', required=True, type=str, help="桶名称")
    parser.add_argument('--type', required=True, type=str, help="upload或download")
    parser.add_argument('--object_key', required=True, type=str, help='文件在OBS中的路径')
    parser.add_argument('--file_path', required=True, type=str, help="本地文件路径")
    args = parser.parse_args()

    myOBS = OBSManager(
        access_key_id=args.access_key,
        secret_access_key=args.access_secret,
        server='https://obs.cn-north-4.myhuaweicloud.com',
        bucket_name=args.bucket_name
    )
    if (args.type == 'upload'):
        myOBS.upload(file_path=args.file_path, object_key=args.object_key)

    if (args.type == 'download'):
        myOBS.download(object_key=args.object_key, file_path=args.file_path)