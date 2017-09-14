<?php

use Illuminate\Database\Seeder;
use App\Param;

class ParamSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        Param::create([ 'name' => 'Suhu', 'description' => 'Suhu (C) dalam rak' ]);
        Param::create([ 'name' => 'Kelembaban', 'description' => 'Kelembaban (%) dalam rak' ]);
        Param::create([ 'name' => 'Gas', 'description' => 'Kadar gas (%) dalam rak' ]);
    }
}
