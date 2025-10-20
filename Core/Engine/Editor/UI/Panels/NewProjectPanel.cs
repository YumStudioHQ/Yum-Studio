using Godot;
using System;
using System.IO;

namespace YumStudio.Core.Engine.Editor.UI.Panels;

public partial class NewProjectPanel : Control
{
  private LineEdit lineProjectName;
  private LineEdit lineProjectPath;

  public override void _Ready()
  {
    lineProjectName = GetNode<LineEdit>("LineProjectName");
    // TODO Path.Selector(@R?)
    lineProjectPath = GetNode<LineEdit>("LineProjectPath");
  }

  public string ProjectName() => lineProjectName.Text;
  public string ProjectPath() => Path.GetFullPath(lineProjectPath.Text);
}
