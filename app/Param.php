<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Param extends Model
{
    protected $fillable = ['name', 'description'];

    public function sensors() {
        return $this->belongsToMany(Sensor::class, 'sensor_params');
    }
}
