@extends('layouts.app')

@section('content')
<div class="container-fluid">
    @foreach ($params as $p)
    <h3>{{ $p->name }} <small>{{ $p->description }}</small></h3>
    <hr>
    <div class="row">
        <div class="col-md-6">
            <div id="chart{{$p->id}}" style="height:330px;"></div>
        </div>

        <div class="col-md-6">
            <div class="row">
                @foreach ($p->sensors as $s)
                <div class="col-md-6 text-center">
                    <div id="gauge{{$s->id}}-{{$p->id}}" style="height:300px;">

                    </div>
                    <div style="font-size:20px;">
                        {{ $s->code }} ({{ $s->position }})
                    </div>
                </div>
                @endforeach
            </div>
        </div>
    </div>
    @endforeach

</div>
@endsection

@push('script')

<script type="text/javascript">


    var getClock = function(date) {
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
        d = date.getDate();
        m = date.getMonth();
        y = date.getFullYear();
        h = date.getHours();
        i = date.getMinutes();
        s = date.getSeconds();

        clock = d + ' ' + months[m] + ' ' + y + ' ' + h + ':' + i + ':' + s;
        return clock;
    }

    setInterval(function() {
        date = new Date();
        $('#clock').html(getClock(date));
    }, 1000);

    @foreach ($params as $p)
        var myChart{{$p->id}} = echarts.init(document.getElementById('chart{{$p->id}}'));
        myChart{{$p->id}}.setOption({
            backgroundColor: '#333',
            tooltip: {},
            xAxis: {
                data: {{json_encode(range(1,36), JSON_NUMERIC_CHECK)}},
                axisLine : {
                    show: true,
                    lineStyle: {
                        color: '#fff',
                    }
               },
                axisTick : {
                    show:true,
                    length: 10,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                axisLabel : {
                    show:true,
                    textStyle: {
                        color: '#fff',
                    }
                },
            },
            yAxis: {
                axisLine : {
                    show: true,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                axisTick : {
                    show:true,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                axisLabel : {
                    show:true,
                    formatter: '{value}{{$p->unit}}',
                    textStyle: {
                        color: '#fff',
                    }
                },
                splitLine : {
                    show:true,
                    lineStyle: {
                        color: '#fff',
                        type: 'dotted',
                    }
                },
                splitArea : {
                    show: true,
                    areaStyle:{
                        color:['rgba(205,92,92,0.3)','rgba(255,215,0,0.3)']
                    }
                }
            },
            series: [{
                name: 'tren',
                type: 'line',
                data: [0]
            }]
        });

        @foreach ($p->sensors as $s)
        var series = [{
            type: 'gauge',
            min: {{$p->gauge_start}},
            max: {{$p->gauge_end}},
            axisLine: {
                show: true,
                lineStyle: {
                    width: 15,
                    color: [
                        [{{$p->min_value/$p->gauge_end}}, '#ff4500'],
                        [{{$p->lo_value/$p->gauge_end}},'orange'],
                        [{{$p->hi_value/$p->gauge_end}}, 'green'],
                        [{{$p->max_value/$p->gauge_end}}, 'orange'],
                        [1, '#ff4500']
                    ],
                }
            },
            axisLabel: {
                color : '#fff',
            },
            axisTick: {
                show : false
            },
            splitLine: {
                show: false,
                length: 18,
            },
            pointer: {
                length: '65%',
                width: 3,
                color: 'auto'
            },
            title: {
                show: true,
                offsetCenter: ['0%', 90],
                textStyle: {
                    color: '#999',
                    fontSize: 15
                }
            },
            detail: {
                show: true,
                formatter: '{value}{{$p->unit}}',
                textStyle: {
                    color: 'auto',
                    fontSize: 25
                }
            },
            data: [{value: 23, name: ''}]
        }];

        var gauge{{$s->id}}_{{$p->id}} = echarts.init(document.getElementById('gauge{{$s->id}}-{{$p->id}}'));
        gauge{{$s->id}}_{{$p->id}}.setOption({series:series});

        setInterval(function() {
            $.get('{{url("/log")}}', {chart: "gauge", param_id: {{$p->id}}, sensor_id: {{$s->id}}}, function(j) {
                gauge{{$s->id}}_{{$p->id}}.setOption({
                    series: {
                        data:[{value:j.value, name:'-'}]
                    }
                });
            }, 'json');
        }, 3000);

        @endforeach

    @endforeach

    setInterval(function() {
        $.get('{{url("/log")}}', function(j) {
            // untuk line chart
            @foreach ($params as $p)
                myChart{{$p->id}}.setOption({
                    series: [{
                        data: j.data,
                        name: 'tren',
                        type: 'line',
                        color: '#ddd'
                    }, {
                        data: j.data1,
                        name: 'tren',
                        type: 'line'
                    }]
                });
            @endforeach
        }, 'json');
    }, 3000);

</script>

@endpush
