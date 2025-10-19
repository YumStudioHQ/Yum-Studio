using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Godot;
using YumStudio.Core.Engine.Cycles;

namespace YumStudio.Core.Engine.Editor.ProjectEditor.Views;

[OnEditorReady]
public partial class FileExplorerView : EditorViewport
{
  public partial class FileEntry : TextureButton
  {
    public string Path { get; private set; }
    public virtual string GetExtension() { return ""; }

    protected virtual void OnButtonPressed() { }

    private void Init()
    {
      Connect("pressed", new Callable(this, nameof(OnButtonPressed)));
    }

    public FileEntry(string path) { Path = path; Init(); }
    public FileEntry() { Init(); }
  }

  public partial class DirectoryEntry : TextureButton
  {
    public string Path { get; private set; }

    protected virtual void OnButtonPressed() { }

    private void Init()
    {
      Connect("pressed", new Callable(this, nameof(OnButtonPressed)));
    }

    public DirectoryEntry(string path) { Path = path; Init(); }
    public DirectoryEntry() { Init(); }
  }

  // TODO?: Create instance version (copy)
  private static readonly Dictionary<string, Type> FileHandlers = []; 
  
  private ScrollContainer scroll = new();
  private GridContainer container = new();

  private void AddFile(string path)
  {
    var type = FileHandlers.GetValueOrDefault(Path.GetExtension(path), typeof(FileEntry));
    AddChild((FileEntry)Activator.CreateInstance(type, [path]));
  }

  public override void _Ready()
  {
    var dirs = Directory.GetDirectories(ProjectPath);
    var files = Directory.GetFiles(ProjectPath);

    foreach (var file in files) AddFile(file);

    AddChild(scroll);
    scroll.AddChild(container);
  }

  public static void InitEditor()
  {
    var assembly = YumStudioEngine.GetEngineAssembly();
    var fileTypes = assembly
                   .Where(t => t.IsAssignableTo(typeof(FileEntry)))
                   .Where(t => t.IsClass && !t.IsAbstract && !t.IsSealed && t.IsPublic)
                   .ToList();

    foreach (var fileType in fileTypes)
      FileHandlers[((FileEntry)Activator.CreateInstance(fileType)).GetExtension()] = fileType;
  }
}