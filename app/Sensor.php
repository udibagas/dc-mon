<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Sensor extends Model
{
    protected $fillable = ['interface', 'code', 'position'];

    public function params() {
        return $this->belongsToMany(Param::class, 'sensor_params');
    }
}
