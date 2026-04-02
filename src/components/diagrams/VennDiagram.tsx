import React from 'react';

interface Props {
  sets: 2 | 3;
  labels: string[];
  shadedRegion: string;
}

const BLUE = '#1CB0F6';
const BLUE_FILL = 'rgba(28,176,246,0.2)';
const BLUE_STROKE = 'rgba(28,176,246,0.6)';
const GRAY = '#E5E7EB';

/**
 * Renders a Venn diagram with 2 or 3 overlapping circles.
 * Uses clipPath + masks for shading regions.
 *
 * Supported shadedRegion values:
 * - "A∪(B∩C)" : All of A + intersection of B and C
 * - "(P-Q)∩(P-R)" : P only (not in Q or R)
 * - "P∩(Q∪R)" : P's overlap with Q or R
 */
export default function VennDiagram({ sets, labels, shadedRegion }: Props) {
  const id = React.useId();
  const w = 280, h = 180;

  // 3-set positions
  const c1 = { cx: 105, cy: 72, r: 50 };
  const c2 = { cx: 175, cy: 72, r: 50 };
  const c3 = { cx: 140, cy: 120, r: 50 };

  // 2-set positions
  const t1 = { cx: 115, cy: 90, r: 55 };
  const t2 = { cx: 165, cy: 90, r: 55 };

  const circles = sets === 3
    ? [c1, c2, c3]
    : [t1, t2];

  // Determine which regions to shade based on expression
  // We use SVG clipPaths for complex regions
  function getShadingPaths() {
    const [A, B, C] = labels;
    const region = shadedRegion;

    // Normalize: replace set names with positional references
    const norm = region
      .replace(new RegExp(A.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '0')
      .replace(new RegExp(B.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '1')
      .replace(C ? new RegExp(C.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g') : /ZZZZ/g, '2');

    // "0∪(1∩2)" => shade all of circle 0 + intersection of 1 and 2
    if (norm.includes('0∪(1∩2)')) return { shadeAll: [0], shadeIntersection: [1, 2] };
    // "(0-1)∩(0-2)" => shade circle 0 only (exclude overlap with 1 and 2)
    if (norm.includes('(0-1)∩(0-2)')) return { shadeOnly: 0 };
    // "0∩(1∪2)" => shade parts of 0 that overlap with 1 or 2
    if (norm.includes('0∩(1∪2)')) return { shadeIntersections: [[0, 1], [0, 2]] };
    // "0∩1" => shade intersection of 0 and 1
    if (norm.includes('0∩1')) return { shadeIntersection: [0, 1] };

    // Default: shade circle 0
    return { shadeAll: [0] };
  }

  const shading = getShadingPaths();

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full" role="img" aria-label={`Venn diagram: ${shadedRegion}`}>
      <defs>
        {circles.map((c, i) => (
          <clipPath key={`clip-${i}`} id={`${id}-clip-${i}`}>
            <circle cx={c.cx} cy={c.cy} r={c.r} />
          </clipPath>
        ))}
        {/* Inverse clip for "only" regions */}
        {sets === 3 && (
          <mask id={`${id}-only-0`}>
            <rect x={0} y={0} width={w} height={h} fill="white" />
            <circle cx={circles[1].cx} cy={circles[1].cy} r={circles[1].r} fill="black" />
            <circle cx={circles[2].cx} cy={circles[2].cy} r={circles[2].r} fill="black" />
          </mask>
        )}
      </defs>

      {/* Background circles (unshaded) */}
      {circles.map((c, i) => (
        <circle
          key={`bg-${i}`}
          cx={c.cx} cy={c.cy} r={c.r}
          fill="white"
          stroke="#9CA3AF"
          strokeWidth={1.5}
        />
      ))}

      {/* Shaded regions */}
      {'shadeAll' in shading && shading.shadeAll?.map(i => (
        <circle key={`shade-${i}`} cx={circles[i].cx} cy={circles[i].cy} r={circles[i].r}
          fill={BLUE_FILL} stroke="none" />
      ))}

      {'shadeIntersection' in shading && shading.shadeIntersection && (() => {
        const [a, b] = shading.shadeIntersection;
        return (
          <circle
            cx={circles[b].cx} cy={circles[b].cy} r={circles[b].r}
            fill={BLUE_FILL}
            clipPath={`url(#${id}-clip-${a})`}
          />
        );
      })()}

      {'shadeOnly' in shading && typeof shading.shadeOnly === 'number' && (
        <circle
          cx={circles[shading.shadeOnly].cx}
          cy={circles[shading.shadeOnly].cy}
          r={circles[shading.shadeOnly].r}
          fill={BLUE_FILL}
          mask={`url(#${id}-only-0)`}
        />
      )}

      {'shadeIntersections' in shading && shading.shadeIntersections?.map(([a, b], i) => (
        <circle
          key={`si-${i}`}
          cx={circles[b].cx} cy={circles[b].cy} r={circles[b].r}
          fill={BLUE_FILL}
          clipPath={`url(#${id}-clip-${a})`}
        />
      ))}

      {/* Circle outlines on top */}
      {circles.map((c, i) => (
        <circle
          key={`outline-${i}`}
          cx={c.cx} cy={c.cy} r={c.r}
          fill="none"
          stroke={BLUE_STROKE}
          strokeWidth={2}
        />
      ))}

      {/* Labels */}
      {sets === 3 ? (
        <>
          <text x={c1.cx - 30} y={c1.cy - 30} fontSize={14} fontWeight={700} fill="#374151">{labels[0]}</text>
          <text x={c2.cx + 15} y={c2.cy - 30} fontSize={14} fontWeight={700} fill="#374151">{labels[1]}</text>
          <text x={c3.cx} y={c3.cy + 45} textAnchor="middle" fontSize={14} fontWeight={700} fill="#374151">{labels[2]}</text>
        </>
      ) : (
        <>
          <text x={t1.cx - 30} y={t1.cy - 40} fontSize={14} fontWeight={700} fill="#374151">{labels[0]}</text>
          <text x={t2.cx + 10} y={t2.cy - 40} fontSize={14} fontWeight={700} fill="#374151">{labels[1]}</text>
        </>
      )}
    </svg>
  );
}
