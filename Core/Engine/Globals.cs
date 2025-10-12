using System;
using System.IO;

namespace YumStudio.Core.Engine;

public static class Globals
{
  public static readonly string ConfigFile = Path.Combine(Environment.CurrentDirectory, "yum-studio.yso");
  public static readonly string ConfigFileHeader = "; YumStudio internal file\n; Prefer using YumStudio.Editor in order to modify this.\n";
}