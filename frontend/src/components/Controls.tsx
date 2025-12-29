import type { ChangeEvent } from 'react';
import { Upload, Settings, Calendar } from 'lucide-react';

interface ControlsProps {
    file: File | null;
    days: number;
    seasonalityMode: string;
    loading: boolean;
    hasData: boolean;
    onFileChange: (e: ChangeEvent<HTMLInputElement>) => void;
    onDaysChange: (val: number) => void;
    onSeasonalityChange: (val: string) => void;
    onSubmit: (e: React.FormEvent) => void;
    onDownload: () => void;
}

export function Controls({
    file,
    days,
    seasonalityMode,
    loading,
    hasData,
    onFileChange,
    onDaysChange,
    onSeasonalityChange,
    onSubmit,
    onDownload
}: ControlsProps) {
    return (
        <div className="glass-panel controls-panel">
            <form onSubmit={onSubmit} className="controls-form">
                <div className="control-group">
                    <label className="label-icon"><Upload size={18} /> Upload Data</label>
                    <div className="file-input-wrapper">
                        <input type="file" accept=".csv,.txt" onChange={onFileChange} id="file-upload" className="file-input" />
                        <label htmlFor="file-upload" className="file-label">
                            {file ? file.name : "Choose CSV file..."}
                        </label>
                    </div>
                </div>

                <div className="control-group">
                    <label className="label-icon"><Calendar size={18} /> Horizon (Days)</label>
                    <input
                        type="number"
                        value={days}
                        onChange={(e) => onDaysChange(parseInt(e.target.value))}
                        min="1"
                        max="365"
                        className="input-field"
                    />
                </div>

                <div className="control-group">
                    <label className="label-icon"><Settings size={18} /> Seasonality</label>
                    <select
                        value={seasonalityMode}
                        onChange={(e) => onSeasonalityChange(e.target.value)}
                        className="select-field"
                    >
                        <option value="additive">Additive</option>
                        <option value="multiplicative">Multiplicative</option>
                    </select>
                </div>

                <div className="actions">
                    <button type="submit" disabled={loading} className="btn-primary">
                        {loading ? 'Processing...' : 'Run Analysis'}
                    </button>

                    {hasData && (
                        <button type="button" onClick={onDownload} disabled={loading} className="btn-secondary">
                            Download PDF
                        </button>
                    )}
                </div>
            </form>
        </div>
    );
}
