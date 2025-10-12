using Godot;
using YumStudio.Core.Engine.Editor.Projects;

namespace YumStudio.TestScripts;

public partial class Test : Control
{
  public override void _Ready()
  {
    var proj = ProjectManager.CreateProject("ys-test", "./Tests/YS/");
    proj.Fire();
  }

  public override void _Process(double delta)
  {
    GetTree().Quit();
  }
}
