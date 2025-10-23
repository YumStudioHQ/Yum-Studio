using System.Collections.Generic;
using Godot;

namespace YumStudio.API.YumStudioAPI.Editor;

public class ExtensionAPI
{
  public virtual Dictionary<string, Control> GetViewports() { return []; }
  public virtual string GetName() { return ""; }
  public virtual void Free() {}
}