using Godot;
using System;
using System.Linq;
using System.Reflection;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core.Engine.Entry;

[AttributeUsage(AttributeTargets.Class)]
public class OnEngineReadyAttribute : Attribute { }

public partial class EngineEntry : Node // bro what
{
  public override void _Ready()
  {
    var readyTypes = AppDomain.CurrentDomain.GetAssemblies()
    .SelectMany(a => a.GetTypes())
    .Where(t => t.GetCustomAttribute<OnEngineReadyAttribute>() != null)
    .ToList();

    foreach (var type in readyTypes)
    {
      var instance = Activator.CreateInstance(type);
      try
      {
        Output.Info($"[{GetType().Name}]: initializing {type.FullName}");
        type.GetMethod("Enter")?.Invoke(instance, null);
      } catch (Exception e) 
      {
        Output.Error($"Failled to init {type.FullName}", e.ToString());
      }
    }

  }
}