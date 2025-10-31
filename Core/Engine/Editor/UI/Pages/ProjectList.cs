using Godot;
using YumStudio.Core.Engine.Cycles;
using YumStudio.Core.Engine.Editor.Projects;

namespace YumStudio.Core.Engine.Editor.UI.Pages;

[OnEditorReady]
public partial class ProjectList : Control
{
  private VBoxContainer projectsBox = new();
  private bool projectsBoxInit = false;

  private void BuildProjectBox()
  {
    if (projectsBoxInit) return;
    AddChild(projectsBox);
    projectsBox.AnchorLeft = 0;
    projectsBox.AnchorTop = 0;
    projectsBox.AnchorRight = 1;
    projectsBox.AnchorBottom = 1;
    projectsBoxInit = true;
  }
  
  private void AddProject(ProjectFile project)
  {
    HBoxContainer panel = new();
    Label label = new() { Text = $"{project.Name} | {(string.IsNullOrEmpty(project.Kind) ? "UNKOWN" : project.Kind)} | {project.Path}" };
    Button button = new() { Text = "Edit" };

    panel.AddChild(label);
    panel.AddChild(button);
    button.Connect("pressed", Callable.From(() =>
    {
      // TODO: already loaded windows

    }));
    projectsBox.AddChild(panel);
  }

  public override void _Ready()
  {
    BuildProjectBox();
    var projects = ProjectSection.Projects;
    foreach (var project in projects)
    {
      AddProject(project.Value);
    }
  }
}
