using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Godot;
using YumStudio.Core.Engine.Cycles;

namespace YumStudio.Core.Engine.Editor.ProjectEditor.Views;

[OnEngineReady]
public partial class FileExplorerView : EditorViewport
{
#region inner classes
  public partial class FileEntry : DisposableInterface
  {
    public string FilePath { get; private set; }
    protected TextureButton button = new();
    protected Label name = new();
    protected VBoxContainer itemBox = new(); 

    public virtual string GetExtension() { return ""; }

    protected virtual void OnButtonPressed() { }

    protected virtual void Init()
    {
      button.TextureNormal = ResourceLoader.Load<Texture2D>("res://assets/icons/documents/empty-page.svg");
    }

    private void SelfInit()
    {
      AddChild(itemBox);
      itemBox.SetAnchorsPreset(LayoutPreset.FullRect);
      itemBox.AddChild(button);
      itemBox.AddChild(name);
      name.Text = Path.GetFileName(FilePath);
      button.Connect("pressed", new(this, nameof(OnButtonPressed)));
      button.CustomMinimumSize = new(100, 100);
      button.SizeFlagsHorizontal = SizeFlags.ExpandFill;
      button.SizeFlagsVertical = SizeFlags.ExpandFill;
      CustomMinimumSize = new(Math.Max(100, name.Size.X), 100);
      Init();
    }

    public FileEntry(string path) { FilePath = path; SelfInit(); }
    public FileEntry() { SelfInit(); }
  }

  public partial class DirectoryEntry : DisposableInterface
  {
    public string FolderPath { get; protected set; }
    protected FileExplorerView view;
    protected TextureButton button = new();
    protected Label name = new();
    protected VBoxContainer itemBox = new(); 

    protected virtual void OnButtonPressed()
     => view.Open(FolderPath);


    protected virtual void Init()
    {
      button.TextureNormal = ResourceLoader.Load<Texture2D>("res://assets/icons/documents/folder.svg");
    }

    private void SelfInit()
    {
      AddChild(itemBox);
      itemBox.SetAnchorsPreset(LayoutPreset.FullRect);
      itemBox.AddChild(button);
      itemBox.AddChild(name);
      name.Text = Path.GetFileName(FolderPath);
      button.Connect("pressed", new(this, nameof(OnButtonPressed)));
      button.CustomMinimumSize = new(100, 100);
      button.SizeFlagsHorizontal = SizeFlags.ExpandFill;
      button.SizeFlagsVertical = SizeFlags.ExpandFill;
      CustomMinimumSize = new(Math.Max(100, name.Size.X), 100);
      Init();
    }
    
    public DirectoryEntry(FileExplorerView explorerView, string path)
    {
      view = explorerView;
      FolderPath = path;
      SelfInit();
    }
    
    public DirectoryEntry() { SelfInit(); }
  }

  public partial class ParentDirectoryEntry : DirectoryEntry
  {
    protected override void OnButtonPressed()
     => view.Open(Directory.GetParent(FolderPath).FullName);

    public ParentDirectoryEntry(FileExplorerView v, string path) { FolderPath = path; view = v; }
  }
#endregion

  // TODO?: Create instance version (copy)
  private static readonly Dictionary<string, Type> FileHandlers = []; 
  
  private ScrollContainer scroll = new();
  private GridContainer container = new();

  private void AddFile(string path)
  {
    var type = FileHandlers.GetValueOrDefault(Path.GetExtension(path), typeof(FileEntry));
    container.AddChild((FileEntry)Activator.CreateInstance(type, [path]));
  }

  private void RenderDirectory()
  {
    foreach (var child in container.GetChildren()) child.QueueFree();

    var dirs = Directory.GetDirectories(ProjectPath);
    var files = Directory.GetFiles(ProjectPath);

    container.AddChild(new ParentDirectoryEntry(this, ProjectPath));

    foreach (var dir in dirs)
    {
      var dirUI = new DirectoryEntry(this, dir)
      {
        CustomMinimumSize = new(100, 100)
      };
      container.AddChild(dirUI);
    }
    foreach (var file in files) AddFile(file);
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
    scroll.SetAnchorsPreset(LayoutPreset.FullRect);
    container.SetAnchorsPreset(LayoutPreset.FullRect);
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
      var ext = (FileEntry)Activator.CreateInstance(fileType);
      FileHandlers[ext.GetExtension()] = fileType;
      ext.QueueFree();
    }
  }

  public FileExplorerView() {}
  public FileExplorerView(string path) { Open(path); }
}