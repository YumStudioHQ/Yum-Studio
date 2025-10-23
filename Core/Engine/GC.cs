using System;
using System.Collections.Concurrent;
using Godot;
using YumStudio.Core.Engine.Cycles;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core.Engine;

/// <summary>
/// Each objects hold in YumStudioEngine's GC derives from Collectable.
/// </summary>
public class Collectable
{
  public virtual void Free() { }
}

public class PromotedCollectable : Collectable
{
  protected object handle;
  protected Action onFree = () => { };

  public override void Free()
  {
    onFree();
  }

  public PromotedCollectable() { handle = null; }

  public PromotedCollectable(object o, Action free)
  {
    handle = o;
    onFree = free;
  }
}

public class CollectableNode : Collectable
{
  public Node Node { get; set; }

  public CollectableNode() => Node = new();
  public override void Free() => Node.QueueFree();

  public CollectableNode(Type type)
    => Node = (Node)Activator.CreateInstance(type);

  public static CollectableNode From<T>() where T : Node => new(typeof(T));
}

/// <summary>
/// YumStudio Engine's common Garbage Collector.
/// </summary>
[OnEngineShutdown]
public class GC
{
  private static readonly ConcurrentBag<WeakReference<Collectable>> Instances = [];

  public static PromotedCollectable Allocate()
  {
    var i = new PromotedCollectable();
    Instances.Add(new WeakReference<Collectable>(i));
    return i;
  }

  public static CollectableNode GetNode(Type type)
  {
    var n = new CollectableNode(type);
    Instances.Add(new WeakReference<Collectable>(n));
    return n;
  }

  public static void Promote(object o, Action free)
  {
    Instances.Add(new WeakReference<Collectable>(new PromotedCollectable(o, free)));
  }

  private void OnEngineShutdown()
  {
    int freed = 0;
    foreach (var instance in Instances)
    {
      if (instance.TryGetTarget(out Collectable tar) && tar != null)
      {
        try
        {
          tar.Free();
        }
        catch (Exception e)
        {
          Output.Error($"Exception caught {e.Message}");
        }
        freed++;
      }
    }
    Output.Info($"[{GetType().FullName}]: freed {freed} objects");
  }
}

/// <summary>
/// Represents any Godot.Node in the Engine's GC.
/// </summary>
/// <typeparam name="T">Node type</typeparam>
public partial class SafeNode<T> : Node where T : Node
{
  public SafeNode()
  {
    GC.Promote(this, QueueFree);
  }
}