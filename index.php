<?php
require 'SitePlugger.php';


use Scanner\SitePlugger;


/**
 * Works only for Absolute URLs
 * 
 * ToDo: save relative paths & files
 * Todo: save pages to folders
 * Todo: replace main domain name...in files
 * Todo: save all image/css/js assets too.
 */

$scanner = new SitePlugger();
$scanner->base_site = "https://example.com";



$scanner->save_ext = ".html";
$scanner->skip_path_array = ['feed','amp'];
$scanner->save_files = false;
$scanner->setSave_directory("example.com");

$scanner->run_plugger();


var_dump($scanner->all_urls);





?>