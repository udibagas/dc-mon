<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Log extends Model
{
    protected $fillable = ['sensor_id', 'param_id', 'value'];

    public function sensor() {
        return $this->belongsTo(Sensor::class);
    }

    public function param() {
        return $this->belongsTo(Param::class);
    }
}
