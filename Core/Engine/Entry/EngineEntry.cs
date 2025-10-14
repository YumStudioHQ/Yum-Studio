using Godot;
using System;
using System.Linq;
using System.Reflection;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.Engine.Cycles;

namespace YumStudio.Core.Engine.Entry;

public static class EngineAttributeProcessor
{
  public static void Run<TAttribute>(string methodName) where TAttribute : Attribute
  {
    var types = AppDomain.CurrentDomain.GetAssemblies()
        .SelectMany(a =>
        {
          try { return a.GetTypes(); }
          catch (ReflectionTypeLoadException ex) { return ex.Types.Where(t => t != null)!; }
        })
        .Where(t => t.GetCustomAttribute<TAttribute>() != null)
        .ToList();

    foreach (var type in types)
    {
      try
      {
        var instance = Activator.CreateInstance(type);
        Output.Info($"[{typeof(TAttribute).Name}]: initializing {type.FullName}");
        type.GetMethod(methodName, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
            ?.Invoke(instance, null);
      }
      catch (Exception e)
      {
        Output.Error($"Failed to process {type.FullName}", e.ToString());
      }
    }
  }
}

public partial class EngineEntry : Node
{
  public override void _Ready()
  {
    EngineAttributeProcessor.Run<OnEngineReadyAttribute>("Init");
    EngineAttributeProcessor.Run<OnEditorReadyAttribute>("Init");
    EngineAttributeProcessor.Run<OnYumStudioReadyAttribute>("Init");
  }

  public override void _ExitTree()
  {
    EngineAttributeProcessor.Run<OnEngineShutdownAttribute>("Shutdown");
  }
}