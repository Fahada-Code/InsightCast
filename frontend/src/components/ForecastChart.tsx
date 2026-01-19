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
    // Sort and Merge anomalies into chart data
    const sortedData = [...data].sort((a, b) => new Date(a.ds).getTime() - new Date(b.ds).getTime());

    const chartData = sortedData.map(point => {
        const anomaly = anomalies.find(a => new Date(a.ds).getTime() === new Date(point.ds).getTime());
        return {
            ...point,
            anomalyValue: anomaly ? anomaly.y : null,
            severity_level: anomaly ? anomaly.severity_level : null,
        };
    });

    // Prepare dedicated anomaly series to avoid drawing at y=0/null
    const anomalySeries = chartData
        .filter(d => d.anomalyValue !== null)
        .map(d => ({
            ds: d.ds,
            anomalyValue: d.anomalyValue,
            severity_level: d.severity_level
        }));

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
                                <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                        <XAxis
                            dataKey="ds"
                            tickFormatter={(tick) => new Date(tick).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                            stroke="#64748b"
                            minTickGap={30}
                        />
                        <YAxis stroke="#64748b" tickFormatter={(val) => typeof val === 'number' ? val.toLocaleString(undefined, { maximumFractionDigits: 1 }) : val} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', color: '#0f172a', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                            labelFormatter={(label) => new Date(label).toDateString()}
                            formatter={(value: any, name: string | any) => {
                                if (typeof value !== 'number') return [value, name];
                                // Improve labels based on dataKey name
                                const labelMap: Record<string, string> = {
                                    'yhat': 'Forecast',
                                    'yhat_upper': 'Upper Bound',
                                    'yhat_lower': 'Lower Bound',
                                    'anomalyValue': 'Actual (Anomaly)'
                                };
                                return [value.toFixed(2), labelMap[name] || name];
                            }}
                        />
                        <Legend verticalAlign="top" height={36} wrapperStyle={{ paddingTop: '10px' }} />

                        <Area
                            type="monotone"
                            dataKey="yhat_upper"
                            stroke="none"
                            fill="#94a3b8"
                            fillOpacity={0.2}
                            name="yhat_upper"
                            legendType="none"
                        />

                        <Line
                            type="monotone"
                            dataKey="yhat"
                            stroke="#0ea5e9"
                            name="yhat"
                            dot={false}
                            strokeWidth={3}
                            activeDot={{ r: 8 }}
                        />

                        <Line
                            type="monotone"
                            dataKey="yhat_upper"
                            stroke="#475569"
                            name="yhat_upper"
                            strokeDasharray="5 5"
                            dot={false}
                            strokeWidth={1.5}
                        />
                        <Line
                            type="monotone"
                            dataKey="yhat_lower"
                            stroke="#475569"
                            name="yhat_lower"
                            strokeDasharray="5 5"
                            dot={false}
                            strokeWidth={1.5}
                        />

                        <Scatter
                            data={anomalySeries}
                            dataKey="anomalyValue"
                            name="anomalyValue"
                            fill="#ff0000"
                            legendType="circle"
                            shape={(props: any) => {
                                const { cx, cy, payload } = props;
                                if (typeof cx !== 'number' || typeof cy !== 'number') return <path d="" />;

                                const severity = payload.severity_level;

                                let fill = "#ff0000"; // Critical
                                let size = 12; // Slightly bigger as requested

                                if (severity === 'Medium') {
                                    fill = "#f97316"; // Significant
                                    size = 8;
                                } else if (severity === 'Low') {
                                    fill = "#f59e0b"; // Notable
                                    size = 6;
                                }

                                return (
                                    <circle
                                        cx={cx}
                                        cy={cy}
                                        r={size}
                                        fill={fill}
                                        stroke="#ffffff"
                                        strokeWidth={2}
                                    />
                                );
                            }}
                        />

                        <Brush dataKey="ds" height={30} stroke="#3b82f6" fill="#f8fafc" />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
