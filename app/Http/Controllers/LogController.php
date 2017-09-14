<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Log;
use App\Sensor;

class LogController extends Controller
{
    public function index(Request $request)
    {
        // untuk line
        // $data = Log::selectRaw('value, CONCAT(MINUTE(created_at), ":", SECOND(created_at))')->when($request->param_id, function($query) use ($request) {
        $data = Log::selectRaw('value')->when($request->param_id, function($query) use ($request) {
                    return $query->where('param_id', $request->param_id);
                })->when($request->sensor, function($query) use ($request) {
                    return $query->where('sensor', $request->sensor);
                })->latest()->take(36)->get()->toArray();

        $value = Log::select('value')->when($request->param_id, function($query) use ($request) {
                    return $query->where('param_id', $request->param_id);
                })->when($request->sensor, function($query) use ($request) {
                    return $query->where('sensor', $request->sensor);
                })->latest()->first();

        $ret = [
            'data' => array_reverse(array_flatten($data)),
            'data1' => array_flatten($data),
            'value' => $value ? $value->value : 0
        ];

        return json_encode($ret, JSON_NUMERIC_CHECK);

    }

    public function store()
    {
        $sensors = Sensor::all();

        foreach ($sensors as $s) {
            foreach ($s->params as $p) {
                Log::create([
                    'sensor_id' => $s->id,
                    'param_id' => $p->id,
                    'value' => mt_rand(16*10, 33*10)/10
                ]);
            }
        }
    }
}
