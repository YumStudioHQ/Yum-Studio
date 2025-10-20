using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Reflection.Metadata.Ecma335;
using Godot;

namespace YumStudio.Core.Engine;

public static class YumStudioEngine
{
  public static readonly string ConfigFile = Path.Combine(AppContext.BaseDirectory, "yum-studio.yso");
  public static readonly string ConfigFileHeader = "; YumStudio internal file\n; Prefer using YumStudio.Editor in order to modify this.\n";

  public static List<Type> GetEngineAssembly()
  {
    return [
      ..AppDomain.CurrentDomain.GetAssemblies()
        .SelectMany(a =>
        {
          try { return a.GetTypes(); }
          catch (ReflectionTypeLoadException ex) { return ex.Types.Where(t => t != null)!; }
        })
    ];
  }
}