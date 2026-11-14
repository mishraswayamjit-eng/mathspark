'use client';

import React from 'react';
import type { FigureSpec } from '@/lib/figures/types';
import { TriangleKind, RectangleKind, PolygonKind, CircleKind, GridKind } from './kinds/geometry';
import { AnglesKind, ClockKind, CompassKind } from './kinds/turning';
import { FractionBarsKind, SetKind, BarModelKind, NumberLineKind, PlaceChartKind, FactorTreeKind } from './kinds/number';
import { JourneyKind, BarChartKind, TableKind, VennKind, BalanceKind } from './kinds/data';

export interface FigureViewProps {
  /** The figure to draw. Already validated offline; draw it as given. */
  spec: FigureSpec;
  /** Extra classes for the outer element. */
  className?: string;
}

function draw(spec: FigureSpec, className: string | undefined): React.ReactElement | null {
  switch (spec.kind) {
    case 'triangle': return <TriangleKind spec={spec} className={className} />;
    case 'rectangle': return <RectangleKind spec={spec} className={className} />;
    case 'polygon': return <PolygonKind spec={spec} className={className} />;
    case 'circle': return <CircleKind spec={spec} className={className} />;
    case 'grid': return <GridKind spec={spec} className={className} />;
    case 'angles': return <AnglesKind spec={spec} className={className} />;
    case 'clock': return <ClockKind spec={spec} className={className} />;
    case 'compass': return <CompassKind spec={spec} className={className} />;
    case 'fractionBars': return <FractionBarsKind spec={spec} className={className} />;
    case 'set': return <SetKind spec={spec} className={className} />;
    case 'barModel': return <BarModelKind spec={spec} className={className} />;
    case 'numberLine': return <NumberLineKind spec={spec} className={className} />;
    case 'placeChart': return <PlaceChartKind spec={spec} className={className} />;
    case 'factorTree': return <FactorTreeKind spec={spec} className={className} />;
    case 'journey': return <JourneyKind spec={spec} className={className} />;
    case 'barChart': return <BarChartKind spec={spec} className={className} />;
    case 'table': return <TableKind spec={spec} className={className} />;
    case 'venn': return <VennKind spec={spec} className={className} />;
    case 'balance': return <BalanceKind spec={spec} className={className} />;
    default: return null;
  }
}

interface GuardProps { spec: FigureSpec; children: React.ReactNode }
interface GuardState { broken: boolean }

/** A figure that cannot be drawn shows nothing, and never takes the screen down with it. */
class FigureGuard extends React.Component<GuardProps, GuardState> {
  state: GuardState = { broken: false };

  static getDerivedStateFromError(): GuardState {
    return { broken: true };
  }

  componentDidUpdate(prev: GuardProps) {
    if (this.state.broken && prev.spec !== this.props.spec) this.setState({ broken: false });
  }

  render() {
    return this.state.broken ? null : this.props.children;
  }
}

/**
 * Draws one question figure: a still picture, never interactive, with nothing
 * on it that the spec does not state. The drawing code for each kind lives in
 * `./kinds/`. An unrecognised kind draws nothing.
 */
export default function FigureView({ spec, className }: FigureViewProps) {
  if (!spec || typeof spec !== 'object') return null;
  return <FigureGuard spec={spec}>{draw(spec, className)}</FigureGuard>;
}
