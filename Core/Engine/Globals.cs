using System;
using System.Collections.Generic;
using System.IO;
using YumStudio.Core.Engine.Cycles;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core.Engine;

public static class Globals
{
  public static readonly string ConfigFile = Path.Combine(AppContext.BaseDirectory, "yum-studio.yso");
  public static readonly string ConfigFileHeader = "; YumStudio internal file\n; Prefer using YumStudio.Editor in order to modify this.\n";

  public static YSObject GlobalObject { get; private set; } = GlobalInstance.GetGlobalYSO();
}

[OnEngineReady][OnEngineShutdown]
internal class GlobalInstance
{
  public static YSObject GetGlobalYSO()
  {
    if (!File.Exists(Globals.ConfigFile))
    {
      File.Create(Globals.ConfigFile).Close();
      Output.Info($"Created file {Globals.ConfigFile}");
      return new();
    }

    return YSObject.Parse(Globals.ConfigFile, true);
  }
}