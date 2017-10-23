<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
// use App\Param;
// use App\Sensor;
use App\SensorLog;

class HomeController extends Controller
{
    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return view('home', [
            // 'params' => Param::all(),
            // 'sensors' => Sensor::all(),
            'log' => SensorLog::latest()->first(),
            'gauges' => [
                'suhu_depan' => 'SUHU DEPAN',
                'suhu_belakang' => 'SUHU BELAKANG',
                'lembab_depan' => 'LEMBAB DEPAN',
                'lembab_belakang' => 'LEMBAB BELAKANG',
            ],
            'buttons' => [
                'pintu_depan' => 'PINTU DEPAN',
                'pintu_belakang' => 'PINTU BELAKANG',
                'compressor' => 'COMPRESSOR',
                'fan' => 'FAN',
            ]
        ]);
    }
}
