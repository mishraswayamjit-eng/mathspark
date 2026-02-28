'use client';

import Link from 'next/link';

interface Props {
  feature:      string;
  requiredPlan: string;
  onDismiss?:   () => void;
}

/**
 * Full-screen overlay shown when a feature requires a higher plan.
 * Place this inside a relative-positioned container.
 */
export default function FeatureGateOverlay({ feature, requiredPlan, onDismiss }: Props) {
  const planColors: Record<string, string> = {
    Starter:   'bg-[#58CC02]',
    Advanced:  'bg-[#1CB0F6]',
    Unlimited: 'bg-[#9B59B6]',
  };
  const btnColor = planColors[requiredPlan] ?? 'bg-[#1CB0F6]';

  return (
    <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-[#131F24]/95 backdrop-blur-sm rounded-2xl p-6 text-center">
      <div className="text-5xl mb-4">🔒</div>
      <h3 className="text-xl font-extrabold text-white mb-2">
        Available on {requiredPlan}
      </h3>
      <p className="text-white/60 text-sm mb-6">
        <strong className="text-white">{feature}</strong> requires the{' '}
        <strong className="text-white">{requiredPlan}</strong> plan or higher.
        Upgrade to unlock this and more!
      </p>

      <Link
        href="/pricing"
        className={`block w-full ${btnColor} text-white font-extrabold py-3.5 rounded-2xl text-base transition-opacity hover:opacity-90`}
      >
        See Plans →
      </Link>

      {onDismiss && (
        <button
          onClick={onDismiss}
          className="mt-3 text-white/40 text-sm hover:text-white/70 transition-colors"
        >
          Maybe later
        </button>
      )}
    </div>
  );
}
