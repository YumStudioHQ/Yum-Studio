using Godot;
using System;


namespace YumStudio.TestScripts;

public partial class Test : Control
{
  public override void _Ready()
  {
    var file = FileAccess.Open("res://Tests/useless.txt", FileAccess.ModeFlags.Read);
    GD.Print(file.GetAsText());
  }
}
