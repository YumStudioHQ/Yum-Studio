using Godot;
using YumStudio.Core.Engine.Cycles;
using YumStudio.Core.Engine.Editor.Projects;
using YumStudio.Core.Engine.Editor.UI.Panels;

namespace YumStudio.Core.Engine.Editor.UI.Home;

public partial class GDWelcome : Control
{
  private Window newProjectWindow;

  public override void _Ready()
  {
    newProjectWindow = GetNode<Window>("NewProjectWindow");
  }

  private void GDSignal_on_new_project_pressed()
  {
    newProjectWindow.Visible = true;
  }

  private void GDSignal_on_new_project_window_close_requested()
  {
    newProjectWindow.Visible = false;
  }

  private void GDSignal_on_ok_btn_pressed()
  {
    var node = GetNode<NewProjectPanel>("NewProjectWindow/NewProjectPanel");
    // TODO: Errors?
    ProjectManager.CreateProject(node.ProjectName(), node.ProjectPath()).Fire();
    newProjectWindow.Visible = false;
    // TODO: Open the project
  }
}

[OnEditorReady]
public partial class Welcome : Control
{
  public override void _Ready()
  {
    AddChild(ResourceLoader.Load<PackedScene>("res://Core/Engine/Editor/UI/Home/welcome.tscn").Instantiate());
  }
}