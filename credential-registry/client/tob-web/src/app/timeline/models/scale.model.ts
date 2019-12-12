export type scaleOpts = 1 | 2 | 3 | 4

export class Scale {

  constructor() {

  }
}
// This is stubbed to be a full class depending on how complex we need to be
export function timelineScale(start: Date, end: Date) {

  const scale =  end.getFullYear() - start.getFullYear()
  return scale < 10 ? 1 : 2;
}
