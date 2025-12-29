import {
    ComposedChart,
    Line,
    Scatter,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Area,
    Brush
} from 'recharts';


interface ForecastChartProps {
    data: any[];
    anomalies: any[];
}

export function ForecastChart({ data, anomalies }: ForecastChartProps) {
    // Merge anomalies into chart data
    const chartData = data.map(point => {
        const anomaly = anomalies.find(a => new Date(a.ds).getTime() === new Date(point.ds).getTime());
        return {
            ...point,
            anomalyValue: anomaly ? anomaly.y : null,
        };
    });

    return (
        <div className="glass-panel chart-panel">
            <div className="panel-header">
                <h2>Forecast & Anomaly Detection</h2>
                <div className="badges">
                    <span className="badge">Drag to Zoom</span>
                </div>
            </div>

            <div style={{ width: '100%', height: 450 }}>
                <ResponsiveContainer>
                    <ComposedChart data={chartData}>
                        <defs>
                            <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#444" vertical={false} />
                        <XAxis
                            dataKey="ds"
                            tickFormatter={(tick) => new Date(tick).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                            stroke="#ccc"
                        />
                        <YAxis stroke="#ccc" />
                        <Tooltip
                            contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '8px', color: '#fff' }}
                            labelFormatter={(label) => new Date(label).toDateString()}
                        />
                        <Legend wrapperStyle={{ paddingTop: '20px' }} />

                        <Area
                            type="monotone"
                            dataKey="yhat_upper"
                            stroke="none"
                            fill="#82ca9d"
                            fillOpacity={0.1}
                        />

                        <Line
                            type="monotone"
                            dataKey="yhat"
                            stroke="#8884d8"
                            name="Forecast"
                            dot={false}
                            strokeWidth={3}
                            activeDot={{ r: 8 }}
                        />

                        <Line
                            type="monotone"
                            dataKey="yhat_upper"
                            stroke="#82ca9d"
                            name="Confidence Bounds"
                            strokeDasharray="5 5"
                            dot={false}
                            strokeWidth={1}
                        />
                        <Line
                            type="monotone"
                            dataKey="yhat_lower"
                            stroke="#82ca9d"
                            name=""
                            strokeDasharray="5 5"
                            dot={false}
                            strokeWidth={1}
                            legendType='none'
                        />

                        <Scatter
                            dataKey="anomalyValue"
                            name="Anomaly"
                            fill="#ef4444"
                            shape="circle"
                        />

                        <Brush dataKey="ds" height={30} stroke="#8884d8" fill="#1f2937" />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
