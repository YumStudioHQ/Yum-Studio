using System;
using System.Collections.Generic;
using Godot;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core;

public partial class TaskPipeline : Node
{
  private readonly List<KeyValuePair<string, Action>> actions = [];

  public void Fire(bool verbose = true)
  {
    for (int i = 0; i < actions.Count; i++)
    {
      if (verbose) Output.Log($"[{i+1}/{actions.Count+1}]: {actions[i].Key}");
      actions[i].Value();
    }
  }

  public void Add(string name, Action action) => actions.Add(new(name, action));

  public TaskPipeline() {}
  public TaskPipeline(List<KeyValuePair<string, Action>> _actions)
  {
    actions = _actions;
  }
}