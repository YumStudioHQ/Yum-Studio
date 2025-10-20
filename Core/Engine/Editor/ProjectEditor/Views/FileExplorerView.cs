using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Godot;
using YumStudio.Core.Engine.Cycles;
using YumStudio.Core.Engine.EngineIO;

namespace YumStudio.Core.Engine.Editor.ProjectEditor.Views;

[OnEngineReady]
public partial class FileExplorerView : EditorViewport
{
#region inner classes
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
    public string Path { get; protected set; }
    protected FileExplorerView view;

    protected virtual void OnButtonPressed()
     => view.Open(Path);
    

    private void Init()
     => Connect("pressed", new Callable(this, nameof(OnButtonPressed)));
    
    public DirectoryEntry(FileExplorerView explorerView, string path)
    {
      view = explorerView;
      Path = path;
      Init();
    }
    
    public DirectoryEntry() { Init(); }
  }

  public partial class ParentDirectoryEntry : DirectoryEntry
  {
    protected override void OnButtonPressed()
     => view.Open(Directory.GetParent(Path).FullName);

    public ParentDirectoryEntry(FileExplorerView v, string path) { Path = path; view = v; }
  }
#endregion

  // TODO?: Create instance version (copy)
  private static readonly Dictionary<string, Type> FileHandlers = []; 
  
  private ScrollContainer scroll = new();
  private GridContainer container = new();

  private void AddFile(string path)
  {
    var type = FileHandlers.GetValueOrDefault(Path.GetExtension(path), typeof(FileEntry));
    Output.Info(type.FullName);
    container.AddChild((FileEntry)Activator.CreateInstance(type, [path]));
  }

  private void RenderDirectory()
  {
    foreach (var child in container.GetChildren()) child.QueueFree();

    var dirs = Directory.GetDirectories(ProjectPath);
    var files = Directory.GetFiles(ProjectPath);

    AddChild(new ParentDirectoryEntry(this, ProjectPath));

    foreach (var file in files) AddFile(file);
    foreach (var dir in dirs) AddChild(new DirectoryEntry(this, dir));
  }

  public override void _Ready()
  {
    scroll.SizeFlagsHorizontal = SizeFlags.ExpandFill;
    scroll.SizeFlagsVertical = SizeFlags.ExpandFill;
    container.SizeFlagsHorizontal = SizeFlags.ExpandFill;
    container.SizeFlagsVertical = SizeFlags.ExpandFill;
    container.Columns = 8;

    AddChild(scroll);
    scroll.AddChild(container);
    RenderDirectory();
  }

  public void Open(string path)
  {
    ProjectPath = path;
    RenderDirectory();
  }

  public static void InitEngine()
  {
    var assembly = YumStudioEngine.GetEngineAssembly();
    var fileTypes = assembly
                   .Where(t => t.IsAssignableTo(typeof(FileEntry)))
                   .ToList();

    foreach (var fileType in fileTypes)
    {
      FileHandlers[((FileEntry)Activator.CreateInstance(fileType)).GetExtension()] = fileType;
    }
  }

  public FileExplorerView() {}
  public FileExplorerView(string path) { Open(path); }
}