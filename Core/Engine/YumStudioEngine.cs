using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;

namespace YumStudio.Core.Engine;

/// <summary>
/// Static class that provides helpers and methods in order to communicate with the engine.
/// </summary>
public class YumStudioEngine
{
  public static readonly string ConfigFile = Path.Combine(AppContext.BaseDirectory, "yum-studio.yso");
  public static readonly string ConfigFileHeader = "; YumStudio internal file\n; Prefer using YumStudio.Editor in order to modify this.\n";
  public static readonly int MainThreadId = Environment.CurrentManagedThreadId;

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

  public static void MainThreadLockGuard()
  {
    if (Environment.CurrentManagedThreadId != MainThreadId)
      throw new InvalidOperationException("This method must be called from the main thread!");
  }

}