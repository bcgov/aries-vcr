/* SystemJS module definition */
declare var module: NodeModule;
interface NodeModule {
  id: string;
}

/* Required for translation loader (class provided by webpack) */
declare var System: System;
interface System {
  import(request: string): Promise<any>;
}
