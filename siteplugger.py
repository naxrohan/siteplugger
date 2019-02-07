import os
import re
import json
import urlparse
import boto3
import zipfile
import datetime
from botocore.vendored import requests


class siteplugger:
    'Main SitePlugger class'

    client = 0
    response = 0

    # full URL of site to scan
    base_site = ""
    replace_site = ""

    # relative path of writable directory
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
    replace_domain_in_file = False

    # Save file extention
    save_ext = ".html"
    log_file = 0
    done_file = 0

    # Log file name
    log_file_name = "scanner_log_.txt"
    done_file_name = "done_log_.txt"
    plugin_path = ""

    # Set plugger folder
    local_dir = ""

    def __init__(self):
        # for local folder
        # self.plugin_path = os.getcwd() + "/" + self.local_dir
        # for lambda folder
        self.plugin_path = "/tmp/" + self.local_dir

    def __del__(self):
        if self.log_file :
            self.log_file.close()

    def js_op(self, msg=[], error=False):
        msg_flg = []
        if error == False :
            msg_flg.append('False')
        else:
            msg_flg.append('True')

        msg_flg.append(msg)

        print json.dumps(msg_flg)
        exit

    def set_save_directory(self, save_dir):
        save_directory = self.plugin_path + save_dir

        if not self.folder_exist(save_directory):
            print save_directory
            if os.mkdir(save_directory, 777):
                print "Error creating folder:", save_directory
                exit
            else:
                print("Created folder:", save_directory)

        else:
            print("Folder already exists:1:", save_directory)

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

        pattern = 'href=(["\'](.*?)["\'])|value=(["\'](.*?)["\'])'

        uniq_array = []
        # matches = re.finditer(pattern1, content)
        matches = re.finditer(pattern, content.content)

        # if len(matches):
        if 1:
            for exact_matches in matches:

                matchx = []
                matchx.append(exact_matches.group(0))
                matchx.append(exact_matches.group(1))
                matchx.append(exact_matches.group(2))
                # matchx.append(exact_matches.group(3))
                # matchx.append(exact_matches.group(4))

                # print(matchx)

                for match in matchx:
                    if match is not None and match is not int:
                        match = match[0:-1]

                        if match.find('"') is not -1:
                            match = match.find(match, 0, match.find('"'))

                        elif match.find("'") is not -1:
                            match = match.find(match, 0, match.find("'"))

                        if not isinstance(match,int):
                            # print(match)
                            if match.find(self.base_site) == 0:
                                link_to_test = match.strip("/")
                                # urlparse.urlparse()
                                link_parsed = urlparse.urlparse(link_to_test)
                                if link_parsed.query == "" and link_parsed.fragment == "":

                                    if link_parsed.path != "":
                                        link_path = link_parsed.path
                                        link_path = link_path.split("/")

                                        if link_path[len(link_path) - 1] not in  self.skip_path_array:
                                            uniq_array.append(link_to_test)

        else:
            print("\n Error 4")

        return list(set(uniq_array))

    def replace_domain(self, content_body):
        r_content = re.sub(self.base_site, self.replace_site, content_body)

        if len(r_content) > 0:
            content = r_content
            print("\n replace = done")
        else:
            print("\n no replaced")

        return content

    def save_file_and_path(self, url, content):
        parsed_url = urlparse.urlparse(url)

        if not parsed_url.path not in parsed_url:
            url_path = parsed_url.path.strip("/")
            url_path = url_path.split("/", -1)

            if len(url_path) > 1:
                file_name = url_path.pop()

                rest_folder_path = "/".join( url_path)
                rest_folder_path = self.plugin_path + self.save_directory + "/" + rest_folder_path

                if not self.folder_exist(rest_folder_path):

                    #Create Folder structure
                    os.makedirs(rest_folder_path)

                    if not os.path.exists(rest_folder_path):
                        print("Error creating folder:", rest_folder_path)
                    else:
                        print("Success creating folder:", rest_folder_path)

                else:
                    print("Folder already exists:2: ", self.save_directory)
                    exit

            else:
                if url_path[0] == " ":
                    file_name = url_path[0]
                else:
                    file_name = "index--not-home"

                rest_folder_path = self.plugin_path + self.save_directory + "/"

            #save file here
            self.save_file(rest_folder_path + "/", file_name, content)
            self.write_done_lines(url)
        else:
            self.save_file(self.plugin_path + self.save_directory + "/", "index", content)
            self.write_done_lines(url)

    def save_file(self, uri, filename, content):

        _local_path_file = uri + filename + self.save_ext

        if not os.path.isfile(_local_path_file):
            file_save = open(_local_path_file, "w")

            print("len=", len(content))

            if not file_save.write(content) :
                print("file save success:", _local_path_file)

            file_save.close()
        else:
            print("skip save,exists:", _local_path_file)

    def write_log_line(self,link):
        self.log_file.write(link + "\n")

    def write_done_lines(self,link):
        self.done_file.write(link + "\n")

    def read_log_lines(self,show_error=True,file_name="log_file_name"):

        final_log_path = self.plugin_path + file_name

        readfp = open(final_log_path, "r")

        if os.path.getsize(final_log_path) > 0:
            log_file_size = os.path.getsize(final_log_path)
        else:
            log_file_size = 0

        print (file_name + " log size=", log_file_size)

        log_content = readfp.read(log_file_size)

        if log_content != False:
            readfp.close()
            allreadline = log_content.split("\n")

            if allreadline is not []:
                return list(set(allreadline))
            else:
                print "no file log exist?"
                return []

        else:
            print "no file log exist!"

        return []

    def scan_pages(self,page_url, deep = 0) :

        print("\n rec=>", deep)
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

                # print (page_content)
                self.save_file_and_path(page_url, page_content)

            page_links = self.extract_hrefs(page_content)
            # image_links = self.extract_img(page_content)

            print("\n found pages=")
            print(len(page_links))
            for page_link in page_links :

                if not page_link in self.all_urls  and not page_link in self.logged_urls:

                    self.write_log_line(page_link)
                    self.all_urls.append(page_link)
                    deep += 1
                    self.scan_pages(page_link, deep)
                    break
                else:
                    print("\n Skipped: ", page_link)

            print("\n unique=")
            print(len(self.all_urls))
            if len(self.all_urls) == 0 :
                print  "Scanning Complete..."

        else:
            print "Error 1->",status_code

    def single_saver(self, line = ""):
        self.make_simple_get(line)
        content =  self.get_body()
        content = content.content

        if self.replace_domain_in_file == True :
          content = self.replace_domain(content)

        self.save_file_and_path(line, content)

        return True
        #  TODO: sent back failure too

    def logger_save(self):
        log_lines = self.read_log_lines(False,self.log_file_name)
        done_lines = self.read_log_lines(False,self.done_file_name)

        if len(log_lines) > 0:
            for line in log_lines:
                if line.strip(" ") != "":
                    line = line.strip(" ")
                    if not line in done_lines:
                        self.make_simple_get(line)
                        status_code = self.status_code()

                        print "code=", status_code

                        content = self.get_body()
                        content = content.content

                        if self.replace_domain_in_file == True:
                            content = self.replace_domain(content)

                        self.save_file_and_path(line, content)
                    else:
                        print "link already done:" + line
                else:
                    print "Blank line skipped"
        else:
            print"Log file empty!!"

    def make_simple_get(self, url):
        print "request_url=" + url
        try:
            self.response = self.client.request("GET", url)
        except requests.exceptions.RequestException as ex:
            print ex

    def status_code(self):
        if self.response:
            return self.response.status_code
        else:
            return False

    def get_body(self):
        print self.response
        return self.response

    def write_to_s3_bucket(self,create_bucket = False) :

        s3client = boto3.client('s3')

        list_buckets_resp = s3client.list_buckets()
        for bucket in list_buckets_resp['Buckets']:

            # print bucket

            if bucket['Name'] == self.save_bucket_s3:
                print('Bucket={} exists since={}'.format(bucket['Name'], bucket['CreationDate']))

                self.sync_to_s3(
                    self.plugin_path + self.save_directory,
                    self.s3_region,
                    self.save_bucket_s3
                )

            else:
                print "Bucket not exist: name=\n", self.save_bucket_s3

    def gzip_local_folder(self, path):
        # get current date
        now = datetime.datetime.now()
        zip_file_name = self.save_directory + "_" + now.strftime("%Y%m%d_%H%M") + '.zip'
        zipf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        # Done: add non root target dir to zip file

        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file))

        zipf.close()
        file_stats = os.stat(zip_file_name)

        print "Zip file created name={} size={}\n".format(zip_file_name, file_stats.st_size)
        # Todo: move zip to s3 bucket & un zip via lamda function to save on usage bandwidth

        return zip_file_name

    def sync_to_s3(self, target_dir, aws_region, bucket_name):

        # ====send compressed target folder
        to_zip_dir = self.local_dir + self.save_directory
        file_to_move = self.gzip_local_folder(to_zip_dir)

        all_files = [file_to_move]

        # ====Check existing files in s3
        # s3client = boto3.client('s3')
        # list_objects = s3client.list_objects(Bucket=self.save_bucket_s3 )
        # print "total objects=", len(list_objects['Contents'])
        # for s3files in list_objects['Contents']:
        #     print s3files['Key']
        #     print s3files['LastModified']
        #     print s3files['Size']
        #     print s3files['Name'] + "-->" + s3files['Key'] + "\n";

        # ====send full uncompressed target folder
        # if not os.path.isdir(target_dir):
        #     raise ValueError('target_dir %r not found.' % target_dir)
        # all_files = []
        # for root, dirs, files in os.walk(target_dir):
        #     all_files += [os.path.join(root, f) for f in files]

        s3_resource = boto3.resource('s3')
        for local_file in all_files:

            # ====get only file name from folder
            # filename = local_file.split(self.save_bucket_s3)

            filename = local_file
            print "moving file={}\n".format(filename)

            file_obj = s3_resource.Object(
                        bucket_name,
                        self.s3_prefix + "/" + filename
                    ).put(Body=open(local_file, 'rb'))
            print file_obj

        print "Total Local Files=", len(all_files)

    def run_plugger(self, mode):
        if mode == "scan_pages":
            self.client = requests
            self.log_file = open(self.plugin_path + self.log_file_name, "a")
            self.logged_urls = self.read_log_lines(False, self.log_file_name)

            self.scan_pages(self.base_site, 0)

        elif mode == "logger_save":
            self.client = requests
            self.log_file = open(self.plugin_path + self.log_file_name, "r")
            self.done_file = open(self.plugin_path + self.done_file_name, 'a')

            self.logger_save()

        elif mode == "single_save":
            self.client = requests
            self.log_file = open(self.plugin_path + self.log_file_name, "r")

        elif mode == "save_2_s3":
            self.write_to_s3_bucket()

