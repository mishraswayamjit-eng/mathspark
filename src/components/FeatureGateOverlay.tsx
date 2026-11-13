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
    Starter:   'bg-action',
    Advanced:  'bg-action',
    Unlimited: 'bg-action',
  };
  const btnColor = planColors[requiredPlan] ?? 'bg-action';

  return (
    <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-white border-2 border-ink rounded-card p-6 text-center">
      <div className="text-5xl mb-4">🔒</div>
      <h3 className="text-xl font-extrabold text-ink mb-2">
        Available on {requiredPlan}
      </h3>
      <p className="text-ink-muted text-sm mb-6">
        <strong className="text-ink">{feature}</strong> requires the{' '}
        <strong className="text-ink">{requiredPlan}</strong> plan or higher.
        Upgrade to unlock this and more!
      </p>

      <Link
        href="/pricing"
        className={`block w-full ${btnColor} text-white font-extrabold py-3.5 rounded-control border-2 border-ink shadow-hard-sm text-base transition-colors hover:bg-action-dark`}
      >
        See Plans →
      </Link>

      {onDismiss && (
        <button
          onClick={onDismiss}
          className="mt-3 text-ink-muted text-sm hover:text-ink transition-colors"
        >
          Maybe later
        </button>
      )}
    </div>
  );
}
