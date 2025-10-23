using Godot;
using System;
using System.IO;
using System.Linq;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core.Engine.Editor.ProjectEditor;

public partial class EditorViewport : Control
{
  public string ProjectPath { get; protected set; }

  public EditorViewport(string path) { ProjectPath = path; }
  public EditorViewport() { }

  public virtual void Destroy()
  {
    foreach (var child in GetChildren()) child.QueueFree();
  }

  public override void _ExitTree() => Destroy();
}

public partial class ProjectEditorView : Control
{
  private string projectPath = ""; // Path to the project

  public ProjectEditorView() { }
  public ProjectEditorView(string path) { Open(path); }

  private HBoxContainer menubar = new();
  private VSplitContainer viewports = new();

  public override void _Ready()
  {
    AddChild(menubar);
    AddChild(viewports);
    menubar.AnchorBottom = 0.059f;
    menubar.AnchorRight = 1f;
    viewports.AnchorTop = 0.059f;
    viewports.AnchorRight = 1f;
    viewports.AnchorBottom = 1f;
  }

  public void Open(string path)
  {
    Output.Info($"Opening editor at {path}");
    if (!Directory.Exists(path)) throw new FileNotFoundException($"No such project file {path}");

    projectPath = path;

    var types = YumStudioEngine.GetEngineAssembly()
      .Where(t => t.IsAssignableTo(typeof(EditorViewport)))
      .Where(t => t != typeof(EditorViewport))
      .ToList();

    // TODO: fix and add if user wants
    foreach (var type in types)
    {
      var instance = (EditorViewport)Activator.CreateInstance(type, [projectPath]);
      viewports.AddChild(instance);
    }
  }

  public static Window NewProjectEditor(string projname, string projpath)
  {
    Window win = new()
    {
      Size = new(1200, 1000),
      Title = $"YumStudio — {projname} • {projpath}",
    };

    win.Connect("close_requested", Callable.From(win.QueueFree));

    var editor = new ProjectEditorView();
    editor.SetAnchorsPreset(LayoutPreset.FullRect);
    editor.Open(projpath);
    win.AddChild(editor);

    return win;
  }
}
