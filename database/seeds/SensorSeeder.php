<?php

use Illuminate\Database\Seeder;
use App\Sensor;

class SensorSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        Sensor::create([
            'interface' => '/dev/tty/USB0',
            'code' => 'DC01-01',
            'position' => 'Left'
        ]);

        Sensor::create([
            'interface' => '/dev/tty/USB1',
            'code' => 'DC01-02',
            'position' => 'Right'
        ]);
    }
}
