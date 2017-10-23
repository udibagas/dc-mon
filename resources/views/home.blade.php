@extends('layouts.app')

@section('content')
<div class="container-fluid">
    <div class="row">
        @foreach ($gauges as $key => $label)
        <div class="col-md-3">
            <div id="gauge_{{$key}}" style="height:250px;">

            </div>
        </div>
        @endforeach
    </div>
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

    @foreach ($gauges as $key => $label)

    var series = [{
        type: 'gauge',
        min: 0,
        max: {{$key == "suhu_depan" || $key == "suhu_belakang" ? 40 : 100}},
        axisLine: {
            show: true,
            lineStyle: {
                width: 5,
                color: [
                    [{{$key == "suhu_depan" || $key == "suhu_belakang" ? 16/40 : 30/100}}, '#ff4500'],
                    [{{$key == "suhu_depan" || $key == "suhu_belakang" ? 18/40 : 40/100}},'orange'],
                    [{{$key == "suhu_depan" || $key == "suhu_belakang" ? 22/40 : 50/100}}, 'green'],
                    [{{$key == "suhu_depan" || $key == "suhu_belakang" ? 24/40 : 60/100}}, 'orange'],
                    [1, '#ff4500']
                ],
            }
        },
        axisLabel: {
            color : '#fff',
            fontSize: 9
        },
        axisTick: {
            show : false
        },
        splitLine: {
            show: false,
            length: 3,
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
            formatter: '{value}{{$key == "suhu_depan" || $key == "suhu_belakang" ? "C" : "%"}}',
            textStyle: {
                color: 'auto',
                fontSize: 15
            }
        },
        data: [{value: 0, name: ''}]
    }];

    var gauge_{{$key}} = echarts.init(document.getElementById('gauge_{{$key}}'));
    gauge_{{$key}}.setOption({series:series});

    @endforeach

    setInterval(function() {
        $.get('{{url("/api/sensorLog")}}', function(j) {
            @foreach ($gauges as $key => $label)
            gauge_{{$key}}.setOption({
                series: {
                    data:[{value:j.{{$key}}, name:'{{$label}}'}]
                }
            });
            @endforeach
        }, 'json');
    }, 3000);

</script>


@endpush
