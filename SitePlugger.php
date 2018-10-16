<?php

namespace Scanner;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\BadResponseException;
use GuzzleHttp\Exception\ClientException;
use GuzzleHttp\Exception\ConnectException;
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Exception\ServerException;
use GuzzleHttp\Exception\TooManyRedirectsException;

require 'vendor/autoload.php';


class SitePlugger {

    public $client;
    public $response;
    
    //full URL of site to scan
    public $base_site = "";
    //relative path of writable directory
    public $save_directory = "";
    public $file_to_save = null;
    
    //Array containing all scanned URL's
    public $all_urls = array();
    //All URL's written to log file
    public $logged_urls = array();
    //URL paths that have to be skipped
    public $skip_path_array = array();
    
    //Enable/ Disable file save
    public $save_files = false;
    //Save file extention
    public $save_ext = ".html";
    
    private $log_file;
    //Log file name
    private $log_file_name = "log_.txt";
    

    public function __construct() {
        error_reporting(E_ALL);
        ini_set('display_errors', 1);

        $this->client = new Client();
        $this->log_file = fopen($this->log_file_name, "a");
        $this->logged_urls = $this->read_log_lines();
    }
    
    public function __destruct() {
        fclose($this->log_file);
    }

    function setSave_directory($save_directory) {
        $this->save_directory = getcwd() ."/". $save_directory;
        
        if($this->folder_exist($this->save_directory)){    
            if(!mkdir($this->save_directory,0777, true)){
                echo "\n Error creating folder:$this->save_directory";
                exit();
            }else {
                echo "\n Created folder:$this->save_directory";
            }
        }else{
            echo "\n  Folder already exists: $this->save_directory";
        }
    }

            
    public function make_simple_get($url){
        try {
            
            $this->response = $this->client->request('GET', $url);
            
            
        } catch (ClientException $ex) {
            var_dump($ex->getMessage());
        } catch (ConnectException $ex) {
            var_dump($ex->getMessage());
        } catch (BadResponseException $ex) {
            var_dump($ex->getMessage());
        } catch (RequestException $ex) {
            var_dump($ex->getMessage());
        } catch (TooManyRedirectsException $ex) {
            var_dump($ex->getMessage());
        } catch (ServerException $ex) {
            var_dump($ex->getMessage());
        }
    }
    public function status_code(){
        return $this->response->getStatusCode();
    }
    public function get_body(){
        return $this->response->getBody();
    }
    
    private function folder_exist($directory){
        if(!file_exists($directory)){
            if(!is_dir($directory)){
                return true;
            } 
            else{
                return false;
            }
        }
        else{
            return false;
        }
    }

    private function extract_img($content){
        $pattern = '/src=\"(.+)\"|src=\'(.+)\'/';
        
        $uniq_array =array();
        if (preg_match_all($pattern, $content, $matches)){
            
            foreach ($matches as $exact_matches){
                foreach ($exact_matches as $i =>  $match) {
                    $match = substr($match, 0,-1);

                    if(strpos($match, '"') > 0){
                        $match = substr($match, 0, strpos($match, '"'));
                    }
                    if(strpos($match, "'") > 0){
                        $match = substr($match, 0, strpos($match, "'"));
                    }    
                    if(strpos($match, $this->base_site)===0){
                        $uniq_array[] = trim($match, "/");
                    }
                }
            }
            
        } else {
            echo "\n Error 2";
        }
        
        return array_unique($uniq_array);        

    }
    private function extract_hrefs($content){
        $pattern = '/href=\"(.+)\"|value=\"(.+)\"|href=\'(.+)\'|value=\'(.+)\'/';
        
        $uniq_array =array();
        if (preg_match_all($pattern, $content, $matches)){
            
            
            foreach ($matches as $exact_matches){
                foreach ($exact_matches as $i =>  $match) {
                    $match = substr($match, 0,-1);

                    if(strpos($match, '"') > 0){
                        $match = substr($match, 0, strpos($match, '"'));
                    }
                    if(strpos($match, "'") > 0){
                        $match = substr($match, 0, strpos($match, "'"));
                    }    
                    if(strpos($match, $this->base_site)===0){
                        $link_to_test = trim($match, "/");
                        
                        $link_parsed = parse_url($link_to_test);
                        if(!isset($link_parsed['query']) && !isset($link_parsed['fragment'])){
                            
                            if (isset($link_parsed['path'])) {
                                $link_path = $link_parsed['path'];
                                $link_path = explode("/", $link_path);

                                if (!in_array($link_path[count($link_path) - 1], $this->skip_path_array)) {
                                    $uniq_array[] = $link_to_test;
                                }
                            }
                        }
                    }
                }
            }
            
        } else {
            echo "\n Error 2";
        }
        
        return array_unique($uniq_array);        

    }

    private function scan_pages($page_url, $deep = 0){
        echo "\n rec=>".$deep; 
//        sleep(2);
        
        echo "\n Page={$page_url}";
        
        $this->make_simple_get($page_url);
        
        $status_code = $this->status_code();
        
        echo "\n Status Code : $status_code";
        if($status_code == 200) {
            $page_content = $this->get_body();
            
            if($this->save_files === true){
                $this->save_file_and_path($page_url, $page_content);
            }
            
            $page_links = $this->extract_hrefs($page_content);
//            $image_links = $this->extract_img($page_content);
            
            echo "\n found pages=";var_dump(count($page_links));
            foreach ($page_links as $j => $page_link){
                
                if(!in_array($page_link, $this->all_urls) && 
                        !in_array($page_link, $this->logged_urls) ){
                    
                    $this->write_log_line($page_link);
                    $this->all_urls[] = $page_link;
                    $this->scan_pages($page_link, ++$deep);
                } else {
                    echo "\n Skipped: {$page_link}";
                }
            }
            echo "\n unique=";var_dump(count($this->all_urls));
        }else {
            echo "\n Error 1-> {$status_code}";
        }
    }

    public function run_plugger(){
        $this->scan_pages($this->base_site, 0);

    }
    
    public function write_log_line($link){
        fwrite($this->log_file, $link. "\n");
    }
    
    public function read_log_lines(){
        $read = fopen($this->log_file_name, "r");
        $status = fread($read, filesize($this->log_file_name));
        if($status != false){
            fclose($read);
            return array_unique(explode("\n", $status));
        }else {
            echo "\n no log exist!!!";
            return [];
        }
        
    }

    public function save_file_and_path($url, $content){
        $parsed_url = parse_url($url);

        if(isset($parsed_url['path'])) {
            $url_path = trim($parsed_url['path'],"/");
            $url_path = explode("/", $url_path);
            
            if(count($url_path) > 1){
                $file_name = array_pop($url_path);
                
                $rest_folder_path = implode("/", $url_path);
                $rest_folder_path = $this->save_directory . "/". $rest_folder_path;
                
                if($this->folder_exist($rest_folder_path)){
                    if(!mkdir($rest_folder_path,0777, true)){
                        echo "\n Error creating folder: {$rest_folder_path}";
                    }else {
                        echo "\n Success creating folder: {$rest_folder_path}";
                    }
                }else{
                    echo "\n  Folder already exists: $this->save_directory";
//                    exit;
                }
            }else {
                $file_name = trim($url_path[0])!="" ? $url_path[0] : "index--not-home";
                $rest_folder_path = $this->save_directory . "/";
            }
            
            //save file here
            $this->save_file($rest_folder_path . "/", $file_name, $content);
        }else {
            $this->save_file($this->save_directory . "/", "index", $content);
        }
    }
    
    public function save_file($uri,$filename,$content){
        $_local_path_file = $uri . $filename. $this->save_ext;
        $file_save = fopen($_local_path_file, "w+");
    
        if(!fwrite($file_save, $content)){
            echo "\n file save error: {$_local_path_file}";
        }else {
            echo "\n file save success: {$_local_path_file}";
        }
        
        fclose($file_save);
    }
    
}