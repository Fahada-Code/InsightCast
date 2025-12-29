import { Lightbulb } from 'lucide-react';
import { motion } from 'framer-motion';

export function InsightsList({ insights }: { insights: string[] }) {
    return (
        <div className="glass-panel insights-panel">
            <h3 className="panel-title"><Lightbulb className="title-icon" /> AI Insights</h3>
            <div className="insights-list">
                {insights.map((insight, idx) => (
                    <motion.div
                        key={idx}
                        className="insight-item"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: idx * 0.15 }}
                        dangerouslySetInnerHTML={{ __html: insight.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                    />
                ))}
            </div>
        </div>
    );
}
