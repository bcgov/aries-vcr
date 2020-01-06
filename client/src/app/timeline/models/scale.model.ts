export type scaleOpts = 1 | 2 | 3 | 4;

export function timelineScale(start: Date, end: Date) {
  const scale = end.getFullYear() - start.getFullYear();
  return scale < 2 ? 1 : 2;
}
