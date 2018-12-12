import os
import re
import json
import urllib
import requests


class Siteplugger:
    'Main SitePlugger class'

    client = 0
    response = 0

    #full URL of site to scan
    base_site = ""
    replace_site = ""

    #relative path of writable directory
    save_directory = ""
    save_bucket_s3 = ""
    s3_prefix = ""
    s3_region = ""

    file_to_save = 0

    # Array containing all scanned URL's
    all_urls = []

    # All URL's written to log file
    logged_urls = []

    # URL paths that have to be skipped
    skip_path_array = []

    # Enable/ Disable file save
    save_files = False
    replace_domain_in_file = False

    # Save file extention
    save_ext = ".html"
    log_file = 0

    # Log file name
    log_file_name = "scanner_log_.txt"
    plugin_path = ""


    def __init__(self):
        self.plugin_path =  os.getcwd() + "/site-plugger/"

    def __del__(self):
        if self.log_file :
            self.log_file.close()

    def js_op(self,msg = [],error = False):
        msg_flg = []
        if error == False :
            msg_flg.append('False')
        else:
            msg_flg.append('True')

        msg_flg.append(msg)

        print (json.dumps(msg_flg))
        exit

    def setSave_directory(self,save_directory) :
        save_directory = self.plugin_path + save_directory

        print(save_directory)

        if self.folder_exist( save_directory ):

            if os.mkdir(save_directory,777) :
                self.js_op(["error" "Error creating folder:self.save_directory"], True)
                exit
            else :
                print("\n Created folder:self.save_directory")

        else:
            print("\n  Folder already exists:1: self.save_directory")

    def folder_exist(self, directory):
        exist = os.path.isdir(directory)
        return exist

    def isset(variable):
        return variable in locals() or variable in globals()

    def extract_img(self, content):
        pattern = '/src=\"(.+)\"|src=\'(.+)\'/'

        uniq_array = []
        matches = re.finditer(pattern, content)
        if len(matches):

            for exact_matches in matches:
                for match in exact_matches:
                    match = match.find(match, -1)

                    if match.find('"') > 0:
                        match = match.find(match.find('"'))

                    if match.find("'") > 0:
                        match = match.find(match.find("'"))

                    if match.find(self.base_site) == 0:
                        uniq_array.append(match.strip("/"))
                    else:
                        print("\n Error 2")

        return list(set(uniq_array))

    def extract_hrefs(self, content):

        pattern = '/href=\"(.+)\"|value=\"(.+)\"|href=\'(.+)\'|value=\'(.+)\'/'

        uniq_array = []
        matches = re.finditer(pattern, content)

        print(matches)
        # if len(matches):
        if 1:

            for exact_matches in matches:
                matchx = []
                matchx.append(exact_matches.group(0))
                matchx.append(exact_matches.group(1))
                matchx.append(exact_matches.group(2))
                matchx.append(exact_matches.group(3))
                matchx.append(exact_matches.group(4))

                for match in matchx:
                    if match is not None and match is not int:
                        match = match.find(match, -1)

                        if match.find('"') > 0:
                            match = match.find(match, 0, match.find('"'))

                        if match.find("'") > 0:
                            match = match.find(match, 0, match.find("'"))

                        if match.find(self.base_site) == 0:
                            link_to_test = match.strip("/")

                            link_parsed = urllib.parse(link_to_test)
                            if  not link_parsed['query'] and not link_parsed['fragment']:

                                if not link_parsed['path']:
                                    link_path = link_parsed['path']
                                    link_path = link_path.split("/")

                                    if link_path[len(link_path) - 1] not in  self.skip_path_array:
                                        uniq_array.append(link_to_test)

        else:
            print("\n Error 4")

        return list(set(uniq_array))

    def replace_domain(content):
                r_content = re.sub("#(self.base_site)#", "self.replace_site", content)

                if r_content.length > 0:
                    content = r_content
                    print("\n replace = done")
                else:
                    print("\n no replaced")

                return content

    def save_file_and_path(self,url, content):
        parsed_url = urllib.parse(url)

        if not parsed_url['path'] not in parsed_url :
            url_path = parsed_url['path'].strip("/")
            url_path = url_path.split("/",-1)

            if len(url_path) > 1:
                file_name = url_path.pop()

                rest_folder_path = "/".join( url_path)
                rest_folder_path = self.save_directory + "/" + rest_folder_path

                if self.folder_exist(rest_folder_path):

                    if not os.mkdir(rest_folder_path,777):
                        print("\n Error creating folder: :rest_folder_path")
                    else :
                        print("\n Success creating folder: :rest_folder_path")

                else:
                    print("\n  Folder already exists:2: self.save_directory")
                    exit

            else :
                if url_path[0] == " ":
                    file_name =  url_path[0]
                else:
                    file_name =  "index--not-home"

                rest_folder_path = self.save_directory + "/"


            # save file here
            self.save_file(rest_folder_path + "/", file_name, content)
        else :
            self.save_file(self.save_directory + "/", "index", content)


#
    def save_file(self,uri,filename,content):
        _local_path_file = uri + filename + self.save_ext
        file_save = open(_local_path_file, "w")

        print("\n len=" + len(content))

        if not file_save.write(self,content):
            print("\n file save error: :_local_path_file")
        else :
            print("\n file save success: :_local_path_file")

        file_save.close()


    def run_plugger(self,mode):
        if mode == "scan_pages":
            self.client = requests
            self.log_file = open(self.plugin_path + self.log_file_name, "w")
            self.logged_urls = self.read_log_lines()

            self.scan_pages(self.base_site, 0)

        elif mode == "logger_save":
            self.client = requests
            self.log_file = open(self.plugin_path + self.log_file_name, "w")
            self.logged_urls = self.read_log_lines()

            self.logger_save()


        elif mode == "single_save":
            self.client = requests
            self.log_file = open(self.plugin_path + self.log_file_name, "a")


            # case "save_2_s3":
            #     self.write_to_s3_bucket()
            # break




    def write_log_line(self,link):
        self.log_file.write(link + "\n")


    def read_log_lines(self,show_error = True):
        readfp = open(self.plugin_path + self.log_file_name, "r")
        if os.path.getsize(self.plugin_path + self.log_file_name) > 0:
            log_file_size =  os.path.getsize(self.plugin_path . self.log_file_name)
        else:
            log_file_size = 0

        status = readfp.read(log_file_size)
        if status != False:
            readfp.close()
            allreadline = status.split("\n")

            if allreadline is [] :
                return list(set(allreadline))

            else :
                if (show_error == True) :
                    self.js_op([ "no file log exist!!!"], True)

            return []

        else :
            if show_error == True:
                self.js_op(["error" "no file log exist!!!"],True)

        return []


    def scan_pages(self,page_url, deep = 0) :

        print("\n rec=>" , deep)
        # sleep(rand(1,2))

        print("\n Page=" +page_url)

        self.make_simple_get(page_url)

        status_code = self.status_code()

        print("\n Status Code : ",status_code)
        if status_code == 200  :
            page_content = self.get_body()

            if self.save_files == True:

                if self.replace_domain_in_file == True :
                    page_content = self.replace_domain(page_content)

                print (page_content)
                self.save_file_and_path(page_url, page_content)

            page_links = self.extract_hrefs(page_content)
            # image_links = self.extract_img(page_content)

            print( "\n found pages=")
            print(len(page_links))
            for page_link in page_links :

                if not page_link in self.all_urls  and not page_link in self.logged_urls:

                    self.write_log_line(page_link)
                    self.all_urls.append(page_link)
                    deep += 1
                    self.scan_pages(page_link, deep)

                else :
                    print("\n Skipped: :page_link")


            print("\n unique=")
            print(len(self.all_urls))
            if len(self.all_urls) == 0 :
                self.js_op(["success" "Scanning Complete"],False)

        else :
            self.js_op(["error" "Error 1-> :status_code"],True)



    def single_saver(self, line = ""):
        self.make_simple_get(line)
        content =  self.get_body()

        if self.replace_domain_in_file == True :
          content = self.replace_domain(content)

        self.save_file_and_path(line, content)

        return True
        #  TODO: sent back failure too

    def logger_save(self):
        log_lines = self.read_log_lines()

        if len(log_lines) > 0 :
            for line in log_lines  :
                self.make_simple_get(line)
                content =  self.get_body()

                if self.replace_domain_in_file == True:
                    content = self.replace_domain(content)

                self.save_file_and_path(line, content)
        else :
            self.js_op(["error" "Log file empty!!"],True)


    def make_simple_get(self,url):
            self.response = self.client.request("GET",url)

         # catch ClientException  :
         #    self.js_op(["error"  ex->getMessage()],True)
         # catch (ConnectException ex) :
         #    self.js_op(["error"=> ex->getMessage()],True)
         # catch (BadResponseException ex) :
         #    self.js_op(["error"=> ex->getMessage()],True)
         # catch (RequestException ex) :
         #    self.js_op(["error"=> ex->getMessage()],True)
         # catch (TooManyRedirectsException ex) :
         #    self.js_op(["error"=> ex->getMessage()],True)
         # catch (ServerException ex) :
         #    self.js_op(["error"=> ex->getMessage()],Truematches)



    def status_code(self):
        if self.response:
            return self.response.status_code
        else :
            return False



    def get_body(self):
        return self.response.content



#     public function write_to_s3_bucket(create_bucket = false) :
#
#         try :
#             provider = CredentialProvider::defaultProvider()
#
#             s3Client = new S3Client([
#                 'region' => self.s3_region,
#                 'version' => '2006-03-01',
#                 'credentials' => provider
#             ])
#
#             buckets = s3Client->listBuckets()
#
#             if(!in_array(self.save_bucket_s3, buckets['Buckets'])):
#                 echo "\n Bucket not exits --:self.save_bucket_s3 !!"
#
#                 if(isset(create_bucket)):
#                     //Creating S3 Bucket
#                     echo "\n creating Bucket -- :self.save_bucket_s3"
#                     result = s3Client->createBucket([
#                         'Bucket' => self.save_bucket_s3,
#                     ])
#                 else:
#                     exit
#                 
#             
#             s3Client->uploadDirectory(
#                     self.save_directory,
#                     self.save_bucket_s3,
#                     self.s3_prefix ,
#                     array(
#                        // 'params' => array('ACL' => 'public-read'),
#                        // 'concurrency' => 10,
#                         'debug' => true
#                     )
#                 )
#          catch (AwsException ex) :
#             self.js_op(["error"=> ex->getMessage()],true)
#          catch (CredentialsException ex) :
#             self.js_op(["error"=> ex->getMessage()],true)
