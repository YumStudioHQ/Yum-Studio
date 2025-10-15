using System;
using System.IO;

namespace YumStudio.Core.Engine;

public static class Globals
{
  public static readonly string ConfigFile = Path.Combine(Environment.CurrentDirectory, "yum-studio.yso");
  public static readonly string ConfigFileHeader = "; YumStudio internal file\n; Prefer using YumStudio.Editor in order to modify this.\n";

  public static Godot.Node CreateInstance(Type type)
  {
    var scenePath = $"res://{type.Namespace?.Replace('.', '/')}/{type.Name}.tscn";
    if (Godot.ResourceLoader.Exists(scenePath))
    {
      return Godot.ResourceLoader.Load<Godot.PackedScene>(scenePath).Instantiate();
    }
    else
    {
      return (Godot.Node)Activator.CreateInstance(type);
    }
  }

}