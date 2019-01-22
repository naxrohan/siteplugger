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

if len(sys.argv) > 1 and sys.argv[0] == "Runner.py":

    if sys.argv[1] == "--help":
        print "Runner.py ---help article \n\n Options below: \n\n" \
              "scan_pages  - to scan for new pages in site.. \n" \
              "local_saver - to save new pages that are found.. \n" \
              "write_s3    - copy new files to s3 bucket.. \n"
    elif sys.argv[1] == "scan_pages":
        scanner.run_plugger(Siteplugger.Siteplugger(), "scan_pages");

    elif sys.argv[1] == "local_saver":
        scanner.run_plugger(Siteplugger.Siteplugger(), "logger_save");

    elif sys.argv[1] == "write_s3":
        scanner.run_plugger(Siteplugger.Siteplugger(), "save_2_s3");

    else:
        print sys.argv

else:
    print "use --help"

    #Testing..
    scanner.run_plugger(Siteplugger.Siteplugger(), "save_2_s3");
