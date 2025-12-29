import { Activity, TrendingUp, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

interface Metrics {
    MAE: number;
    RMSE: number;
    MAPE: number;
}

export function MetricsCards({ metrics }: { metrics: Metrics }) {
    const confidence = (100 - metrics.MAPE).toFixed(1);

    const cards = [
        { label: "Model Confidence", value: `${confidence}%`, icon: <TrendingUp size={24} color="#4ade80" /> },
        { label: "Review Error (MAPE)", value: `${metrics.MAPE}%`, icon: <Activity size={24} color="#60a5fa" /> },
        { label: "Root Mean Sq Error", value: metrics.RMSE.toFixed(2), icon: <AlertTriangle size={24} color="#facc15" /> },
    ];

    return (
        <div className="metrics-grid">
            {cards.map((card, idx) => (
                <motion.div
                    key={idx}
                    className="glass-panel metric-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                >
                    <div className="metric-header">
                        <span>{card.label}</span>
                        {card.icon}
                    </div>
                    <div className="metric-value">{card.value}</div>
                </motion.div>
            ))}
        </div>
    );
}
