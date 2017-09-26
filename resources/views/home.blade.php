@extends('layouts.app')

@section('content')
<div class="container-fluid">
    @foreach ($sensors as $s)
    <div class="panel panel-info" style="background-color:transparent;">
        <div class="panel-heading text-center">
            <span style="font-size:20px;">{{ strtoupper($s->position) }}</span>
        </div>
        <div class="panel-body">
            <div class="row">
                @foreach ($s->params as $p)
                <div class="col-md-4 text-center">
                    <div id="gauge{{$s->id}}-{{$p->id}}" style="height:350px;">
                        {{$p->name}}
                    </div>

                    <div class="alert alert-success text-center">
                        <span style="font-size:20px;">NORMAL</span>
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

    @foreach ($sensors as $s)
        @foreach ($s->params as $p)
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
                    fontSize: 30
                }
            },
            data: [{value: 0, name: ''}]
        }];

        var gauge{{$s->id}}_{{$p->id}} = echarts.init(document.getElementById('gauge{{$s->id}}-{{$p->id}}'));
        gauge{{$s->id}}_{{$p->id}}.setOption({series:series});

        setInterval(function() {
            $.get('{{url("/log")}}', {chart: "gauge", param_id: {{$p->id}}, sensor_id: {{$s->id}}}, function(j) {
                gauge{{$s->id}}_{{$p->id}}.setOption({
                    series: {
                        data:[{value:j.value, name:'{{strtoupper($p->name)}}'}]
                    }
                });
            }, 'json');
        }, 3000);

        @endforeach
    @endforeach
</script>

@endpush
