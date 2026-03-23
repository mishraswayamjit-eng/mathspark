/** Map topicName → accent color for card left border */
export function getTopicColor(topicName: string): string {
  const lower = topicName.toLowerCase();
  if (lower.includes('number') || lower.includes('arithmetic') || lower.includes('place value'))
    return '#34D399'; // emerald
  if (lower.includes('algebra') || lower.includes('equation') || lower.includes('expression'))
    return '#60A5FA'; // sky blue
  if (lower.includes('geometry') || lower.includes('angle') || lower.includes('triangle') || lower.includes('quadrilateral') || lower.includes('circle'))
    return '#A78BFA'; // purple
  if (lower.includes('fraction') || lower.includes('decimal'))
    return '#F472B6'; // pink
  if (lower.includes('measurement') || lower.includes('time') || lower.includes('calendar') || lower.includes('unit'))
    return '#FBBF24'; // amber
  if (lower.includes('data') || lower.includes('statistic') || lower.includes('graph'))
    return '#2DD4BF'; // teal
  if (lower.includes('percent') || lower.includes('interest') || lower.includes('ratio') || lower.includes('profit'))
    return '#FB923C'; // orange
  if (lower.includes('mental') || lower.includes('warm') || lower.includes('speed') || lower.includes('puzzle') || lower.includes('magic'))
    return '#E879F9'; // fuchsia
  if (lower.includes('factor') || lower.includes('multiple') || lower.includes('hcf') || lower.includes('lcm'))
    return '#34D399'; // emerald
  if (lower.includes('bodmas') || lower.includes('operation') || lower.includes('sequence'))
    return '#60A5FA'; // sky blue
  return '#94A3B8'; // default gray
}
