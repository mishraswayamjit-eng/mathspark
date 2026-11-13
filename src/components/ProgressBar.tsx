interface ProgressBarProps {
  value: number;      // 0-100
  color?: string;     // Tailwind bg class (overrides gradient when set)
  height?: string;    // Tailwind h class
  showLabel?: boolean;
}

export default function ProgressBar({
  value,
  color,
  height = 'h-4',
  showLabel = false,
}: ProgressBarProps) {
  const pct = Math.min(100, Math.max(0, Math.round(value)));

  const fillClass = color
    ? color
    : 'bg-action';

  return (
    <div className="w-full">
      <div className={`w-full ui-meter ${height}`}>
        <div
          className={`${fillClass} h-full rounded-full transition-[width] duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      {showLabel && (
        <p className="text-xs text-gray-500 mt-1 text-right font-semibold">{pct}%</p>
      )}
    </div>
  );
}
