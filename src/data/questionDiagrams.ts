// ── Question → Diagram mapping ─────────────────────────────────────────────
// Static mapping from question IDs to diagram component + props.
// No DB changes needed. QuestionDiagram.tsx reads this at render time.

// ── Shared types ──────────────────────────────────────────────────────────

export interface FractionDiagramSpec {
  type: 'fraction';
  props: {
    shape: 'rectangle' | 'circle' | 'triangle';
    totalParts: number;
    shadedParts: number;
    columns?: number;
    label?: string;
  };
}

export interface MultiFractionDiagramSpec {
  type: 'multiFraction';
  props: {
    figures: Array<{
      shape: 'rectangle' | 'circle' | 'triangle';
      totalParts: number;
      shadedParts: number;
      columns?: number;
      label: string;
    }>;
    highlightIndex?: number; // which figure to highlight as correct
  };
}

export interface BalanceDiagramSpec {
  type: 'balance';
  props: {
    scales: Array<{
      left: Array<{ label: string; count?: number; shape?: 'circle' | 'triangle' | 'square' | 'star' }>;
      right: Array<{ label: string; count?: number; shape?: 'circle' | 'triangle' | 'square' | 'star' }>;
    }>;
  };
}

export interface AngleDiagramSpec {
  type: 'angle';
  props: {
    lines: Array<{
      x1: number; y1: number;
      x2: number; y2: number;
      label?: string;
      parallel?: boolean;
    }>;
    angles: Array<{
      cx: number; cy: number;
      startAngle: number;
      endAngle: number;
      label: string;
      radius?: number;
    }>;
    points: Array<{
      x: number; y: number;
      label: string;
    }>;
  };
}

export interface VennDiagramSpec {
  type: 'venn';
  props: {
    sets: 2 | 3;
    labels: string[];
    shadedRegion: string; // e.g. "A∪(B∩C)", "P-(Q∪R)", "(P-Q)∩(P-R)"
  };
}

export interface CircleDiagramSpec {
  type: 'circle';
  props: {
    variant: 'sector' | 'inscribed' | 'twoCirclesOnDiameter' | 'semicircles' | 'circleInSquare' | 'fourCirclesInSquare' | 'segment' | 'twoDiameters';
    radius?: number;
    angle?: number;
    labels?: Array<{ text: string; x: number; y: number }>;
    shaded?: string; // description of shaded region
    dimensions?: Record<string, string>;
  };
}

export interface TriangleDiagramSpec {
  type: 'triangle';
  props: {
    variant: 'countTriangles' | 'countSquares' | 'labeled' | 'rightTriangle';
    subdivisions?: number;
    answer?: number;
    vertices?: Array<{ x: number; y: number; label?: string }>;
    lines?: Array<{ x1: number; y1: number; x2: number; y2: number }>;
    labels?: Array<{ text: string; x: number; y: number }>;
  };
}

export interface CompositeShapeDiagramSpec {
  type: 'compositeShape';
  props: {
    rects: Array<{
      x: number; y: number;
      width: number; height: number;
      label?: string;
      shaded?: boolean;
    }>;
    dimensions: Array<{
      x1: number; y1: number;
      x2: number; y2: number;
      label: string;
    }>;
  };
}

export interface PatternDiagramSpec {
  type: 'pattern';
  props: {
    variant: 'symbols' | 'shapes' | 'dots' | 'blocks';
    sequence: string[];
    showQuestion?: boolean;
  };
}

export interface MirrorDiagramSpec {
  type: 'mirror';
  props: {
    variant: 'letter' | 'shape' | 'arrow' | 'symmetry';
    content: string;
    axis: 'vertical' | 'horizontal';
  };
}

export interface ClockDiagramSpec {
  type: 'clock';
  props: {
    hour: number;
    minute: number;
  };
}

export interface NumberLineDiagramSpec {
  type: 'numberLine';
  props: {
    min: number;
    max: number;
    points: Array<{ value: number; label: string }>;
    step?: number;
  };
}

export interface BlockDiagramSpec {
  type: 'blocks';
  props: {
    layers: number[][];   // each layer is a grid row of block counts
    answer: number;
  };
}

export interface AbacusDiagramSpec {
  type: 'abacus';
  props: {
    rods: Array<{ label: string; beads: number }>;
  };
}

export interface CalendarDiagramSpec {
  type: 'calendar';
  props: {
    month: string;
    year: number;
    startDay: number;
    daysInMonth: number;
    highlight?: number[];
  };
}

export interface CurrencyDiagramSpec {
  type: 'currency';
  props: {
    items: Array<{ type: 'coin' | 'note'; value: string }>;
  };
}

export interface NumberGridDiagramSpec {
  type: 'numberGrid';
  props: {
    grid: string[][];
    unknownLabel?: string;
  };
}

export interface TetrominoDiagramSpec {
  type: 'tetromino';
  props: {
    figures: Array<{ cells: Array<[number, number]>; label: string }>;
  };
}

export interface PolygonDiagramSpec {
  type: 'polygon';
  props: {
    sides: number;
    labels: Array<{ text: string; side: number }>;
  };
}

export interface HeightsDistanceDiagramSpec {
  type: 'heightsDistance';
  props: {
    variant: 'cliff-tower' | 'cliff-boat';
    heights: { cliff: number; tower?: number };
    angles: number[];
    labels?: Record<string, string>;
  };
}

export interface PictographDiagramSpec {
  type: 'pictograph';
  props: {
    icon: 'candle' | 'star' | 'apple';
    count: number;
    label?: string;
  };
}

export type DiagramSpec =
  | FractionDiagramSpec
  | MultiFractionDiagramSpec
  | BalanceDiagramSpec
  | AngleDiagramSpec
  | VennDiagramSpec
  | CircleDiagramSpec
  | TriangleDiagramSpec
  | CompositeShapeDiagramSpec
  | PatternDiagramSpec
  | MirrorDiagramSpec
  | ClockDiagramSpec
  | NumberLineDiagramSpec
  | BlockDiagramSpec
  | AbacusDiagramSpec
  | CalendarDiagramSpec
  | CurrencyDiagramSpec
  | NumberGridDiagramSpec
  | TetrominoDiagramSpec
  | PolygonDiagramSpec
  | HeightsDistanceDiagramSpec
  | PictographDiagramSpec;

// ── Mapping ───────────────────────────────────────────────────────────────

export const QUESTION_DIAGRAMS: Record<string, DiagramSpec> = {

  // ═══════════════════════════════════════════════════════════════════════
  // FRACTIONS / SHADED PARTS
  // ═══════════════════════════════════════════════════════════════════════

  // "Represent the unshaded portion of the figure in fractional form" — 8 parts, 5 shaded → answer 3/8
  'EXT_G5_WS_B7_001': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 8, shadedParts: 5, columns: 4, label: 'Unshaded = ?' },
  },

  // "Fraction of unshaded part (1 of 3 circles shaded)" → answer 2/3
  'EXT_G2_PP_01_017': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 3, shadedParts: 1, columns: 3 },
  },

  // "In which figure is the shaded part 3/5?" → answer B (Figure 2)
  'EXT_G2_PP_01_021': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 5, shadedParts: 2, label: 'Fig 1' },
        { shape: 'rectangle', totalParts: 5, shadedParts: 3, label: 'Fig 2' },
        { shape: 'rectangle', totalParts: 5, shadedParts: 4, label: 'Fig 3' },
        { shape: 'rectangle', totalParts: 5, shadedParts: 1, label: 'Fig 4' },
      ],
      highlightIndex: 1,
    },
  },

  // "Which shaded portion is smaller?" → answer A (Figure 1)
  'EXT_G2_PP_01_043': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 8, shadedParts: 2, label: 'Fig 1' },
        { shape: 'rectangle', totalParts: 4, shadedParts: 2, label: 'Fig 2' },
        { shape: 'circle', totalParts: 6, shadedParts: 3, label: 'Fig 3' },
        { shape: 'circle', totalParts: 4, shadedParts: 3, label: 'Fig 4' },
      ],
      highlightIndex: 0,
    },
  },

  // "In which figure is the circled part 1/3?" → answer B (Fig 2)
  'EXT_G2_PP_02_020': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'circle', totalParts: 4, shadedParts: 1, label: 'Fig 1' },
        { shape: 'circle', totalParts: 3, shadedParts: 1, label: 'Fig 2' },
        { shape: 'circle', totalParts: 2, shadedParts: 1, label: 'Fig 3' },
        { shape: 'circle', totalParts: 6, shadedParts: 1, label: 'Fig 4' },
      ],
      highlightIndex: 1,
    },
  },

  // "Which 2 figures are equally shaded?" → answer D (Q & R)
  'EXT_G2_PP_02_041': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 4, shadedParts: 3, label: 'P' },
        { shape: 'circle', totalParts: 4, shadedParts: 2, label: 'Q' },
        { shape: 'triangle', totalParts: 4, shadedParts: 2, label: 'R' },
        { shape: 'circle', totalParts: 8, shadedParts: 3, label: 'S' },
      ],
    },
  },

  // "In which figure is shaded portion 1/2?" → answer B (Q)
  'EXT_G2_PP_02_042': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 4, shadedParts: 1, label: 'P' },
        { shape: 'rectangle', totalParts: 4, shadedParts: 2, label: 'Q' },
        { shape: 'circle', totalParts: 4, shadedParts: 3, label: 'R' },
        { shape: 'circle', totalParts: 8, shadedParts: 5, label: 'S' },
      ],
      highlightIndex: 1,
    },
  },

  // "Unshaded portion in figure S is ___" → answer 3/4
  'EXT_G2_PP_02_043': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 4, shadedParts: 1, label: 'S' },
  },

  // Grade 2 Paper 3 — fraction from figure
  'EXT_G2_PP_03_004': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 6, shadedParts: 4, columns: 3 },
  },
  'EXT_G2_PP_03_005': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 8, shadedParts: 3 },
  },
  'EXT_G2_PP_04_002': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 6, shadedParts: 2, columns: 3 },
  },
  'EXT_G2_PP_04_004': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 5, shadedParts: 2 },
  },

  // Grade 3 fraction questions
  'EXT_G3_MF_2010_002': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 8, shadedParts: 3, columns: 4 },
  },
  'EXT_G3_MF_2011_012': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 6, shadedParts: 2 },
  },
  'EXT_G3_MF_2016_004': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 10, shadedParts: 7, columns: 5 },
  },
  'EXT_G3_MF_2018_014': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 4, shadedParts: 3 },
  },
  'EXT_G3_MF_2019_003': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 8, shadedParts: 5, columns: 4 },
  },
  'EXT_G3_MF_2024_013': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 12, shadedParts: 7, columns: 4 },
  },

  // Grade 8 — shaded area with circle geometry
  'EXT_G8_MF_2020_002': {
    type: 'circle',
    props: {
      variant: 'semicircles',
      radius: 6,
      dimensions: { PS: '12', PQ: '4', RS: '4' },
      shaded: 'Yin-yang type: large semicircle minus three small semicircles',
      labels: [
        { text: 'P', x: 20, y: 140 },
        { text: 'Q', x: 73, y: 140 },
        { text: 'R', x: 207, y: 140 },
        { text: 'S', x: 260, y: 140 },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // VENN DIAGRAMS
  // ═══════════════════════════════════════════════════════════════════════

  // "The shaded region in the given Venn Diagram represents?" → A∪(B∩C)
  'EXT_G8_MF_2020_014': {
    type: 'venn',
    props: { sets: 3, labels: ['A', 'B', 'C'], shadedRegion: 'A∪(B∩C)' },
  },

  // "The shaded region in the given Venn diagram represents?" → None of these (D)
  'EXT_G8_MF_2022_008': {
    type: 'venn',
    props: { sets: 3, labels: ['P', 'Q', 'R'], shadedRegion: 'P∩(Q∪R)' },
  },

  // "The shaded region in the Venn diagram represents?" → A∪(B∩C)
  'EXT_G9_MF_2022_005': {
    type: 'venn',
    props: { sets: 3, labels: ['A', 'B', 'C'], shadedRegion: 'A∪(B∩C)' },
  },

  // "The shaded region in the adjoining figure is:" → (P-Q)∩(P-R)
  'EXT_G9_MF_2020_015': {
    type: 'venn',
    props: { sets: 3, labels: ['P', 'Q', 'R'], shadedRegion: '(P-Q)∩(P-R)' },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CIRCLE / SECTOR DIAGRAMS
  // ═══════════════════════════════════════════════════════════════════════

  // PR and QS two diameters, PR=28cm, PS=14√3 → shaded = 2 segments, answer 241.12
  'EXT_G8_MF_2021_004': {
    type: 'circle',
    props: {
      variant: 'twoDiameters',
      radius: 14,
      angle: 120,
      shaded: 'Two opposite segments between diameters',
      labels: [
        { text: 'P', x: 20, y: 80 },
        { text: 'R', x: 260, y: 80 },
        { text: 'Q', x: 140, y: 10 },
        { text: 'S', x: 140, y: 150 },
        { text: 'O', x: 140, y: 80 },
      ],
      dimensions: { PR: '28 cm', PS: '14√3 cm' },
    },
  },

  // Equilateral triangle ABC, B is centre, diameter=28cm → shaded = segment
  'EXT_G8_MF_2022_003': {
    type: 'circle',
    props: {
      variant: 'segment',
      radius: 14,
      angle: 60,
      shaded: 'Segment between chord AC and arc (60° sector minus triangle)',
      labels: [
        { text: 'A', x: 70, y: 20 },
        { text: 'B', x: 140, y: 80 },
        { text: 'C', x: 70, y: 140 },
      ],
      dimensions: { diameter: '28 cm' },
    },
  },

  // AB diameter, OA=7cm → answer 66.5
  'EXT_G8_MF_2023_010': {
    type: 'circle',
    props: {
      variant: 'segment',
      radius: 7,
      shaded: 'Shaded region within semicircle',
      labels: [
        { text: 'A', x: 20, y: 80 },
        { text: 'B', x: 260, y: 80 },
        { text: 'O', x: 140, y: 80 },
      ],
      dimensions: { OA: '7 cm' },
    },
  },

  // PQRS square, 4 circles touching → ratio 3:11
  'EXT_G9_MF_2022_012': {
    type: 'circle',
    props: {
      variant: 'fourCirclesInSquare',
      shaded: 'Region inside square but outside all four circles',
      labels: [
        { text: 'P', x: 15, y: 15 },
        { text: 'Q', x: 255, y: 15 },
        { text: 'R', x: 255, y: 145 },
        { text: 'S', x: 15, y: 145 },
      ],
    },
  },

  // Two small circles on diameter, each radius=1
  'EXT_G6_FP_2016_017': {
    type: 'circle',
    props: {
      variant: 'twoCirclesOnDiameter',
      radius: 2,
      shaded: 'Region in large circle but outside both small circles',
      labels: [
        { text: 'A', x: 20, y: 80 },
        { text: 'C', x: 260, y: 80 },
      ],
      dimensions: { smallRadius: '1' },
    },
  },

  // Square perimeter=112, circle inside → shaded region
  'EXT_G6_FP_2018_021': {
    type: 'circle',
    props: {
      variant: 'circleInSquare',
      radius: 14,
      shaded: 'Region inside square but outside circle',
      dimensions: { squarePerimeter: '112 cm' },
    },
  },

  // Square perimeter=56, inscribed circle → shaded = sq − circle
  'EXT_G6_FP_2019_002': {
    type: 'circle',
    props: {
      variant: 'circleInSquare',
      radius: 7,
      shaded: 'Region inside square but outside inscribed circle',
      dimensions: { squarePerimeter: '56 cm' },
    },
  },

  // "Shaded region in circle figure is?" → Minor segment
  'EXT_G6_FP_2019_039': {
    type: 'circle',
    props: {
      variant: 'segment',
      radius: 10,
      angle: 90,
      shaded: 'Minor segment (between chord and arc)',
      labels: [
        { text: 'O', x: 140, y: 80 },
      ],
    },
  },

  // Area of shaded region, circle radius=14cm → answer 56
  'EXT_G6_FP_2021_003': {
    type: 'circle',
    props: {
      variant: 'sector',
      radius: 14,
      angle: 90,
      shaded: 'Sector minus triangle = segment',
      labels: [
        { text: 'O', x: 140, y: 80 },
      ],
      dimensions: { radius: '14 cm' },
    },
  },

  // "Shaded region P-X-Q in circle diagram is?" → Minor Segment
  'EXT_G6_FP_2022_036': {
    type: 'circle',
    props: {
      variant: 'segment',
      radius: 10,
      angle: 80,
      shaded: 'Minor segment P-X-Q',
      labels: [
        { text: 'P', x: 60, y: 30 },
        { text: 'Q', x: 220, y: 30 },
        { text: 'X', x: 140, y: 10 },
        { text: 'O', x: 140, y: 80 },
      ],
    },
  },

  // Shaded region r=10cm, angle XOY=90° → answer 28.5
  'EXT_G6_FP_2023_015': {
    type: 'circle',
    props: {
      variant: 'sector',
      radius: 10,
      angle: 90,
      shaded: 'Sector area minus triangle area',
      labels: [
        { text: 'X', x: 250, y: 80 },
        { text: 'Y', x: 140, y: 10 },
        { text: 'O', x: 140, y: 80 },
      ],
      dimensions: { radius: '10 cm', angle: '90°' },
    },
  },

  // Circumference=88 → r=14, circle inscribed in square → shaded
  'EXT_G6_FP_2023_030': {
    type: 'circle',
    props: {
      variant: 'circleInSquare',
      radius: 14,
      shaded: 'Region inside square but outside circle',
      dimensions: { circumference: '88 cm' },
    },
  },

  // Perimeter of circle=88cm → similar to above
  'EXT_G6_FP_2025_026': {
    type: 'circle',
    props: {
      variant: 'circleInSquare',
      radius: 14,
      shaded: 'Shaded region in figure',
      dimensions: { perimeterCircle: '88 cm' },
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // ANGLE / PARALLEL LINES
  // ═══════════════════════════════════════════════════════════════════════

  // "Adjacent angles from diagram?" → answer ∠AOB & ∠BOC
  'EXT_G6_FP_2016_031': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 80, x2: 260, y2: 80, label: '' },
        { x1: 140, y1: 80, x2: 60, y2: 20, label: '' },
        { x1: 140, y1: 80, x2: 220, y2: 20, label: '' },
        { x1: 140, y1: 80, x2: 140, y2: 10, label: '' },
      ],
      angles: [
        { cx: 140, cy: 80, startAngle: 180, endAngle: 135, label: '∠AOB' },
        { cx: 140, cy: 80, startAngle: 135, endAngle: 90, label: '∠BOC' },
        { cx: 140, cy: 80, startAngle: 90, endAngle: 35, label: '∠COD' },
        { cx: 140, cy: 80, startAngle: 35, endAngle: 0, label: '∠DOE' },
      ],
      points: [
        { x: 20, y: 80, label: 'A' },
        { x: 60, y: 20, label: 'B' },
        { x: 140, y: 10, label: 'C' },
        { x: 220, y: 20, label: 'D' },
        { x: 260, y: 80, label: 'E' },
        { x: 140, y: 80, label: 'O' },
      ],
    },
  },

  // "AB‖CD. Which statement is true?" → GH‖EF
  'EXT_G6_FP_2017_017': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 40, x2: 260, y2: 40, label: '', parallel: true },
        { x1: 20, y1: 120, x2: 260, y2: 120, label: '', parallel: true },
        { x1: 60, y1: 10, x2: 100, y2: 150 },
        { x1: 180, y1: 10, x2: 220, y2: 150 },
      ],
      angles: [
        { cx: 72, cy: 40, startAngle: 250, endAngle: 360, label: '85°', radius: 20 },
        { cx: 195, cy: 40, startAngle: 250, endAngle: 360, label: '85°', radius: 20 },
      ],
      points: [
        { x: 20, y: 40, label: 'A' },
        { x: 260, y: 40, label: 'B' },
        { x: 20, y: 120, label: 'C' },
        { x: 260, y: 120, label: 'D' },
        { x: 60, y: 10, label: 'E' },
        { x: 100, y: 150, label: 'F' },
        { x: 180, y: 10, label: 'G' },
        { x: 220, y: 150, label: 'H' },
      ],
    },
  },

  // "AB‖CD. Find angle x" → answer 80°
  'EXT_G6_FP_2021_024': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 40, x2: 260, y2: 40, parallel: true },
        { x1: 20, y1: 120, x2: 260, y2: 120, parallel: true },
        { x1: 80, y1: 10, x2: 200, y2: 150 },
      ],
      angles: [
        { cx: 100, cy: 40, startAngle: 250, endAngle: 360, label: '80°', radius: 22 },
        { cx: 160, cy: 120, startAngle: 70, endAngle: 180, label: 'x', radius: 22 },
      ],
      points: [
        { x: 20, y: 40, label: 'A' },
        { x: 260, y: 40, label: 'B' },
        { x: 20, y: 120, label: 'C' },
        { x: 260, y: 120, label: 'D' },
      ],
    },
  },

  // "Find angle Z from polygon figure" → answer 103°
  'EXT_G6_FP_2021_030': {
    type: 'angle',
    props: {
      lines: [
        { x1: 60, y1: 30, x2: 220, y2: 30 },
        { x1: 220, y1: 30, x2: 260, y2: 120 },
        { x1: 260, y1: 120, x2: 140, y2: 150 },
        { x1: 140, y1: 150, x2: 20, y2: 120 },
        { x1: 20, y1: 120, x2: 60, y2: 30 },
      ],
      angles: [
        { cx: 60, cy: 30, startAngle: 300, endAngle: 360, label: '108°', radius: 20 },
        { cx: 220, cy: 30, startAngle: 180, endAngle: 250, label: '120°', radius: 20 },
        { cx: 260, cy: 120, startAngle: 135, endAngle: 200, label: '112°', radius: 20 },
        { cx: 140, cy: 150, startAngle: 30, endAngle: 130, label: 'z', radius: 22 },
        { cx: 20, cy: 120, startAngle: 330, endAngle: 60, label: '97°', radius: 20 },
      ],
      points: [],
    },
  },

  // "XY‖AB, PQ transversal. Sum of ∠PCA and ∠PDX" → (6m-12)°
  'EXT_G6_FP_2024_015': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 50, x2: 260, y2: 50, parallel: true },
        { x1: 20, y1: 120, x2: 260, y2: 120, parallel: true },
        { x1: 60, y1: 10, x2: 220, y2: 150 },
      ],
      angles: [
        { cx: 110, cy: 50, startAngle: 250, endAngle: 360, label: '(3m−6)°', radius: 25 },
        { cx: 165, cy: 120, startAngle: 70, endAngle: 180, label: '(3m−6)°', radius: 25 },
      ],
      points: [
        { x: 20, y: 50, label: 'X' },
        { x: 260, y: 50, label: 'Y' },
        { x: 20, y: 120, label: 'A' },
        { x: 260, y: 120, label: 'B' },
        { x: 60, y: 10, label: 'P' },
        { x: 220, y: 150, label: 'Q' },
        { x: 110, y: 50, label: 'D' },
        { x: 165, y: 120, label: 'C' },
      ],
    },
  },

  // "XY‖MN, t1‖t2, find angle P" → answer 110°
  'EXT_G6_FP_2024_017': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 30, x2: 260, y2: 30, parallel: true },
        { x1: 20, y1: 130, x2: 260, y2: 130, parallel: true },
        { x1: 50, y1: 10, x2: 120, y2: 150, parallel: true },
        { x1: 160, y1: 10, x2: 230, y2: 150, parallel: true },
      ],
      angles: [
        { cx: 65, cy: 30, startAngle: 250, endAngle: 360, label: '70°', radius: 22 },
        { cx: 140, cy: 80, startAngle: 50, endAngle: 150, label: 'P', radius: 18 },
      ],
      points: [
        { x: 20, y: 30, label: 'X' },
        { x: 260, y: 30, label: 'Y' },
        { x: 20, y: 130, label: 'M' },
        { x: 260, y: 130, label: 'N' },
        { x: 50, y: 10, label: 't₁' },
        { x: 160, y: 10, label: 't₂' },
      ],
    },
  },

  // XY‖MN, ∠AXY=55°, ∠MAN=88° → answer ∠NMA=37°
  'EXT_G6_FP_2025_006': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 30, x2: 260, y2: 30, parallel: true },
        { x1: 20, y1: 130, x2: 260, y2: 130, parallel: true },
        { x1: 90, y1: 30, x2: 160, y2: 130 },
      ],
      angles: [
        { cx: 90, cy: 30, startAngle: 240, endAngle: 360, label: '55°', radius: 22 },
        { cx: 130, cy: 80, startAngle: 60, endAngle: 148, label: '88°', radius: 20 },
        { cx: 160, cy: 130, startAngle: 60, endAngle: 97, label: '?', radius: 22 },
      ],
      points: [
        { x: 20, y: 30, label: 'X' },
        { x: 260, y: 30, label: 'Y' },
        { x: 20, y: 130, label: 'M' },
        { x: 260, y: 130, label: 'N' },
        { x: 130, y: 80, label: 'A' },
      ],
    },
  },

  // AB‖CD, DE‖BF, ∠ACB=68° → answer (112+q)°
  'EXT_G6_FP_2025_019': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 40, x2: 260, y2: 40, parallel: true },
        { x1: 20, y1: 120, x2: 260, y2: 120, parallel: true },
        { x1: 80, y1: 10, x2: 160, y2: 150 },
        { x1: 180, y1: 10, x2: 230, y2: 150, parallel: true },
      ],
      angles: [
        { cx: 120, cy: 80, startAngle: 60, endAngle: 128, label: '68°', radius: 20 },
        { cx: 190, cy: 80, startAngle: 0, endAngle: 90, label: 'M', radius: 18 },
      ],
      points: [
        { x: 20, y: 40, label: 'A' },
        { x: 260, y: 40, label: 'B' },
        { x: 20, y: 120, label: 'C' },
        { x: 260, y: 120, label: 'D' },
        { x: 180, y: 10, label: 'E' },
        { x: 230, y: 150, label: 'F' },
      ],
    },
  },

  // "In given figure y=2n. Find y" → answer 72°
  'EXT_G6_FP_2025_035': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 80, x2: 260, y2: 80 },
        { x1: 140, y1: 80, x2: 60, y2: 15 },
        { x1: 140, y1: 80, x2: 220, y2: 15 },
      ],
      angles: [
        { cx: 140, cy: 80, startAngle: 145, endAngle: 180, label: 'n', radius: 30 },
        { cx: 140, cy: 80, startAngle: 107, endAngle: 145, label: '36°', radius: 25 },
        { cx: 140, cy: 80, startAngle: 35, endAngle: 107, label: 'y=2n', radius: 30 },
      ],
      points: [],
    },
  },

  // Segment BD and AE intersect at C, AB=BC=CD=CE, ∠A=5/2∠B → answer 52.5°
  'EXT_G9_MF_2020_014': {
    type: 'angle',
    props: {
      lines: [
        { x1: 40, y1: 30, x2: 240, y2: 130 },
        { x1: 240, y1: 30, x2: 40, y2: 130 },
      ],
      angles: [
        { cx: 40, cy: 30, startAngle: 330, endAngle: 360, label: '∠A', radius: 25 },
        { cx: 240, cy: 30, startAngle: 180, endAngle: 215, label: '∠B', radius: 25 },
        { cx: 240, cy: 130, startAngle: 145, endAngle: 180, label: '∠D', radius: 25 },
      ],
      points: [
        { x: 40, y: 30, label: 'A' },
        { x: 240, y: 30, label: 'B' },
        { x: 140, y: 80, label: 'C' },
        { x: 240, y: 130, label: 'D' },
        { x: 40, y: 130, label: 'E' },
      ],
    },
  },

  // Angle C=90°, AD=DB, DE⊥AB, AB=20, AC=12 → answer 58.5
  'EXT_G9_MF_2021_010': {
    type: 'angle',
    props: {
      lines: [
        { x1: 40, y1: 130, x2: 40, y2: 30 },
        { x1: 40, y1: 30, x2: 230, y2: 130 },
        { x1: 40, y1: 130, x2: 230, y2: 130 },
        { x1: 135, y1: 80, x2: 135, y2: 130 },
      ],
      angles: [
        { cx: 40, cy: 130, startAngle: 270, endAngle: 360, label: '90°', radius: 15 },
      ],
      points: [
        { x: 40, y: 30, label: 'A' },
        { x: 230, y: 130, label: 'B' },
        { x: 40, y: 130, label: 'C' },
        { x: 135, y: 80, label: 'D' },
        { x: 135, y: 130, label: 'E' },
      ],
    },
  },

  // Grade 3-4 angle questions
  'EXT_G3_MF_2011_010': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 80, x2: 260, y2: 80 },
        { x1: 140, y1: 80, x2: 200, y2: 20 },
      ],
      angles: [
        { cx: 140, cy: 80, startAngle: 330, endAngle: 360, label: '?', radius: 25 },
      ],
      points: [],
    },
  },

  'EXT_G3_MF_2012_013': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 80, x2: 260, y2: 80 },
        { x1: 140, y1: 80, x2: 60, y2: 20 },
        { x1: 140, y1: 80, x2: 220, y2: 20 },
      ],
      angles: [
        { cx: 140, cy: 80, startAngle: 145, endAngle: 180, label: 'a', radius: 25 },
        { cx: 140, cy: 80, startAngle: 35, endAngle: 145, label: 'b', radius: 30 },
        { cx: 140, cy: 80, startAngle: 0, endAngle: 35, label: 'c', radius: 25 },
      ],
      points: [],
    },
  },

  'EXT_G4_FP_2022_015': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 80, x2: 260, y2: 80 },
        { x1: 140, y1: 80, x2: 140, y2: 10 },
        { x1: 140, y1: 80, x2: 220, y2: 25 },
      ],
      angles: [
        { cx: 140, cy: 80, startAngle: 70, endAngle: 90, label: 'x', radius: 30 },
        { cx: 140, cy: 80, startAngle: 90, endAngle: 180, label: '90°', radius: 20 },
      ],
      points: [],
    },
  },

  'EXT_G4_FP_2024_023': {
    type: 'angle',
    props: {
      lines: [
        { x1: 20, y1: 80, x2: 260, y2: 80 },
        { x1: 140, y1: 80, x2: 80, y2: 15 },
      ],
      angles: [
        { cx: 140, cy: 80, startAngle: 135, endAngle: 180, label: '45°', radius: 30 },
      ],
      points: [],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // BALANCE SCALES
  // ═══════════════════════════════════════════════════════════════════════

  'EXT_G2_PP_01_028': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '●', count: 3, shape: 'circle' }], right: [{ label: '▲', count: 1, shape: 'triangle' }] },
      ],
    },
  },

  'EXT_G2_PP_01_037': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '■', count: 2, shape: 'square' }], right: [{ label: '●', count: 3, shape: 'circle' }] },
      ],
    },
  },

  'EXT_G2_PP_04_007': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '▲', count: 4, shape: 'triangle' }], right: [{ label: '●', count: 2, shape: 'circle' }] },
      ],
    },
  },

  'EXT_G3_MF_2009_014': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '●', count: 3 }], right: [{ label: '▲', count: 2 }] },
        { left: [{ label: '▲', count: 1 }], right: [{ label: '■', count: 4 }] },
      ],
    },
  },

  'EXT_G3_MF_2010_010': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '●', count: 2 }], right: [{ label: '▲', count: 3 }] },
        { left: [{ label: '▲', count: 1 }], right: [{ label: '■', count: 2 }] },
      ],
    },
  },

  'EXT_G3_MF_2011_014': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '★', count: 1, shape: 'star' }], right: [{ label: '●', count: 5 }] },
        { left: [{ label: '●', count: 1 }], right: [{ label: '▲', count: 3 }] },
      ],
    },
  },

  'EXT_G4_FP_2017_008': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '●', count: 4, shape: 'circle' }], right: [{ label: '■', count: 2, shape: 'square' }] },
        { left: [{ label: '■', count: 1, shape: 'square' }], right: [{ label: '▲', count: 3, shape: 'triangle' }] },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // COUNTING TRIANGLES / SQUARES
  // ═══════════════════════════════════════════════════════════════════════

  // "Count the number of triangles in the figure" → answer 8
  'EXT_G2_PP_01_038': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 2, answer: 8 },
  },

  // "How many squares are there?" → answer 5
  'EXT_G2_PP_01_049': {
    type: 'triangle',
    props: {
      variant: 'countSquares',
      answer: 5,
      vertices: [
        { x: 40, y: 40 }, { x: 160, y: 40 },
        { x: 160, y: 160 }, { x: 40, y: 160 },
        { x: 100, y: 100 },
      ],
    },
  },

  'EXT_G2_PP_02_036': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 2, answer: 8 },
  },

  'EXT_G2_PP_04_030': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 3, answer: 13 },
  },

  'EXT_G2_PP_06_008': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 2, answer: 8 },
  },

  'EXT_G2_PP_06_022': {
    type: 'triangle',
    props: { variant: 'countSquares', answer: 5 },
  },

  'EXT_G2_PP_07_024': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 2, answer: 8 },
  },

  'EXT_G3_MF_2018_001': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 3, answer: 13 },
  },

  'EXT_G4_FP_2017_010': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 3, answer: 13 },
  },

  'EXT_G4_FP_2021_037': {
    type: 'triangle',
    props: { variant: 'countTriangles', subdivisions: 4, answer: 27 },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // COMPOSITE SHAPES
  // ═══════════════════════════════════════════════════════════════════════

  // "In the diagram, area of quadrilateral EDIF..." → compound rectangles
  'EXT_G9_MF_2022_002': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 20, y: 20, width: 80, height: 60, label: 'EDIF', shaded: true },
        { x: 100, y: 20, width: 80, height: 60, label: 'GIAH', shaded: true },
        { x: 20, y: 20, width: 240, height: 120, label: 'ABCD' },
      ],
      dimensions: [
        { x1: 20, y1: 85, x2: 100, y2: 85, label: 'ED = (x+2)' },
        { x1: 100, y1: 85, x2: 180, y2: 85, label: 'AH = (2x−1)' },
        { x1: 20, y1: 145, x2: 260, y2: 145, label: 'AB = ?' },
      ],
    },
  },

  // "Shaded area=162cm². Find perimeter of square" → answer 72cm
  'EXT_G6_FP_2021_031': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 20, width: 200, height: 120, label: '' },
        { x: 80, y: 40, width: 120, height: 80, label: '', shaded: true },
      ],
      dimensions: [
        { x1: 40, y1: 145, x2: 240, y2: 145, label: 'side = ?' },
      ],
    },
  },

  // "Two rectangles PQRS and KLMN. Shaded area" → answer 52
  'EXT_G6_FP_2022_021': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 20, y: 20, width: 200, height: 100, label: 'PQRS' },
        { x: 80, y: 40, width: 100, height: 60, label: 'KLMN', shaded: true },
      ],
      dimensions: [
        { x1: 20, y1: 125, x2: 220, y2: 125, label: '10 cm' },
        { x1: 225, y1: 20, x2: 225, y2: 120, label: '8 cm' },
      ],
    },
  },

  // Grade 6 — "PQRS square, ABCD rectangle. Shaded area?" → answer 32
  'EXT_G6_FP_2017_023': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 20, width: 120, height: 120, label: 'PQRS' },
        { x: 80, y: 40, width: 160, height: 80, label: 'ABCD' },
        { x: 40, y: 20, width: 40, height: 120, shaded: true },
      ],
      dimensions: [
        { x1: 80, y1: 125, x2: 240, y2: 125, label: 'AD = 2' },
      ],
    },
  },

  // "Squares joined. Un-shaded area?" → answer 3
  'EXT_G6_FP_2020_005': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 40, width: 80, height: 80, label: '' },
        { x: 120, y: 60, width: 60, height: 60, label: '' },
        { x: 40, y: 40, width: 80, height: 80, shaded: true },
      ],
      dimensions: [
        { x1: 40, y1: 125, x2: 120, y2: 125, label: '3' },
        { x1: 120, y1: 125, x2: 180, y2: 125, label: '√3' },
      ],
    },
  },

  // Grade 2 composite shape questions
  'EXT_G2_PP_02_035': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 20, width: 60, height: 120, label: '' },
        { x: 100, y: 60, width: 120, height: 80, label: '' },
      ],
      dimensions: [
        { x1: 40, y1: 145, x2: 220, y2: 145, label: '' },
      ],
    },
  },

  'EXT_G2_PP_04_024': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 20, width: 200, height: 40, label: '' },
        { x: 100, y: 60, width: 80, height: 80, label: '' },
      ],
      dimensions: [],
    },
  },

  // Grade 4 composite
  'EXT_G4_FP_2017_028': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 20, width: 80, height: 120, label: '' },
        { x: 120, y: 60, width: 100, height: 80, label: '' },
      ],
      dimensions: [
        { x1: 40, y1: 145, x2: 120, y2: 145, label: '4 cm' },
        { x1: 120, y1: 145, x2: 220, y2: 145, label: '5 cm' },
        { x1: 225, y1: 60, x2: 225, y2: 140, label: '4 cm' },
        { x1: 35, y1: 20, x2: 35, y2: 140, label: '6 cm' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PATTERNS
  // ═══════════════════════════════════════════════════════════════════════

  // "Series figure pattern: 1997th place?" → answer ψ
  'EXT_G6_FP_2016_007': {
    type: 'pattern',
    props: { variant: 'symbols', sequence: ['ψ', '♣', '♦', '♥'], showQuestion: true },
  },

  // "What symbol will come in 349th place: ♥♣♦♣□▲..." → answer ♣
  'EXT_G6_FP_2025_040': {
    type: 'pattern',
    props: { variant: 'symbols', sequence: ['♥', '♣', '♦', '♣', '□', '▲'], showQuestion: true },
  },

  // Grade 2 pattern questions
  'EXT_G2_PP_01_025': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['●', '■', '▲', '●', '■', '▲', '?'], showQuestion: true },
  },
  'EXT_G2_PP_02_028': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['▲', '■', '●', '▲', '■', '●', '?'], showQuestion: true },
  },
  'EXT_G2_PP_04_006': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['■', '●', '▲', '■', '●', '?'], showQuestion: true },
  },
  'EXT_G2_PP_05_005': {
    type: 'pattern',
    props: { variant: 'dots', sequence: ['1', '3', '6', '10', '?'], showQuestion: true },
  },
  'EXT_G2_PP_07_017': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['●', '●', '■', '●', '●', '■', '?'], showQuestion: true },
  },

  // Grade 3 pattern questions
  'EXT_G3_MF_2014_004': {
    type: 'pattern',
    props: { variant: 'blocks', sequence: ['1', '4', '9', '?'], showQuestion: true },
  },
  'EXT_G3_MF_2015_001': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['▲', '▲■', '▲■●', '?'], showQuestion: true },
  },
  'EXT_G3_MF_2015_009': {
    type: 'pattern',
    props: { variant: 'blocks', sequence: ['1', '3', '6', '10', '?'], showQuestion: true },
  },
  'EXT_G3_MF_2018_008': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['●', '●●', '●●●', '?'], showQuestion: true },
  },
  'EXT_G3_MF_2019_006': {
    type: 'pattern',
    props: { variant: 'blocks', sequence: ['2', '6', '12', '20', '?'], showQuestion: true },
  },
  'EXT_G3_MF_2019_015': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['■', '■■', '■■■', '?'], showQuestion: true },
  },
  'EXT_G3_MF_2024_009': {
    type: 'pattern',
    props: { variant: 'blocks', sequence: ['1', '5', '13', '25', '?'], showQuestion: true },
  },
  'EXT_G4_WS2_CH16_016': {
    type: 'pattern',
    props: { variant: 'shapes', sequence: ['◇', '◇◇', '◇◇◇', '?'], showQuestion: true },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // MIRROR / SYMMETRY
  // ═══════════════════════════════════════════════════════════════════════

  // "Which figure is symmetrical?" → answer D (P & Q)
  'EXT_G2_PP_01_019': {
    type: 'mirror',
    props: { variant: 'symmetry', content: 'P Q R', axis: 'vertical' },
  },

  // "Which figure will look as it is in the mirror?" → answer C (↑)
  'EXT_G2_PP_01_039': {
    type: 'mirror',
    props: { variant: 'arrow', content: '↗ ↙ ↑ →', axis: 'vertical' },
  },

  // "If you look at APC in the mirror, it will look like:" → answer A
  'EXT_G2_PP_02_023': {
    type: 'mirror',
    props: { variant: 'letter', content: 'APC', axis: 'vertical' },
  },

  'EXT_G2_PP_05_004': {
    type: 'mirror',
    props: { variant: 'shape', content: 'L-shape', axis: 'vertical' },
  },

  'EXT_G2_PP_05_026': {
    type: 'mirror',
    props: { variant: 'letter', content: 'BCDEHIKOX', axis: 'vertical' },
  },

  'EXT_G2_PP_06_026': {
    type: 'mirror',
    props: { variant: 'shape', content: 'T-shape', axis: 'horizontal' },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CLOCK
  // ═══════════════════════════════════════════════════════════════════════

  'EXT_G2_PP_02_038': {
    type: 'clock',
    props: { hour: 3, minute: 30 },
  },
  'EXT_G2_PP_03_008': {
    type: 'clock',
    props: { hour: 6, minute: 0 },
  },
  'EXT_G2_PP_04_015': {
    type: 'clock',
    props: { hour: 9, minute: 15 },
  },
  'EXT_G2_PP_04_026': {
    type: 'clock',
    props: { hour: 4, minute: 30 },
  },
  'EXT_G2_PP_04_035': {
    type: 'clock',
    props: { hour: 7, minute: 45 },
  },
  'EXT_G2_PP_06_017': {
    type: 'clock',
    props: { hour: 10, minute: 10 },
  },
  'EXT_G3_MF_2012_011': {
    type: 'clock',
    props: { hour: 5, minute: 25 },
  },
  'EXT_G3_MF_2015_006': {
    type: 'clock',
    props: { hour: 8, minute: 40 },
  },
  'EXT_G3_MF_2015_011': {
    type: 'clock',
    props: { hour: 2, minute: 50 },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // NUMBER LINE
  // ═══════════════════════════════════════════════════════════════════════

  'EXT_G6_FP_2020_002': {
    type: 'numberLine',
    props: {
      min: -8, max: 10, step: 2,
      points: [
        { value: -6, label: 'a' },
        { value: -2, label: 'b' },
        { value: 1, label: 'c' },
        { value: 7, label: 'd' },
      ],
    },
  },

  'EXT_G3_MF_2009_006': {
    type: 'numberLine',
    props: {
      min: 0, max: 20, step: 5,
      points: [
        { value: 3, label: 'A' },
        { value: 8, label: 'B' },
        { value: 14, label: 'C' },
      ],
    },
  },

  'EXT_G5_WS_B7_008': {
    type: 'numberLine',
    props: {
      min: 0, max: 1, step: 0.25,
      points: [
        { value: 0.25, label: 'P' },
        { value: 0.5, label: 'Q' },
        { value: 0.75, label: 'R' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // 3D BLOCKS
  // ═══════════════════════════════════════════════════════════════════════

  // "This 3D figure is made up of ___ blocks" → answer 8
  'EXT_G2_PP_01_010': {
    type: 'blocks',
    props: {
      layers: [[2, 2], [2, 2]],
      answer: 8,
    },
  },

  // Grade 2 block counting
  'EXT_G2_PP_03_002': {
    type: 'blocks',
    props: {
      layers: [[3, 2], [2, 1]],
      answer: 8,
    },
  },

  // Grade 6 — 3D cube: 27 smaller cubes
  'EXT_G6_FP_2016_009': {
    type: 'blocks',
    props: {
      layers: [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
      answer: 27,
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // MULTIPLICATION / GROUPING FIGURES
  // ═══════════════════════════════════════════════════════════════════════

  // "Which number sentence represents the figure? 3 groups of 4 stars" → All of these
  'EXT_G2_PP_02_024': {
    type: 'pattern',
    props: { variant: 'dots', sequence: ['★★★★', '★★★★', '★★★★'], showQuestion: false },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // ABACUS
  // ═══════════════════════════════════════════════════════════════════════

  // "What number is shown on the abacus?" H=3, T=2, O=3 → 323
  'EXT_G2_PP_01_027': {
    type: 'abacus',
    props: { rods: [{ label: 'H', beads: 3 }, { label: 'T', beads: 2 }, { label: 'O', beads: 3 }] },
  },

  // "What number is shown on the abacus?" H=4, T=0, O=3 → 403
  'EXT_G2_PP_03_003': {
    type: 'abacus',
    props: { rods: [{ label: 'H', beads: 4 }, { label: 'T', beads: 0 }, { label: 'O', beads: 3 }] },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CALENDAR
  // ═══════════════════════════════════════════════════════════════════════

  // "Look at the calendar: 4th Saturday, date on 3rd Sunday" Feb 2006 starts Wed
  'EXT_G2_PP_02_031': {
    type: 'calendar',
    props: {
      month: 'February',
      year: 2006,
      startDay: 3, // Wednesday
      daysInMonth: 28,
      highlight: [25, 19], // 4th Saturday = 25th, 3rd Sunday = 19th
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CURRENCY
  // ═══════════════════════════════════════════════════════════════════════

  // "Total money in the figure?" Rs.1+Rs.2+25p+50p+25p+Rs.5 → Rs.8.75 (but answer Rs.9)
  'EXT_G2_PP_04_037': {
    type: 'currency',
    props: {
      items: [
        { type: 'coin', value: 'Rs.1' },
        { type: 'coin', value: 'Rs.2' },
        { type: 'coin', value: '25p' },
        { type: 'coin', value: '50p' },
        { type: 'coin', value: '25p' },
        { type: 'note', value: 'Rs.5' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // NUMBER GRID
  // ═══════════════════════════════════════════════════════════════════════

  // "Find the missing number in the grid" — magic square / pattern grid
  'EXT_G3_MF_2018_009': {
    type: 'numberGrid',
    props: {
      grid: [
        ['6', '7', '2'],
        ['1', '5', '9'],
        ['8', '3', '?'],
      ],
      unknownLabel: '?',
    },
  },

  // "Find the missing number" — pattern grid
  'EXT_G4_FP_2022_028': {
    type: 'numberGrid',
    props: {
      grid: [
        ['3', '5', '7'],
        ['4', '?', '10'],
        ['5', '7', '9'],
      ],
      unknownLabel: '?',
    },
  },

  // "Find the missing number" — pattern grid
  'EXT_G4_FP_2023_029': {
    type: 'numberGrid',
    props: {
      grid: [
        ['2', '9', '4'],
        ['7', '5', '3'],
        ['6', '1', '?'],
      ],
      unknownLabel: '?',
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // TETROMINO
  // ═══════════════════════════════════════════════════════════════════════

  // "Which shape has smallest perimeter?" I/L/O/S tetrominoes
  'EXT_G3_MF_2022_004': {
    type: 'tetromino',
    props: {
      figures: [
        { cells: [[0, 0], [0, 1], [0, 2], [0, 3]], label: 'A (I)' },
        { cells: [[0, 0], [1, 0], [2, 0], [2, 1]], label: 'B (L)' },
        { cells: [[0, 0], [0, 1], [1, 0], [1, 1]], label: 'C (O)' },
        { cells: [[0, 1], [0, 2], [1, 0], [1, 1]], label: 'D (S)' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // POLYGON
  // ═══════════════════════════════════════════════════════════════════════

  // "Pentagon with algebraic side expressions, find perimeter"
  'EXT_G6_FP_2023_019': {
    type: 'polygon',
    props: {
      sides: 5,
      labels: [
        { text: '2x+3', side: 0 },
        { text: 'x+7', side: 1 },
        { text: '3x−1', side: 2 },
        { text: '2x+1', side: 3 },
        { text: 'x+5', side: 4 },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // HEIGHTS & DISTANCE
  // ═══════════════════════════════════════════════════════════════════════

  // "200m cliff, angles 30° depression and 60° elevation to tower top/bottom"
  'EXT_G9_MF_2023_007': {
    type: 'heightsDistance',
    props: {
      variant: 'cliff-tower',
      heights: { cliff: 200, tower: undefined },
      angles: [30, 60],
      labels: { cliff: '200m' },
    },
  },

  // "Rock, boat at 30° depression moves to 60° depression"
  'EXT_G9_MF_2024_009': {
    type: 'heightsDistance',
    props: {
      variant: 'cliff-boat',
      heights: { cliff: 0 },
      angles: [30, 60],
      labels: { cliff: 'h', boat1: 'B', boat2: 'C' },
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // ADDITIONAL BALANCE MAPPINGS (existing component)
  // ═══════════════════════════════════════════════════════════════════════

  // "3 balanced scales with shapes → solve 4th" answer 28g
  'EXT_G3_MF_2013_001': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '●', count: 2, shape: 'circle' }], right: [{ label: '▲', count: 1, shape: 'triangle' }] },
        { left: [{ label: '▲', count: 1, shape: 'triangle' }], right: [{ label: '■', count: 3, shape: 'square' }] },
        { left: [{ label: '■', count: 1, shape: 'square' }], right: [{ label: '★', count: 2, shape: 'star' }] },
      ],
    },
  },

  // "3 balanced scales with shapes → solve 4th" answer 18g
  'EXT_G3_MF_2020_014': {
    type: 'balance',
    props: {
      scales: [
        { left: [{ label: '●', count: 3, shape: 'circle' }], right: [{ label: '▲', count: 1, shape: 'triangle' }] },
        { left: [{ label: '▲', count: 2, shape: 'triangle' }], right: [{ label: '■', count: 3, shape: 'square' }] },
        { left: [{ label: '■', count: 1, shape: 'square' }], right: [{ label: '★', count: 2, shape: 'star' }] },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // ADDITIONAL COMPOSITE SHAPE MAPPING (existing component)
  // ═══════════════════════════════════════════════════════════════════════

  // "Grid of 1cm squares, irregular shape, find perimeter" → 29cm
  'EXT_G3_MF_2014_007': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 40, y: 20, width: 120, height: 40, label: '' },
        { x: 40, y: 60, width: 80, height: 40, label: '' },
        { x: 40, y: 100, width: 40, height: 40, label: '' },
      ],
      dimensions: [
        { x1: 40, y1: 145, x2: 160, y2: 145, label: '6 cm' },
        { x1: 35, y1: 20, x2: 35, y2: 140, label: '6 cm' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CLOCK — angle-between-hands questions (existing component)
  // ═══════════════════════════════════════════════════════════════════════

  // "Angle between hour and minute hand at 9:30" → obtuse
  'EXT_G3_MF_2008_015': {
    type: 'clock',
    props: { hour: 9, minute: 30 },
  },

  // "Angle between hands at 9:20pm?" → obtuse
  'EXT_G3_MF_2020_013': {
    type: 'clock',
    props: { hour: 9, minute: 20 },
  },

  // "At half past six, angle between hour and minute hand?" → 15°
  'EXT_G4_FP_2020_033': {
    type: 'clock',
    props: { hour: 6, minute: 30 },
  },

  // "Angle between hour and minute hand at 8:30 am?" → 75°
  'EXT_G4_FP_2023_034': {
    type: 'clock',
    props: { hour: 8, minute: 30 },
  },

  // "Angle between hour and minute hand at 7:20 pm?" → 100°
  'EXT_G4_FP_2024_017': {
    type: 'clock',
    props: { hour: 7, minute: 20 },
  },

  // "Angle between hour and minute at 18 minutes past 5?" → 57°
  'EXT_G4_FP_2025_013': {
    type: 'clock',
    props: { hour: 5, minute: 18 },
  },

  // "Clock started at 4pm. Degrees hour hand rotates to 8:53pm?" → 146.5°
  'EXT_G9_MF_2022_010': {
    type: 'clock',
    props: { hour: 4, minute: 0 },
  },

  // "Angle between hour and minute hand at 2:31?" → 110.5°
  'EXT_G9_MF_2023_014': {
    type: 'clock',
    props: { hour: 2, minute: 31 },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // ABACUS — additional mappings (existing component)
  // ═══════════════════════════════════════════════════════════════════════

  // "1 bead added to one's place on abacus H=3,T=2,O=5 → carry to ten's"
  'EXT_G2_PP_01_044': {
    type: 'abacus',
    props: { rods: [{ label: 'H', beads: 3 }, { label: 'T', beads: 2 }, { label: 'O', beads: 5 }] },
  },

  // "Abacus shows number ___" → 241 (H=2, T=4, O=1)
  'EXT_G2_PP_06_004': {
    type: 'abacus',
    props: { rods: [{ label: 'H', beads: 2 }, { label: 'T', beads: 4 }, { label: 'O', beads: 1 }] },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // BLOCKS — staircase (existing component)
  // ═══════════════════════════════════════════════════════════════════════

  // "3-step staircase with 6 blocks. How many for 7-step?" → 28
  'EXT_G3_MF_2013_006': {
    type: 'blocks',
    props: {
      layers: [[3], [2], [1]],
      answer: 6,
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // COMPOSITE SHAPE — PYQ figures (existing component)
  // ═══════════════════════════════════════════════════════════════════════

  // "Rectangle 4cm×1cm cut into 4 pieces (1cm squares). Perimeter diff?" → 6cm
  'PYQ_2016_Q24': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 60, y: 50, width: 40, height: 40, label: '' },
        { x: 100, y: 50, width: 40, height: 40, label: '' },
        { x: 140, y: 50, width: 40, height: 40, label: '' },
        { x: 180, y: 50, width: 40, height: 40, label: '' },
      ],
      dimensions: [
        { x1: 60, y1: 95, x2: 220, y2: 95, label: '4 cm' },
        { x1: 55, y1: 50, x2: 55, y2: 90, label: '1 cm' },
      ],
    },
  },

  // "3 squares (side 9cm) joined by edges → perimeter of rectangle?" → 72cm
  'PYQ_2019_Q30': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 20, y: 30, width: 80, height: 80, label: '' },
        { x: 100, y: 30, width: 80, height: 80, label: '' },
        { x: 180, y: 30, width: 80, height: 80, label: '' },
      ],
      dimensions: [
        { x1: 20, y1: 115, x2: 100, y2: 115, label: '9 cm' },
        { x1: 100, y1: 115, x2: 180, y2: 115, label: '9 cm' },
        { x1: 180, y1: 115, x2: 260, y2: 115, label: '9 cm' },
        { x1: 265, y1: 30, x2: 265, y2: 110, label: '9 cm' },
      ],
    },
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PICTOGRAPH
  // ═══════════════════════════════════════════════════════════════════════

  // "How old is Nupur?" → 6 candles pictograph → answer 6 years
  'EXT_G2_PP_01_012': {
    type: 'pictograph',
    props: { icon: 'candle', count: 6, label: "Nupur's birthday cake" },
  },
};
