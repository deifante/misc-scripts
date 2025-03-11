<?php
$curl_handle = curl_init("https://export.highcharts.com");
$form_data = array(
    'options' => "{xAxis: {categories: ['Jan', 'Feb', 'Mar', 'Avril']},series: [{data: [29.9, 71.5, 106.4, 141.3]}]}",
    'type' => 'image/png'
);

curl_setopt($curl_handle, CURLOPT_VERBOSE, true);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl_handle, CURLOPT_POSTFIELDS, $form_data);
$image_data = curl_exec($curl_handle);
if (false !== $image_data) {
    $file_handle = fopen("lol.png", "w");
    $result = fwrite($file_handle, $image_data);
    fclose($file_handle);
}
curl_close($curl_handle);

echo "Done\n";