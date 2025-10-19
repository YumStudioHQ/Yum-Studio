using Godot;
using System;
using System.IO;
using System.Linq;
using System.Reflection;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core.Engine.Editor.ProjectEditor;

public partial class EditorViewport : Control
{
  public string ProjectPath { get; protected set; }

  public EditorViewport(string path) { ProjectPath = path; }
  public EditorViewport() { }
}

public partial class ProjectEditor : Control
{
  private string projectPath = ""; // Path to the project's file!

  public ProjectEditor() { }
  public ProjectEditor(string path) { Open(path); }

  private HBoxContainer menubar;
  private VSplitContainer viewports;

  public override void _Ready()
  {
    menubar = GetNode<HBoxContainer>("Menubar");
    viewports = GetNode<VSplitContainer>("Viewports");
  }

  public void Open(string path)
  {
    if (!File.Exists(path)) throw new FileNotFoundException($"No such project file {path}");

    var types = YumStudioEngine.GetEngineAssembly()
      .Where(t => t.IsAssignableTo(typeof(EditorViewport)))
      .ToList();

    foreach (var type in types)
    {
      var instance = (EditorViewport)Activator.CreateInstance(type, []);
      AddChild(instance);
      Output.Info($"Editor viewport loaded: {type.FullName}");
    }
  }
}
