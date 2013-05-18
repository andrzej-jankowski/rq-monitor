var QueuesChart = {
    chart: null,

    updateChart: function(ticks, chartData) {
        QueuesChart.chart.xAxis[0].setCategories(ticks, false);
        QueuesChart.chart.series[0].setData(chartData, false);
        QueuesChart.chart.redraw();
    },

    init: function(ticks, chartData) {
        QueuesChart.chart = new Highcharts.Chart({
            chart: {
                type: 'column',
                renderTo: 'queues_chart'
            },
            title: {
                text: null
            },
            xAxis: {
                categories: ticks
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Jobs'
                },
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    enabled: false
                }
            },
            series: [{
                name: 'Current Jobs Count',
                data: chartData,
                dataLabels: {
                    enabled: true,
                    style: {
                        fontSize: '16px',
                        fontWeight: 'bold'
                    }
                }
            }],
            legend: {
                enabled: false
            }
        });
    }
}

var WorkersTable = {
    renderRow: function(worker) {
        return "<tr><td>" + worker.name  + "</td><td>" + worker.state +
               "</td><td>" + worker.queue_names + "</td></tr>";
    },

    updateTable: function(workers) {
        var html = "";
        for(var i = 0; i < workers.length; i++) {
            html += this.renderRow(workers[i]);
        }
        $("#workers_table tbody").html(html);
    }
}

var WebSocketUtils = {
    onOpen: function(evt) {
        // todo
    },

    onClose: function(evt) {
        // todo
    },

    onMessage: function(evt) {
        var data = JSON.parse(evt.data);
        var ticks = [];
        var values = [];
        for(var i = 0; i < data.queues.length; i++) {
            ticks.push(data.queues[i].name);
            values.push(data.queues[i].jobs_count);
        }
        QueuesChart.updateChart(ticks, values);
        WorkersTable.updateTable(data.workers);
    },

    onError: function(evt) {
        console.log(evt.data);
    },

    init: function() {
        var websocket = new WebSocket(
            "ws://" + window.location.host + "/websocket"
        );
        websocket.onopen = function(evt) { WebSocketUtils.onOpen(evt); };
        websocket.onclose = function(evt) { WebSocketUtils.onClose(evt); };
        websocket.onmessage = function(evt) { WebSocketUtils.onMessage(evt); };
        websocket.onerror = function(evt) { WebSocketUtils.onError(evt); };
    }
};
