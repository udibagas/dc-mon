<?php

use Illuminate\Database\Seeder;
use App\Sensor;
use App\Param;

class SensorParamSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $params = Param::all();
        $sensors = Sensor::all();

        foreach ($params as $p ) {
            foreach ($sensors as $s) {
                $p->sensors()->attach($s->id);
            }
        }
    }
}
