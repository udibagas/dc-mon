<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Param;
use App\Sensor;

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
            'params' => Param::all(),
            'sensors' => Sensor::all(),
        ]);
    }
}
