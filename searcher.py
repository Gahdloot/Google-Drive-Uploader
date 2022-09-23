from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Googleuploader:
    

    def __init__(self):
        '''
        gauth has a default property for credential which is 'client_secrets.json' which is filename the script expectes.
        {i tried to modify it in the auth module GoogleAuth class by creating getCred() class with a returnCred() method, but I wasnt confident about the implementation}
        so before running the code,   your Oauth credntials has to be renamed to 'client_secrets.json'
        and it has to be in the same directory as the python script
        '''
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        self.drive = drive

    def writeFile(self, filename,content):
        '''
        type(filename) : str
         extention of file must be appended e.g newfile.txt or newfile.json
        content of file : str
         content
        '''
        if isinstance(filename, str):
            pass
        else:
            filename = str(filename)
        if isinstance(content, str):
            pass
        else:
            content = str(content)
        file4 = self.drive.CreateFile({'title': filename})
        file4.SetContentString(content)
        file4.Upload()

    def uploadfile(self, filename):
        '''This accepts two type of files
        1. file that are in the same directory as it e.g picpicpictest.jpg
        2. and file with proper location e.g C:/User/appdata/file/text.txt
        the try bloock is meant to catch unicode error annd convert it to raw string before uploading the file

        '''
        if isinstance(filename, str):
            pass
        else:
            filename = str(filename)
        try:
            file1 = self.drive.CreateFile()
            file1.SetContentFile(filename)
        except SyntaxError:

            rawfilename = r'{}'.format(filename)
            filename = rawfilename.split("\\")
            file1 = self.drive.CreateFile({'title':filename[-1]})
        file1.Upload()


    def listOfFiles(self):
        '''
        For fetching list of all files and appending to a list
        '''

        FileList = []
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            file = {'id': file1['id'], 'title': file1['title']}
            FileList.append(file)
        return FileList

    def fileInDrive(self, title):
        '''this queries the api and search if the argument is in the google drive'''

        fil = False
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            if file1['title'] == title:
                fil = True
                break
        return True

    def download(self, title):
        '''to download a file
        1. I tried to check if the requested download exists by using  the fileInDrive method
        2. Download the file in to the working directory'''
        if isinstance(title, str):
            pass
        else:
            title = str(title)
        if self.fileInDrive(title):
            file = self.drive.CreateFile({'title': title})
            file.GetContentFile(title)