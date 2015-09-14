<?php
$curl_handle = curl_init("https://export.highcharts.com");
$form_data = array(
    'options' => "{xAxis: {categories: ['Jan', 'Feb', 'Mar', 'Apr']},series: [{data: [29.9, 71.5, 106.4, 141.3]}]}",
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