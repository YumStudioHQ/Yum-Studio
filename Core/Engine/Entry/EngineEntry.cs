using Godot;
using System;
using System.Linq;
using System.Reflection;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.Engine.Cycles;

namespace YumStudio.Core.Engine.Entry;

public partial class EngineEntry : Node
{
  private static void Run<TAttribute>(
        string methodName,
        BindingFlags bindings,
        Type restrict = null,
        Action<Type, object> onInstanceCreated = null) where TAttribute : Attribute
  {
    var types = AppDomain.CurrentDomain.GetAssemblies()
        .SelectMany(a =>
        {
          try { return a.GetTypes(); }
          catch (ReflectionTypeLoadException ex) { return ex.Types.Where(t => t != null)!; }
        })
        .Where(t => t.GetCustomAttribute<TAttribute>() != null)
        .Where(t => restrict == null || t.IsAssignableTo(restrict))
        .ToList();

    foreach (var type in types)
    {
      try
      {
        var instance = Activator.CreateInstance(type);
        Output.Info($"[{typeof(TAttribute).Name}]: initializing {type.FullName}");

        onInstanceCreated?.Invoke(type, instance);

        try
        {
          type.GetMethod(methodName, bindings)
              ?.Invoke(instance, null);
        }
        catch (Exception)
        {
          throw;
        }
      }
      catch (Exception e)
      {
        Output.Error($"Failed to process {type.FullName}", e.ToString());
      }
    }
  }

  private TabContainer pages;

  public override void _Ready()
  {
    pages = GetNode<TabContainer>("Pages");
    Output.WriteLine($"{Output.Color.BrightMagenta}YumStudio — V{Version.YumStudioVersion.Full}{Output.Color.Reset}");

    Run<OnEngineReadyAttribute>("Init", BindingFlags.Instance | BindingFlags.Public);

    Run<OnEditorReadyAttribute>(
      "Init", BindingFlags.Instance | BindingFlags.Public, restrict: typeof(Node),
      onInstanceCreated: (type, instance) =>
      {
        var attr = type.GetCustomAttribute<OnEditorReadyAttribute>();

        if (instance is Node node)
        {
          node.Name = type.Name;
          pages.AddChild(node);

        }
        else
        {
          Output.Warning($"{type.FullName} has [OnEditorReady] but is not a Node!");
        }
      }
    );

    Run<OnYumStudioReadyAttribute>("Init", BindingFlags.Instance | BindingFlags.Public);
  }

  public override void _ExitTree()
  {
    Run<OnEngineShutdownAttribute>(
        "Shutdown",
        BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
    );
  }
}
