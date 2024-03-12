import json
from swan.api.mcs_api import MCSAPI, File
from swan.common.utils import datetime_to_unixtime


class SourceFilesInfo():
    
    def __init__(self):
        self.file_list = []
        self.mcs_client = None
        
    def mcs_connection(self, mcs_client: MCSAPI):
        """Add mcs connection.

        Args:
            mcs_client: mcs API object.
        """
        self.mcs_client = mcs_client

    def add_folder(self, bucket_name: str, object_name: str):
        """Add a folder/repo to the source file info.

        Args:
            bucket_name: bucket name of bucket locating the folder.
            object_name: folder object_name (directory)
        """
        folder_file = self.mcs_client._get_full_file_list(bucket_name, object_name)
        self.file_list += self.get_folder_files(bucket_name, folder_file)
        

    def add_file(self, bucket_name: str, object_name: str):
        """Add single file to source file info.

        Args:
            bucket_name: bucket name of bucket locating the folder.
            object_name: file object_name (directory + file name)
        """
        file = self.mcs_client.get_file(bucket_name, object_name)
        list.append(file)

    def _file_to_dict(self, file: File):
        return {
            "cid": file.payloadCid,
            "created_at": datetime_to_unixtime(file.created_at),
            "name": file.name,
            "updated_at": datetime_to_unixtime(file.updated_at),
            "url": file.ipfs_url
        }
    
    def get_folder_files(self, bucket_name: str, file_list: list):
        """Retrieve all files under folders.

        Args: 
            bucket_name: bucket name of bucket locating the folder.
            file_llist: list of directories (cotain folders).
        
        Returns:
            Updated file_list without folder and all files under given directories.
        """
        folder_list = []
        exist_folder = False
        for file in file_list:
            if file.is_folder:
                exist_folder = True
                folder_list.append(file)
                file_list.remove(file)
        for folder in folder_list:
            new_file_list = self.mcs_client.list_files(bucket_name, folder.object_name)
            file_list += new_file_list
        if exist_folder:
            file_list = self.get_folder_files(bucket_name, file_list)
        return file_list

    def to_dict(self):
        return {
            "data": {
                "files": [
                    self._file_to_dict(file) for file in self.file_list
                ]
            }
        }
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    

class Repository():

    def __init__(self):
        """Initialize repository for swan task.
        """
        self.folder_dir = None
        self.bucket = None
        self.path = None
        self.source_uri = None

    def update_bucket_info(self, bucket_name: str, object_name: str):
        """Update the current mcs bucket info on MCS.

        Args:
            bucket_name: name of bucket.
            object_name: directory + file_name.
        """
        self.bucket = bucket_name
        self.path = object_name

    def add_local_dir(self, folder_dir: str):
        """Initialize repository for swan task.

        Args:
            folder_dir: Directory of folder to upload to mcs.
        """
        self.folder_dir = folder_dir

    def mcs_connection(self, mcs_client: MCSAPI):
        """Add mcs connection.

        Args:
            mcs_client: mcs API object.
        """
        self.mcs_client = mcs_client

    def upload_local_to_mcs(self, bucket_name: str, obj_name: str, mcs_client: MCSAPI = None):
        """Upload repository to MCS to create remote source.

        Args:
            bucket_name: bucket to upload repository.
            obj_name: dir + file_name for repository.
            mcs_client: mcs API object.

        Returns:
            API response from uploading folder to MCS. Contain info of list of files uploaded.
        """
        if self.folder_dir:
            if mcs_client:
                self.mcs_connection(mcs_client)
            self.bucket = bucket_name
            self.path = obj_name
            upload = mcs_client.upload_folder(bucket_name, obj_name, self.folder_dir)
            return upload
        return None

    def generate_source_uri(self, bucket_name: str, obj_name: str, file_path: str, mcs_client: MCSAPI = None, replace: bool = True):
        """Generate source uri for task using MCS service.

        Args:
            bucket_name: bucket name to store source uri.
            obj_name: object name (dir + file name) to store source uri.
            file_path: local file path to store source uri JSON file.
            replace: replace existing file or not.
            mcs_client: mcs API object.

        Returns：
            API response from MCS after uploading. Contains file information.

        """
        if self.bucket and self.path:
            if mcs_client:
                self.mcs_connection(mcs_client)
                local_source = SourceFilesInfo()
                local_source.mcs_connection(mcs_client)
                local_source.add_folder(self.bucket, self.path)
                with open(file_path, "w") as file:
                    json.dump(local_source.to_dict(), file)
                res = mcs_client.upload_file(bucket_name, obj_name, file_path, replace)
                self.source_uri = res.ipfs_url
                return res
            
    def to_dict(self):
        return {
            "folder_dir": self.folder_dir,
            "bucket_name": self.bucket,
            "folder_path": self.path,
            "source_uri": self.source_uri
        }

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)