<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class SensorLog extends Model
{
    protected $fillable = [
        'suhu_depan', 'suhu_belakang', 'lembab_depan', 'lembab_belakang',
        'gas_depan', 'gas_belakang', 'pintu_depan', 'pintu_belakang',
        'arus_input_ets', 'arus_input_ups', 'fan', 'compressor', 'hipressure'
    ];
}
