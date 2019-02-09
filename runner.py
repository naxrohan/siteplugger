import siteplugger
import sys
import json


def runner_handler(event, context):
    scanner = siteplugger.siteplugger

    scanner.base_site = "https://disciplesofhope.wordpress.com"
    scanner.replace_site = "https://disciplesofhope.com"

    scanner.save_ext = ".html"
    scanner.skip_path_array = ['feed', 'amp', 'xmlrpc.ph']

    scanner.save_files = False
    scanner.replace_domain_in_file = True

    scanner.set_save_directory(siteplugger.siteplugger(), "disciplesofhope.com")

    scanner.save_bucket_s3 = "disciplesofhope.com"
    scanner.save_directory = "disciplesofhope.com"
    scanner.s3_prefix = "testing"
    scanner.s3_region = "us-west-2"

    if len(event) > 0:

        if event['cmd'] == "--help":
            return {
                'message': "Options below: \n\n"
                           "scan_pages  - to scan for new pages in site.. \n"
                           "local_saver - to save new pages that are found.. \n"
                           "write_s3 - copy new files to s3 bucket.. \n"
            }
        elif event['cmd'] == "scan_pages":
            response = scanner.run_plugger(siteplugger.siteplugger(), "scan_pages")
            return {
                'message': json.dumps(response)
            }

        elif event['cmd'] == "local_saver":
            response = scanner.run_plugger(siteplugger.siteplugger(), "logger_save")
            return {
                'message': json.dumps(response)
            }

        elif event['cmd'] == "write_s3":
            response = scanner.run_plugger(siteplugger.siteplugger(), "save_2_s3")
            return {
                'message': json.dumps(response)
            }

        else:
            return sys.argv

    else:
        print "use --help"
        return "use --help"


# Local testing
print sys.argv
if len(sys.argv) > 1:
    event_local = {'cmd':  sys.argv[1]}
    local_re = runner_handler(event_local, " ")
    print local_re
