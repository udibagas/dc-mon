<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddUnitOnParams extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('params', function (Blueprint $table) {
            $table->string('unit', 10);
            $table->decimal('min_value');
            $table->decimal('max_value');
            $table->decimal('lo_value');
            $table->decimal('hi_value');
            $table->decimal('gauge_start');
            $table->decimal('gauge_end');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('params', function (Blueprint $table) {
            $table->dropColumn(['unit', 'min_value', 'max_value', 'lo_value', 'hi_value']);
        });
    }
}
