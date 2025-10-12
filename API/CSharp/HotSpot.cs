using System.Collections.Generic;

namespace YumStudio.API;

public partial class HotSpot<T>
{
  private readonly List<Flow<T>> flows = [];

  /// <summary>
  /// Given parameter will be registered and called by the HotSpot when HotSpot<T>.Fire(T args) is called.
  /// </summary>
  /// <param name="flow"></param>
  public void Subscribe(Flow<T> flow) => flows.Add(flow);

  /// <summary>
  /// Removes all flows with the given name.
  /// </summary>
  /// <param name="name"></param>
  public void Unsubscribe(string name)
  {
    foreach (var flow in flows) if (flow.Name == name) flows.Remove(flow);
  }

  /// <summary>
  /// Calls all subscribed flows, with given arg.
  /// </summary>
  /// <param name="arg"></param>
  public void Fire(T arg)
  {
    foreach (var flow in flows) flow.Call(arg);
  }
}

public partial class HotSpot
{
  private readonly List<Flow> flows = [];

  /// <summary>
  /// Given parameter will be registered and called by the HotSpot when HotSpot<T>.Fire(T args) is called.
  /// </summary>
  public void Subscribe(Flow flow) => flows.Add(flow);

  /// <summary>
  /// Removes all flows with the given name.
  /// </summary>
  public void Unsubscribe(string name)
  {
    foreach (var flow in flows) if (flow.Name == name) flows.Remove(flow);
  }

  /// <summary>
  /// Calls all subscribed flows, with given arg.
  /// </summary>
  public void Fire()
  {
    foreach (var flow in flows) flow.Call();
  }
}