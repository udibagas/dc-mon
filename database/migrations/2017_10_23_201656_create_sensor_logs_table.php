<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateSensorLogsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('sensor_logs', function (Blueprint $table) {
            $table->increments('id');
            $table->decimal('suhu_depan')->nullable();
            $table->decimal('suhu_belakang')->nullable();
            $table->decimal('lembab_depan')->nullable();
            $table->decimal('lembab_belakang')->nullable();
            $table->decimal('gas_depan')->nullable();
            $table->decimal('gas_belakang')->nullable();
            $table->boolean('pintu_depan')->nullable()->default(1);
            $table->boolean('pintu_belakang')->nullable()->default(1);
            $table->decimal('arus_input_ets')->nullable();
            $table->decimal('arus_input_ups')->nullable();
            $table->boolean('fan')->default(1);
            $table->boolean('compressor')->default(0);
            $table->boolean('hipressure')->default(0);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('sensor_logs');
    }
}
