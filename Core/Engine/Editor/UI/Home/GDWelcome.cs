using Godot;
using YumStudio.Core.Engine.Cycles;

namespace YumStudio.Core.Engine.Editor.UI.Home;

public partial class GDWelcome : Control
{
  public override void _Ready()
  {
    
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