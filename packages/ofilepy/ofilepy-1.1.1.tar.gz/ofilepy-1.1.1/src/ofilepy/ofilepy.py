# %%
__version__ = '1.1.0'

# %% [markdown]
# # ofilepath Lib (Moving/Copying/Getting Files Information)

# %%
import os
import time
import shutil
import pathlib
import datetime

def get_file_extension(file_path: str):
    file_extension = os.path.splitext(file_path)[1]
    return(file_extension)

def get_file_name(file_path: str, extension: bool=True):
    if extension == True:
        file_name = file_path[(len(file_path) - file_path[::-1].find('\\')):]
    else:
        extension_size = len(os.path.splitext(file_path)[1])
        file_name = file_path[(len(file_path) - file_path[::-1].find('\\')):-extension_size]

    return file_name

def get_last_file(file_path: str=None, extension: bool=True, file_type: str='', contains: str=''):
    if file_path is None: file_path = get_downloads_folder()
    list_of_files = [str(file) for file in pathlib.Path(file_path).iterdir() if not file.is_dir() and str(file).endswith(file_type) and contains in str(file)]
    file_path = max(list_of_files, key=os.path.getctime)
    extension_size = file_path[::-1].find('.')
    file_path_without_extension = file_path[:-(extension_size+1)]

    if extension == True: file = file_path
    else: file = file_path_without_extension
        
    return file

def get_last_file_name(file_path=None,extension=True,file_type='',contains=''):
    if file_path == None: file_path = get_downloads_folder()
    try:
        list_of_files = [str(file) for file in pathlib.Path(file_path).iterdir() if not file.is_dir() and str(file).endswith(file_type) and contains in str(file)]
        file_path = max(list_of_files, key=os.path.getctime)
        file_name = file_path[(len(file_path) - file_path[::-1].find('\\')):]
        extension_size = file_name[::-1].find('.')
        file_name_without_extension = file_path[(len(file_path) - file_path[::-1].find('\\')):-(extension_size+1)]

        if extension == True:
            file = file_name
            
        else:
            file = file_name_without_extension
            
        return file
    except:
        return print('Any file was found!')
    
def move_the_last_file(old_path,new_path,file_type='',contains='',delete=False):
    list_of_files = [str(i) for i in pathlib.Path(old_path).iterdir() if not i.is_dir() and str(i).endswith(file_type) and contains in str(i)]
    latest_file = max(list_of_files, key=os.path.getctime)
    new_file = latest_file.replace(old_path,new_path)
    
    if delete == False:
        try:
            os.rename(latest_file, new_file)
        except:
            print('File already exist!')
            
    else:
        try:
            os.rename(latest_file, new_file)
        except:
            os.remove(new_file)
            os.rename(latest_file, new_file)

def rename_file(old_path,new_path,delete=False):
    if delete == False:
        try: os.rename(old_path, new_path)
        except: print('File already exist!')
    else:
        try: os.rename(old_path, new_path)
        except: os.remove(new_path); os.rename(old_path, new_path)
             
def copy_the_last_file(old_path,new_path,file_type=''):
    list_of_files = [str(i) for i in pathlib.Path(old_path).iterdir() if not i.is_dir() and file_type in str(i)]
    lastest_file = max(list_of_files, key=os.path.getctime)
    lastest_file_name = lastest_file[(len(lastest_file) - lastest_file[::-1].find('\\')):]
    new_file_name = lastest_file[(len(lastest_file) - lastest_file[::-1].find('\\')):]
    new_file = lastest_file.replace(old_path,new_path).replace(lastest_file_name,new_file_name)
    shutil.copy(lastest_file,new_file)
    
def get_subfolders(folder_path):
    subfolder = [str(i) for i in pathlib.Path(folder_path).iterdir() if i.is_dir()]
    
    return subfolder

def get_files(folder_path, file_type='',contains=''):
    files = [str(i) for i in pathlib.Path(folder_path).iterdir() if not i.is_dir() and file_type in str(i) and contains in str(i)]
    
    return files

def get_all_files(folder_path,file_type='',contains='',include_path=True):
    filelist = []

    for root, dir, files in os.walk(folder_path):
        for file in files:
            if str(file).endswith(file_type) and contains in str(file) and include_path: 
                filelist.append(os.path.join(root,file))

            elif str(file).endswith(file_type) and contains in str(file):
                filelist.append(file)
                
    return filelist

def is_file_open(file_path):
    try:
        with open(file_path, 'r+') as f:
            print('file is closed, proceed to write')
    except PermissionError:
        print('file is open, close it and try again')

def get_downloads_folder(downloads_folder_name='Downloads'):
    downloads_folder = os.path.join(os.path.expanduser('~'), downloads_folder_name)
    return downloads_folder

def detect_file_download(download_path=None,tries=50,wait=1):
    if download_path is None: download_path = get_downloads_folder()
    tries_count = 0
    while True and tries_count <= tries:
        time.sleep(wait)
        if len(get_files(download_path)) > 0: break
        else: tries_count += 1

def detect_file_download_with_criteria(folder_path: str=None,file_type='',contains='',tries=50, wait=5):
    if folder_path is None: folder_path = get_downloads_folder()

    def is_file_downloaded():
        return isinstance(get_last_file_name(folder_path, extension=True, file_type=file_type, contains=contains), str)

    tries_count = 0
    while tries_count <= tries:
        if is_file_downloaded():
            return True
        time.sleep(wait)
        tries_count += 1

    print('File was not downloaded!')
    return False

def adding_prefix_to_files(file_path: str=None, file_type: str='', contains: str='',prefix: str=''):
    if file_path is None: file_path = get_downloads_folder()

    list_of_files = [str(i) for i in pathlib.Path(file_path).iterdir() if not i.is_dir() and i.endswith(file_type) and contains in str(i)]
    for file in list_of_files:
        file_oldname = file.replace(file_path + "\\","")
        file_newname = prefix + file.replace(file_path + "\\","")
        file_new = file.replace(file_oldname,file_newname)
        os.rename(file,file_new)
    print('Done!')

def remove_files_by_date(folder_path: str, cutoff_date, comparison, include_subs: bool=False):
    for root, directories, files in os.walk(folder_path):
        if not include_subs:
            directories.clear()
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_creation_time = datetime.date.fromtimestamp(os.path.getctime(file_path))
                if (comparison == 'greater_or_equal' and file_creation_time >= cutoff_date) or \
                   (comparison == 'greater' and file_creation_time > cutoff_date) or \
                   (comparison == 'less_or_equal' and file_creation_time <= cutoff_date) or \
                   (comparison == 'less' and file_creation_time < cutoff_date) or \
                   (comparison == 'equal' and file_creation_time == cutoff_date):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

def get_creation_date(file_path: str):
    timestamp = os.path.getctime(file_path)
    creation_date = datetime.datetime.fromtimestamp(timestamp)
    return creation_date

def get_modified_date(file_path: str):
    timestamp = os.path.getmtime(file_path)
    modified_date = datetime.datetime.fromtimestamp(timestamp)
    return modified_date

def get_access_date(file_path: str):
    timestamp = os.path.getatime(file_path)
    access_date = datetime.datetime.fromtimestamp(timestamp)
    return access_date

def get_file_size(file_path: str,size: str='default'):
    if size == 'default': file_size = os.path.getsize(file_path)
    elif size == 'kb': file_size = os.path.getsize(file_path) / 1024
    elif size == 'mb': file_size = os.path.getsize(file_path) / (1024 * 1024)
    elif size == 'gb': file_size = os.path.getsize(file_path) / (1024 * 1024 * 1024)
    else: print('Size not found!'); file_size = None
    
    return file_size

def get_file_information(file_path: str):
    file_name = get_file_name(file_path)
    file_extension = get_file_extension(file_path)
    file_size = get_file_size(file_path)
    creation_date = get_creation_date(file_path)
    modified_date = get_modified_date(file_path)
    access_date = get_access_date(file_path)
    file_information = {
        'file_name':file_name,
        'file_extension':file_extension,
        'file_size':file_size,
        'creation_date':creation_date,
        'modified_date':modified_date,
        'access_date':access_date}
    
    return file_information

def clean_folder(folder_path: str, file_type: str='',contains: str=''):
    # Clean the download folder
    files_in_actual_folder = get_files(folder_path,file_type=file_type,contains=contains)
    for file in files_in_actual_folder:
        os.remove(file)

def check_file_type(file: str, file_types: tuple[str]):
    """
    Check if the file is of a certain type.
    """
    return file.lower().endswith(file_types)

def get_local_sharepoint_path(sharepoint_site, raw_adress):
    sharepoint_local_folder = os.path.expanduser('~/MFP Michelin')
    if raw_adress.startswith('/'):
        raw_adress = raw_adress[1:]
    for folder in os.listdir(sharepoint_local_folder):
        site = folder.split(' - ')[0]
        if sharepoint_site == site or sharepoint_site == folder:
            sharepoint_site_folder = folder
            break
    return os.path.join(sharepoint_local_folder, sharepoint_site_folder, raw_adress)

