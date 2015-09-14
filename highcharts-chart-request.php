<?php


$curl_handle = curl_init("https://export.highcharts.com");

$header = array();

$header []= "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8";
$header []= "accept-language:en-US,en;q=0.8";
$header []= "cache-control:no-cache";
$header []= "content-type:application/x-www-form-urlencoded";
$header []= "origin:http://localhost";
$header []= "pragma:no-cache";
$header []= "upgrade-insecure-requests:1";
//curl_setopt($curl_handle, CURLOPT_HEADER, 0);

curl_setopt($curl_handle, CURLOPT_POST, true);
curl_setopt($curl_handle, CURLOPT_USERAGENT, "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36");
curl_setopt($curl_handle, CURLOPT_REFERER, "referer:http://localhost/test-form.html");
curl_setopt($curl_handle, CURLOPT_ENCODING, "gzip, deflate");

curl_setopt($curl_handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);

$form_data = array(
    'options' => "{xAxis: {categories: ['Jan', 'Feb', 'Mar']},series: [{data: [29.9, 71.5, 106.4]}]}",
    'type' => 'image/png',
    'width' => null,
    'scale' => null,
    'constr' => 'Chart',
    'callback' => null
);

curl_setopt($curl_handle, CURLOPT_POSTFIELDS, $form_data);


curl_exec($curl_handle);
curl_close($curl_handle);
echo "Done\n";