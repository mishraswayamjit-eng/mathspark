interface ProgressBarProps {
  value: number;      // 0-100
  color?: string;     // Tailwind bg class
  height?: string;    // Tailwind h class
  showLabel?: boolean;
}

export default function ProgressBar({
  value,
  color = 'bg-blue-500',
  height = 'h-2',
  showLabel = false,
}: ProgressBarProps) {
  const pct = Math.min(100, Math.max(0, Math.round(value)));

  return (
    <div className="w-full">
      <div className={`w-full bg-gray-200 rounded-full overflow-hidden ${height}`}>
        <div
          className={`${color} ${height} rounded-full transition-all duration-500`}
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
      {showLabel && (
        <p className="text-xs text-gray-500 mt-1 text-right">{pct}%</p>
      )}
    </div>
  );
}
