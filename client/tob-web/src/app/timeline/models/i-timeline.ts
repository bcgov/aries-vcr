export interface Layout {
  start?: Date;
  end?: Date;
  width?: number;
  menuPos?: string;
  rowScale?: number;
  noAnimate?: boolean;
  time?: number;
}

export interface MarkerSpec {
  classNames?: string[];
  date: Date;
  label?: string;
  link?: string;
}

export interface RowSpec {
  slots: SlotSpec[];
  classNames?: string[];
  height?: number;
}

export interface SlotSpec {
  groups: string[];
  start: Date;
  end: Date;
  htmlContent: string | (string | Node)[];
  classNames?: string[];
  url?: string;
  data?: string;
}
