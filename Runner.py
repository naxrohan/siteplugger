import Siteplugger
import sys

scanner = Siteplugger.Siteplugger

scanner.base_site = "https://disciplesofhope.wordpress.com"
scanner.replace_site = "https://disciplesofhope.com"

scanner.save_ext = ".html"
scanner.skip_path_array = ['feed', 'amp', 'xmlrpc.ph']

scanner.save_files = False
scanner.replace_domain_in_file = True

scanner.set_save_directory(Siteplugger.Siteplugger(), "disciplesofhope.com")

scanner.save_bucket_s3 = "disciplesofhope.com"
scanner.save_directory = "disciplesofhope.com"
scanner.s3_prefix = "testing";
scanner.s3_region = "us-west-2";

print sys.argv[1]

if sys.argv[0] == "Runner.py":

# scanner.run_plugger(Siteplugger.Siteplugger(), "scan_pages");

# scanner.run_plugger(Siteplugger.Siteplugger(),"logger_save");

# scanner.run_plugger(Siteplugger.Siteplugger(),"save_2_s3");


# print(scanner.all_urls);


