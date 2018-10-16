<?php
require 'SitePlugger.php';


use Scanner\SitePlugger;


/**
 * Works only for Absolute URLs
 *
 * ToDo: save relative paths & files
 * Todo: save all image/css/js assets too.
 */

$scanner = new SitePlugger();
$scanner->base_site = "https://example.wordpress.com";
$scanner->replace_site = "https://example.com";



$scanner->save_ext = ".html";
$scanner->skip_path_array = ['feed','amp'];

$scanner->save_files = false;
$scanner->replace_domain_in_file = true;

$scanner->setSave_directory("example.com");

$scanner->save_bucket_s3 = "example.com";



// $scanner->run_plugger("scan_pages");
// $scanner->run_plugger("logger_save");
$scanner->run_plugger("save_2_s3");


//var_dump($scanner->all_urls);





?>
